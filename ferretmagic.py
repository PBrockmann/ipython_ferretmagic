# -*- coding: utf-8 -*-
"""
===========
ferretmagic
===========

Magics for interacting with ferret via pyferret.

.. note::

  The ``pyferret`` module needs to be installed first

Usage
=====

``%%ferret``

{ferret_DOC}

``%ferret_run``

{ferret_RUN_DOC}

``%ferret_getdata``

{ferret_GETDATA_DOC}

``%ferret_putdata``

{ferret_PUTDATA_DOC}

"""

#-----------------------------------------------------------------------------
#  Patrick.Brockmann@lsce.ipsl.fr
#
#  Release: 0.6 - 2013/08/28
#
#-----------------------------------------------------------------------------

import sys
import os.path
import tempfile
from glob import glob
from shutil import rmtree

import numpy as np
import pyferret
from xml.dom import minidom

from IPython.core.displaypub import publish_display_data
from IPython.core.magic import Magics, magics_class, line_magic, cell_magic, needs_local_scope
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring
from IPython.utils.py3compat import unicode_to_str
from pexpect import ExceptionPexpect

class ferretMagicError(Exception):
    pass

@magics_class
class ferretMagics(Magics):
    """A set of magics useful for interactive work with ferret via pyferret.

    """
#----------------------------------------------------
    def __init__(self, shell):
        """
        Parameters
        ----------
        shell : IPython shell

        """
        super(ferretMagics, self).__init__(shell)
        try:
            pyferret.start(journal=False, unmapped=True)
        except ExceptionPexpect:
            raise ferretMagicError('pyferret cannot be started')

        # Allow publish_display_data to be overridden for
        # testing purposes.
        self._publish_display_data = publish_display_data

#----------------------------------------------------
    @magic_arguments()
    @argument(
        'string',
	nargs='*'
        )
    @line_magic
    def ferret_run(self, line):
        '''
        Line-level magic to run a command in ferret.

            In [19]: %ferret_run 'let a = 12'

        '''
	args = parse_argstring(self.ferret_run, line)

	code = unicode_to_str(" ".join(args.string))
	pyferret.run(self.shell.ev(code))

#----------------------------------------------------
    @magic_arguments()
    @argument(
        '--create_mask', default=False, action='store_true',
        help='The data array associated with the "data" key will be a MaskedArray NumPy array instead an ordinary NumPy array.'
        )
    @argument(
        'code',
	nargs='*'
        )
    @line_magic
    def ferret_getdata(self, line):
        '''
        Line-level magic to get data from ferret.

            In [18]: %%ferret
               ....: use levitus_climatology
            In [19]: %ferret_getdata tempdict = temp
            In [20]: tempdict 

        '''

	args = parse_argstring(self.ferret_getdata, line)

	code = unicode_to_str(args.code[0])
	pythonvariable = code.split('=')[0]
	ferretvariable = code.split('=')[1]
	exec('%s = pyferret.getdata("%s", %s)' % (pythonvariable, ferretvariable, args.create_mask) )
	self.shell.push("%s" % pythonvariable)
        self._publish_display_data('ferretMagic.ferret', {'text/html': 
		'<pre style="background-color:#F2F5A9; border-radius: 4px 4px 4px 4px; font-size: smaller">' +
		'Message: ' + pythonvariable + " is now available in python as a dictionary containing the variable's metadata and data array."
		'</pre>' 
	})

#----------------------------------------------------
    @magic_arguments()
    @argument(
        '--axis_pos', default=None, 
        help='Order of the axes. Default mode uses a reasonable guess from examining the axis types.'
        )
    @argument(
        'code',
	nargs='*'
        )
    @line_magic
    def ferret_putdata(self, line):
        '''
        Line-level magic to put data to ferret.

            In [18]: a=12
            In [19]: %ferret_putdata a
            In [20]: %%ferret
               ....: list a

        '''
	args = parse_argstring(self.ferret_putdata, line)

	ferretvariable = unicode_to_str(args.code[0])
	if args.axis_pos:
		axis_pos_variable = eval(args.axis_pos)
	else:
		axis_pos_variable = None
	pyferret.putdata(self.shell.user_ns[ferretvariable], axis_pos=axis_pos_variable)
        self._publish_display_data('ferretMagic.ferret', {'text/html': 
		'<pre style="background-color:#F2F5A9; border-radius: 4px 4px 4px 4px; font-size: smaller">' +
		'Message: ' + ferretvariable + ' is now available in ferret.'
		'</pre>' 
	})

#----------------------------------------------------
    @magic_arguments()
    @argument(
        '-m', '--memory', type=int,
        help='Physical memory used by ferret expressed in megawords. Default is 50 megawords = 400 megabytes.'
        )
    @argument(
        '-s', '--size',
        help='Pixel size of plots, "width x height". Default is "-s 600x500".'
        )
    @argument(
        '-a', '--antialias', default=False, action='store_true',
        help='Use anti-aliasing technics to improve the appearance of images and get smoother edges.' 
        )
    @argument(
        '-p', '--pdf', type=str,
        help='Output plot as a pdf file. Extension must be ".pdf". Size has no matter since pdf is a vector output.'
        )
    @needs_local_scope
    @cell_magic
    def ferret(self, line, cell, local_ns=None):
        '''
            In [10]: %%ferret
               ....: let a=12
               ....: list a

        The size of output plots can be specified:
            In [18]: %%ferret -s 800,600 
                ...: plot i[i=1:100]

        '''
	args = parse_argstring(self.ferret, line)

	code = cell.split('\n')

        # If there is no local namespace then default to an empty dict
        if local_ns is None:
            local_ns = {}

	# Temporary directory
        plot_dir = tempfile.mkdtemp().replace('\\', '/')

	# Memory setting
	# With Ferret v6.8 and higher you are allocating double-precision "words"
        if args.memory:
        	(errval, errmsg) = pyferret.run('set memory/size=%s' % args.memory)
	else:
        	(errval, errmsg) = pyferret.run('set memory/size=50')

	# Plot size
        plot_width_default = 1098
        plot_height_default = 824
        if args.size:
            plot_size  = args.size.split(',')
            plot_width  = int(plot_size[0])
            plot_height  = int(plot_size[1])
        else:
            plot_width = 600
            plot_height = 500

	#-------------------------------
	# Start of ferret script for png output
	(errval, errmsg) = pyferret.run('set mode metafile:"%(plot_dir)s/__ipy_ferret_fig.png"' % locals())
	# Set window with correct aspect and size
        (errval, errmsg) = pyferret.run('set window/aspect=`%(plot_height)s/%(plot_width)s`/size=`(0.7*%(plot_width)s*%(plot_height)s)/(%(plot_width_default)s*%(plot_height_default)s)` 1' % locals())
	# SDOUT handling
        (errval, errmsg) = pyferret.run('set redirect/clobber/file="%(plot_dir)s/__ipy_ferret_tmp.txt" stdout' % locals())
	# Set graphics with or without antialias
	if args.antialias:
        	(errval, errmsg) = pyferret.run('set graphics/antialias')
	else:
        	(errval, errmsg) = pyferret.run('set graphics/noantialias')
	# Run code
	pyferret_error = False
        FERR_OK = 3
        for input in code:
            input = unicode_to_str(input)
            (errval, errmsg) = pyferret.run(input)
            if errval != FERR_OK :
            	self._publish_display_data('ferretMagic.ferret', {'text/html': 
									'<pre style="background-color:#F79F81; border-radius: 4px 4px 4px 4px; font-size: smaller">' +
            								'yes? %s\n' % input +
									'error val = %s\nerror msg = %s' % (errval, errmsg) +
									'</pre>' 
								})
		pyferret_error = True
		break
	# Close output file 
        (errval, errmsg) = pyferret.run('cancel mode metafile')
	# Close stdout
        (errval, errmsg) = pyferret.run('cancel redirect')
	# Close window
	(errval, errmsg) = pyferret.run('cancel window 1')
	#-------------------------------

        # Publish
        key = 'ferretMagic.ferret'
        display_data = []

        # Publish text output
	try:
		text_outputs = []
		text_outputs.append('<pre style="background-color:#ECF6CE; border-radius: 4px 4px 4px 4px; font-size: smaller">')
        	f = open ("%(plot_dir)s/__ipy_ferret_tmp.txt" % locals(),"r")
		for line in f:
			text_outputs.append(line)
		f.close()
		text_outputs.append("</pre>")
		text_output = "".join(text_outputs)
        	display_data.append((key, {'text/html': text_output}))
	except:
		pass

        # Publish image if present
	try:
        	image = open("%(plot_dir)s/__ipy_ferret_fig.png" % locals(), 'rb').read() 
        	display_data.append((key, {'image/png': image}))
	except:
		pass

	# Delete temporary directory
        rmtree(plot_dir)

	# Set output as pdf
        if args.pdf and not pyferret_error:
		pdf_file = args.pdf
		#-------------------------------
		# Start of ferret script for pdf output
		(errval, errmsg) = pyferret.run('set mode metafile:"%(pdf_file)s"' % locals())
		# Set window with correct aspect
        	(errval, errmsg) = pyferret.run('set window/aspect=`%(plot_height)s/%(plot_width)s` 1' % locals())
		# SDOUT handling
        	(errval, errmsg) = pyferret.run('set redirect/clobber/file="%(plot_dir)s/__ipy_ferret_tmp.txt" stdout' % locals())
		# Run code
		pyferret_error = False
        	FERR_OK = 3
        	for input in code:
            		input = unicode_to_str(input)
            		(errval, errmsg) = pyferret.run(input)
            		if errval != FERR_OK :
				pyferret_error = True
				break
		# Close output file 
        	(errval, errmsg) = pyferret.run('cancel mode metafile')
		# Close stdout
        	(errval, errmsg) = pyferret.run('cancel redirect')
		# Close window
		(errval, errmsg) = pyferret.run('cancel window 1')
		#-------------------------------

        	# Create link to pdf if no error and file exist
        	if not pyferret_error and os.path.isfile("%(pdf_file)s" % locals()):
			text_outputs = []
			text_outputs.append('<pre style="background-color:#F2F5A9; border-radius: 4px 4px 4px 4px; font-size: smaller">')
			# file visible from cell from files directory
            		text_outputs.append('Message: <a href="files/%(pdf_file)s" target="_blank">%(pdf_file)s</a> also available.' % locals())
            		text_outputs.append('</pre>')
			text_output = "".join(text_outputs)
        		display_data.append((key, {'text/html': text_output}))

	# Publication
        for source, data in display_data:
          	self._publish_display_data(source, data)

#----------------------------------------------------
__doc__ = __doc__.format(
    ferret_DOC = ' '*8 + ferretMagics.ferret.__doc__,
    ferret_RUN_DOC = ' '*8 + ferretMagics.ferret_run.__doc__,
    ferret_GETDATA_DOC = ' '*8 + ferretMagics.ferret_getdata.__doc__,
    ferret_PUTDATA_DOC = ' '*8 + ferretMagics.ferret_putdata.__doc__
    )


def load_ipython_extension(ip):
    """Load the extension in IPython."""
    ip.register_magics(ferretMagics)

ipython-ferretmagic
===================

IPython notebook extension for ferret (a great software for Data Visualisation and Analysis from NOAA/PMEL).

Browse the demo notebooks from http://nbviewer.ipython.org/github/PBrockmann/ipython-ferretmagic/tree/master/

## Latest news 

Combine pyferret and ipython widgets and create interactive notebooks !

![ScreenShot](ferretmagic_widgets.png)

## Installation

Install pyferret following instructions from http://ferret.pmel.noaa.gov/Ferret/documentation/pyferret.

Once you can import the pyferret module in ipython then install the ipython notebook extension.

In IPython, install ferretmagic (you get a warning I have to figure out):

    In [1]: %install_ext https://raw.github.com/PBrockmann/ipython-ferretmagic/master/ferretmagic.py

Tested with pyferret 1.2.0 and Jupiter 4.0.x
    
## Usage

In IPython, load the magics:

    In [2]: %reload_ext ferretmagic
   
### Line magics

The `%ferret_run` magic enables one-line execution of ferret command in the IPython interpreter or notebook:

```
    In [3]: for i in [100,500,1000]:
      ....: 	%ferret_run -s 400,400 'plot sin(i[i=1:%(i)s]*0.1)' % locals()
```

### Cell magics

Multi-line input can be entered with the `%%ferret` cell magic:

```
In [4]: %%ferret
  ....: use levitus_climatology
  ....: shade temp[k=1]			! comments
```

* Control size of plot with --size, -s option.
* Create a local pdf at the same time with --pdf, -p option.

```
In [5]: %%ferret -s 400,300 -pdf myfig.pdf
  ....: shade temp[k=1]			
```

### Passing variables between Python and ferret 

* Variables can be pushed from IPython into ferret with `%ferret_putdata`:

```
In [18]: %%ferret
   ....: use levitus_climatology
In [19]: %ferret_getdata tempdict = temp
   ....: Message: tempdict is now available in python as a dictionary containing the variable's metadata and data array.
In [20]: print tempdict.keys()
   ....: ['axis_coords', 'axis_types', 'data_unit', 'axis_units', 'title', 'axis_names', 'missing_value', 'data']
```

* Variables can be pulled from ferret into IPython with `%ferret_getdata`:

```
In [31]: import numpy as np
   ....: b = {}
   ....: b['name']='myvar'
   ....: b['name']='myvar'
   ....: x=np.linspace(-np.pi*4, np.pi*4, 500)
   ....: b['data']=np.sin(x)/x
   ....: b.keys()
Out[31]: ['data', 'name']
In [32]: %ferret_putdata --axis_pos (1,0,2,3,4,5) b
   ....: Message: b is now available in ferret as myvar
```

Explore notebook for examples.

## Known issues and limitations

* Note that the pdf file produced by -p,--pdf option is not embedded in the notebook
* Limitations are the ones exposed from pyferret, the qualifier /pattern is not usable for example. Read http://ferret.pmel.noaa.gov/Ferret/documentation/pyferret/known-issues


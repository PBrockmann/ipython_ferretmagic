import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
  name = 'ferretmagic',
  packages = ['ferretmagic'],
  py_modules = ['ferretmagic'],
  version = '20220825',
  description = 'ipython extension for pyferret',
  author = 'Patrick Brockmann',
  author_email = 'Patrick.Brockmann@lsce.ipsl.fr',
  long_description=long_description,
  long_description_content_type="text/markdown",
  url = 'https://github.com/PBrockmann/ipython_ferretmagic',
  download_url = 'https://github.com/PBrockmann/ipython_ferretmagic/tarball/master',
  keywords = ['jupyter', 'ipython', 'ferret', 'pyferret', 'magic', 'extension'],
  classifiers = [
        'Programming Language :: Python :: 3',
	'License :: OSI Approved :: MIT License',
	'Operating System :: OS Independent',
	'Framework :: Jupyter',
	'Framework :: IPython'
  ],
)

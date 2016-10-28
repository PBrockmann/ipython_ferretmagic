from distutils.core import setup

setup(
  name = 'ipython_ferretmagic',
  packages = ['ipython_ferretmagic'],
  install_requires=['ipython'],
  py_modules=['ipython_ferretmagic'],
  version = '2016.10',
  description = 'ipython extension for pyferret',
  author = 'Patrick Brockmann',
  author_email = 'Patrick.Brockmann@lsce.ipsl.fr',
  url = 'https://github.com/PBrockmann/ipython_ferretmagic', 
  download_url = 'https://github.com/PBrockmann/ipython_ferretmagic/tarball/master',
  keywords = ['ipython', 'jupyter', 'ferret', 'pyferret', 'magic', 'extension'], 
  classifiers = [],
)

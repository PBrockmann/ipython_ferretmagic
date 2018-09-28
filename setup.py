import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
  name = 'ferretmagic',
  packages = ['ferretmagic'],
  py_modules = ['ferretmagic'],
  version = '2018.09.28',
  description = 'ipython extension for pyferret',
  author = 'Patrick Brockmann',
  author_email = 'Patrick.Brockmann@lsce.ipsl.fr',
  url = 'https://github.com/PBrockmann/ipython_ferretmagic',
  download_url = 'https://github.com/PBrockmann/ipython_ferretmagic/tarball/master',
  keywords = ['jupyter', 'ipython', 'ferret', 'pyferret', 'magic', 'extension'],
  classifiers = []
)

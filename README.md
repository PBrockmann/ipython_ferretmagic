ipython-ferretmagic
===================

ipython notebook extension for ferret

## Installation

Install pyferret from instruction from http://ferret.pmel.noaa.gov/Ferret/documentation/pyferret.
Once you can import pyferret module then install the ipython notebook extension 

In IPython, install ferretmagic:

    In [1]: %install_ext https://raw.github.com/PBrockmann/ipython-ferretmagic/master/ferretmagic.py
    
## Usage

In Ipython, load the magics:

    In [2]: %reload_ext ferretmagic
   
### Line magics

The `%ferret_run` magic enables one-line execution of ferret command in the IPython interpreter or notebook:

```
In [3]: %ferret_run 'let a=12'
```

### Cell magics

Multi-line input can be entered with the `%%ferret` cell magic:

```
In [4]: %%ferret
   ...: use levitus_climatology
   ...: shade temp[k=1]			! comments
```

* Control size of plot with --size, -s option.
* Create a local pdf at the same time with --pdf, -p option.
* Improve your graphic with antialiasing with --antialias, -a option.

```
In [5]: %%ferret -a -s 400,300 -pdf myfig.pdf
   ...: shade temp[k=1]			
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
In [9]: %ferret_putdata sstdict
```
sstdict is now available in python as a dictionary containing the variable's metadata and data array.

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

* pdf are not embedded in the notebook
* Only one plot can be rendered per cell
* Limitations are the ones exposed from pyferret (the qualifier /pattern is not usable for example) for example. Read http://ferret.pmel.noaa.gov/Ferret/documentation/pyferret/known-issues


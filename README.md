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

Control size of plot with --size, -s option.
Create a local pdf at the same time with --pdf, -p option.
Improve your graphic with antialiasing with --antialias, -a option.

In [5]: %%ferret -a -s 400,300 -pdf myfig.pdf
   ...: shade temp[k=1]			

### Passing variables between Python and ferret 

Variables may be pushed from IPython into ferret with `%ferret_putdata`:
Variables may be pulled from ferret into IPython with `%ferret_getdata`:

Explore notebook for examples.

## Known issues and limitations

* pdf are not embedded in the notebook
* Only one plot can be rendered per cell
* Limitations are the ones exposed from pyferret (the qualifier /pattern is not usable for example) for example . Read http://ferret.pmel.noaa.gov/Ferret/documentation/pyferret/known-issues


"""Okean ocean modelling and analysis tools ...

Requires:
    NumPy
    matplotlib with the Basemap toolkit
    netcdf interface for python (like netCDF4)

"""

import glob
from numpy.distutils.core import setup
from numpy.distutils.core import Extension
from numpy.distutils.command.install import install

classifiers = """\
Development Status :: alpha
Environment :: Console
Intended Audience :: Science/Research
Intended Audience :: Developers
License :: European Union Public Licence - EUPL v.1.1
Operating System :: OS Independent
Programming Language :: Python
Topic :: Scientific/Engineering
Topic :: Software Development :: Libraries :: Python Modules
"""


class my_install(install):
    def run(self):
        install.run(self)

        # Post installation:
        # Link pppack
        # import os
        # from distutils.sysconfig import get_python_lib
        # p = get_python_lib(plat_specific=1)  # Installation folder.
        # src = os.path.join(p,'okean', 'roms', 'rtools.so')
        # dest = os.path.join(p,'okean', 'pppack.so')


alg = Extension(name='alg',
                sources=['okean/ext/alg.f'])

pnpoly = Extension(name='pnpoly',
                   sources=['okean/ext/pnpoly.f'])

rtools = Extension(name='roms.rtools',
                   sources=['okean/roms/ext/rtools.f90',
                            'okean/ext/pppack.f90'])

pppack = Extension(name='pppack',
                   sources=['okean/ext/pppack.f90'])

lu = Extension(name='lusolver',
               sources=['okean/ext/lu.f90'])

doclines = __doc__.split("\n")


def get_version():
    v = 'unknonw'
    lines = open('okean/__init__.py').readlines()
    for l in lines:
        if l.startswith('__version__'):
            v = eval(l.split('=')[-1])
    return v


setup(name="okean",
        version=get_version(),
        description=doclines[0],
        long_description="\n".join(doclines[2:]),
        packages=['okean',
                'okean.roms',
                'okean.roms.inputs',
                'okean.nc',
                'okean.datasets'],
        license='EUPL',
        platforms=["any"],
        ext_package='okean',
        ext_modules=[alg, pnpoly, rtools, pppack, lu],
        classifiers=filter(None, classifiers.split("\n")),
        scripts=['okean/bin/show_nctime',
                'okean/bin/show', 'okean/bin/qstate',
                'okean/bin/romsview'],
        cmdclass={'install': my_install})

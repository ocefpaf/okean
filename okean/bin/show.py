#!/usr/bin/python
from okean import netcdf
from sys import argv
import numpy as np


if len(argv)>=4:
    action=argv[3]
    v,nc=netcdf.var(argv[1],argv[2])

    if len(argv)==6:
        scale=eval(argv[4])
        offset=eval(argv[5])
    else:
        scale,offset=1,0

    if action=='lims':
        # first and last
        print np.array((v[:].flat[:][0],v[:].flat[:][-1]))*scale+offset
    elif action=='list':
        print v[:]*scale+offset
    elif action=='last':
        print v[:].flat[:][0]*scale+offset
    elif action=='range':
        # highest and lowest:
        print np.array(v.range())*scale+offset

    nc.close()

elif len(argv)==3:
    netcdf.showvar(argv[1],argv[2])
elif len(argv)==2:
    netcdf.show(argv[1])
else:
    print 'wrong arguments'
    print 'usage: show filename [varname [<action>] [<scale> <offset>]]'
    print 'where action can be: lims, list, last or range'
    print ''
    print 'mma dec 2009'

print ''

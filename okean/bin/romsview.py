#!/usr/bin/python

if __name__=='__main__':
    import sys
    import argparse
    from okean import roms, cache

    parser = argparse.ArgumentParser()
    parser.add_argument("source", help="ROMS netcdf file (clm, his, ini, avg) or opendap address",type=str)
    parser.add_argument("varname", help="variable to plot", type=str)
    for i in 'xyzt':
        parser.add_argument("-%s"%i, help="%s index"%i)

    parser.add_argument('-iso', help='iso value for sliceiso')
    parser.add_argument('-c', help='coords',type=str)
    parser.add_argument('-surf_nans', default=True, help='extrap in the vertical in shallow slicez depths')#,type=bool)
    parser.add_argument('-xy', help='x,y points for slicell')
    parser.add_argument('--opts', help="plot options",type=str)

    args = parser.parse_args()



    x=getattr(args,'x')
    y=getattr(args,'y')
    z=getattr(args,'z')
    t=getattr(args,'t')
    iso=getattr(args,'iso')
    xy=getattr(args,'xy')

    coords=getattr(args,'c')
    surfnans=getattr(args,'surf_nans')
    try: surfnans=eval(surfnans)
    except: pass

    ind=None
    if not z is None:
        z=float(z)
        if z>=0 or z==-1: meth,ind='slicek', int(z)
        elif z<0: meth,ind='slicez',z

    if not x is None:
        ind=int(x)
        meth='slicei'

    if not y is None:
        ind=int(y)
        meth='slicej'

    if not iso is None:
        ind=float(iso)
        meth='sliceiso'

    if not xy is None:
        x0,y0=eval(xy)[0]
        x1,y1=eval(xy)[1]
        npts=eval(xy)[2]
        import numpy as np
        xp=np.linspace(x0,x1,npts)
        yp=np.linspace(y0,y1,npts)
        meth='slicell'

    if not t is None: t=int(t)

    if coords is None: coords=roms.His._default_coords(meth)
    else: coords=','.join(sorted(coords.split(',')))

    print ind, t, meth


    moreInfo=''
    moreArgs={}
    if meth=='slicez':
        moreInfo=surfnans
        moreArgs=dict(surf_nans=surfnans)
    elif meth=='slicell':
        moreInfo=xp,yp


    cacheLab=str((args.source,args.varname,meth,ind,t,coords,moreInfo))
    print cacheLab
    cch=cache.Cache()
    if cch.is_stored(cacheLab,'localfile'):
        d=cch.load(cacheLab,'localfile')
    else:
##    print args.varname,ind,t,coords
##    sys.exit()
        r=roms.His(args.source)

        if args.varname[0]=='*':
            args.varname=args.varname[1:]
            meth='slice_derived'

        if meth in ['slicei','slicej','slicek','slicez','slice_derived']:
            d=getattr(r,meth)(args.varname,ind,t,coords=coords,**moreArgs)
        elif meth=='slicell':
            d=getattr(r,meth)(args.varname,xp,yp,t,coords=coords,**moreArgs)




        if d.msg:
            print 'ERROR: %s'%d.msg
            sys.exit()
        cch.store(cacheLab,d,'localfile')

#  print meth
#  d.plot()
#  import pylab as pl
#  pl.show()
#  sys.exit()

    # plot options:
    opts={}
    if  args.opts:
        for o in args.opts.split(';'):
            oname,oval=o.split('=')
            oname=oname.strip()
            oval=oval.strip()
            print oname, oval

            # check if conf is for extras (need to find 2 '.')
            if sum([i=='.' for i in oname])>1:
                alias=oname[:oname.find('.')]
                oname=oname[oname.find('.')+1:]
                for i in d.extra:
                    print '\n checking alias'
                    if i.alias==alias:
                        print '\n found %s %s'%(alias,oname),oval
                        try:    i.config[oname]=eval(oval)
                        except: i.config[oname]=oval
                        break

            else: # apply conf to main obj
                try:    d.config[oname]=eval(oval)
                except: d.config[oname]=oval

    import pylab as pl
#  d.extra=[]
    d.plot()
    if meth in ['slicei','slicej']:
        d.ax.axis('tight')

     # pl.figure(), pl.pcolormesh(d.d,d.z,d.z)
    pl.show()

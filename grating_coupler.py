import nazca as nd
import nazca.demofab as demo
import numpy as np
from nazca.interconnects import Interconnect

Minimum_Radius = 50
Minimum_Width = 0.3
IndivLength = 20

SIN = (1, 0)
nd.add_layer('SIN', SIN)
nd.add_xsection('SIN Waveguide')
nd.add_layer2xsection('SIN Waveguide', layer=SIN)

WG_route = nd.interconnects.Interconnect(width=Minimum_Width, radius=Minimum_Radius, xs='SIN Waveguide')
  
def grating_coupler(Rmax, Rmin, angle, wg_wth):
    with nd.Cell ("grating_coupler") as grating:
        delR = 0.45
        r = Rmin
        while (r < Rmax):
            WG_route.bend(radius = r, width= 0.3).put(r,0,90)
            r = r + delR
        WG_route.bend(radius = Rmin/2, width= Rmin).put(Rmin/2,0,90)
        WG_route.strt(length= Rmax, width=0.1).put(Rmin/4, Rmin/4,-135)
        
    return grating
width = 0.3
angle2 = 0.4468
angle1 = np.pi/4
Rmax = 34
Rmin = 22
x_0 = 60
grating_coupler(Rmax=34, Rmin=22, angle = angle2, wg_wth=0.1).put()
grating_coupler(Rmax=34, Rmin=22, angle = angle2, wg_wth=0.1).put(50, 50, 90)
grating_coupler(Rmax=34, Rmin=22, angle = angle2, wg_wth=0.1).put(0, -50, 45)
grating_coupler(Rmax=34, Rmin=22, angle = angle2, wg_wth=0.1).put(-50, 0, -45)

# r = 10
# WG_route.bend(radius = r, width= 0.3). put (x_0+r*np.cos(angle1), -r*np.sin(angle1), -angle1*180/(2*np.pi))
# r = 2
# WG_route.bend(radius = r, width= 0.3). put (x_0+r*np.cos(angle1), -r*np.sin(angle1), -angle1*180/(2*np.pi))
# r = 30 
# WG_route.bend(radius = r, width= 0.3). put (x_0+r*np.cos(angle1), -r*np.sin(angle1), -angle1*180/(2*np.pi))
# r = 40 
# WG_route.bend(radius = r, width= 0.3). put (x_0+r*np.cos(angle1), -r*np.sin(angle1), -angle1*180/(2*np.pi))
# r = 50 
# WG_route.bend(radius = r, width= 0.3). put (x_0+r*np.cos(angle1), -r*np.sin(angle1), -angle1*180/(2*np.pi))
# r = 60 
# WG_route.bend(radius = r, width= 0.3). put (x_0+r*np.cos(angle1), -r*np.sin(angle1), -angle1*180/(2*np.pi))

# delR = 0.45
# r = Rmin
# WG_route.bend(radius = r, width= 0.3).put(r,0,90)
# r = Rmin + delR
# WG_route.bend(radius = r, width= 0.3).put(r,0,90)
# r = Rmin + delR
# WG_route.bend(radius = r, width= 0.3).put(r,0,90)
# r = Rmin + delR
# WG_route.bend(radius = r, width= 0.3).put(r,0,90)
# r = Rmin + delR
# WG_route.bend(radius = r, width= 0.3).put(r,0,90)
# r = Rmin + delR
# WG_route.bend(radius = r, width= 0.3).put(r,0,90)
# r = Rmax
# WG_route.bend(radius = r, width= 0.3).put(r,0,90)

# #WG_route.taper(length=Rmin/np.sqrt(2), width1=Rmin*np.sqrt(2), width2=0.1).put(Rmin/2,Rmin/2,-135)
# WG_route.bend(radius = Rmin/2, width= Rmin).put(Rmin/2,0,90)
# WG_route.strt(length= 10, width=0.1).put(Rmin/4, Rmin/4,-135)

nd.export_gds( filename= "grating.gds")
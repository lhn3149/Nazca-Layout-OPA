import nazca as nd
import nazca.demofab as demo
import numpy as np
from nazca.interconnects import Interconnect

#   Grating coupler (GC)
#   Input 
#       Rmax: the maximum radius
#       Rmin: the minimum radius | the grating area is Rmax - Rmin which needs to be greater than 90um
#       angle:  the open angle of the grating coupler
#       wg_wdth:    output waveguide width from the GC
#       gc_witdth:  width of the teeth in the GC area
#       pitch:  pitch between waveguide in GC area | duty cycle can be calculated = wg_wdth/pitch 

Minimum_Radius = 50
Minimum_Width = 0.3
IndivLength = 20

SIN = (1, 0)
nd.add_layer('SIN', SIN)
nd.add_xsection('SIN Waveguide')
nd.add_layer2xsection('SIN Waveguide', layer=SIN)

WG_route = nd.interconnects.Interconnect(width=Minimum_Width, radius=Minimum_Radius, xs='SIN Waveguide')
  
def grating_coupler(Rmax, Rmin, angle, wg_width, gc_width, pitch):
    with nd.Cell ("grating_coupler") as grating:
        r = Rmin
        ang_deg = angle*180/np.pi
        while (r < Rmax):
            WG_route.bend(radius = r, width= gc_width, angle = ang_deg).put(r,0,90)
            r = r + pitch
        WG_route.bend(radius = Rmin/2, width= Rmin, angle = ang_deg).put(Rmin/2,0,90)
        WG_route.strt(length= Rmax, width=wg_width).put(Rmin/4 *np.cos(angle/2), Rmin/4*np.sin(angle/2),-180+ang_deg/2)
    return grating
angle1 = 0.4468
Rmax = 300
Rmin = 150

grating_coupler(Rmax=Rmax, Rmin=Rmin, angle = angle1, gc_width=0.3, pitch= 0.45, wg_width=0.1).put()

nd.export_gds( filename= "grating.gds")
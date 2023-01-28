import nazca as nd
import nazca.demofab as demo
import numpy as np
import math

def OPAarray(N, offset, distribution, width, length):
    with nd.Cell(name='OPAarray') as OPAarray:
        for i in range(N):
            input_name = "a" + str(i)
            output_name = "b" + str(i)
            i = i + 1
            # sbend
            # straight
            print("Position of waveguide", i)
            straight1   = demo.shallow.strt(length=i*N, width = width).put(0, i*offset, 0)
            bend1       = demo.shallow.bend(angle = -90, radius = 10, width = width).put(straight1.pin['b0'])
            straight2   = demo.shallow.strt(length = length, width = width).put(bend1.pin['b0'])
    return OPAarray
    
OPAarray1 = OPAarray(N=6, offset=5, width=2, length=20).put()

nd.export_plt()
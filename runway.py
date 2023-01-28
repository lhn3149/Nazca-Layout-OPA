import nazca as nd
import nazca.demofab as demo
import numpy as np
import math


def runway(N, offset, width, length):
    with nd.Cell(name='runway_OPA') as runwayOPA:
        for i in range(N):
            input_pin = "a" + str(i)
            output_pin = "b" + str(i)
            print("input pin position", input_pin)
            print("output pin position", output_pin)
            i = i + 1
            print("Position of waveguide", i)
            straight1   = nd.strt(length=i*N, width = width).put(0, i*offset, 0)
            bend1       = nd.bend(angle = -90, radius = 10, width = width).put(straight1.pin['b0'])
            straight2   = nd.strt(length = length, width = width).put(bend1.pin['b0'])
            nd.Pin(input_pin, pin=straight1.pin['a0']).put()
            nd.Pin(output_pin, pin=straight2.pin['b0']).put()
    return runwayOPA
# return x average
# return y average  
runway1 = runway(N=7, offset=5, width=2, length=20).put()
print("ending...")
print("debugging process...")
x1 = runway1.pin['b0'].x
x2 = runway1.pin['b1'].x
x_avg = np.mean([x1,x2])
print("average x", x_avg)
print(runway1.pin['a1'].x)
print(runway1.pin['b3'].y)

#nd.export_plt()
nd.export_gds(filename = 'test.gds')
import nazca as nd
import nazca.demofab as demo
import numpy as np
import math

# contain components after the split tree
# runway (curve and bend) and trombone (can use ubend)


def runway(N, offset, width, length, split):
    with nd.Cell(name='runway_OPA') as runwayOPA:
        for i in range(N):
            input_pin = "a" + str(i)
            output_pin = "b" + str(i)
            print("input pin position", input_pin)
            print("output pin position", output_pin)
            i = i + 1
            print("Position of waveguide", i)
            curve = curve_bend(width=width, length1=i*offset, length2=length+i*offset).put(split.pin[output_pin])
            tromb1 = trombone(5, 10, 0.3).put(curve.pin['b0'])
            tromb2 = trombone(5, 10, 0.3).put(tromb1.pin['b0'])
            tromb3 = trombone(5, 10, 0.3).put(tromb2.pin['b0'])

            nd.Pin(input_pin, pin=curve.pin['a0']).put()
            nd.Pin(output_pin, pin=tromb3.pin['b0']).put()
    return runwayOPA

def curve_bend(width, length1, length2):
    with nd.Cell(name='curve') as curve:
        straight1   = nd.strt(length= length1, width = width).put()
        bend1       = nd.bend(angle = -90, radius = 10, width = width).put(straight1.pin['b0'])
        straight2   = nd.strt(length = length2, width = width).put(bend1.pin['b0'])
        nd.Pin('a0', pin=straight1.pin['a0']).put()
        nd.Pin('b0', pin=straight2.pin['b0']).put()
    return curve


def trombone (length, radius, width):
    # bend(90) - straight - bend(180) - straight - bend(90)
    with nd.Cell(name='trombone') as trombone:
        bend1 = nd.bend(angle=-90, radius=radius, width=width).put()
        strt1 = nd.strt(length = length, width=width).put(bend1.pin['b0'])
        bend2 = nd.bend(angle=180, radius = radius, width=width).put()
        strt2 = nd.strt(length = length, width=width).put()
        bend3 = nd.bend(angle=-90, radius=radius, width=width).put()
        nd.Pin('a0', pin=bend1.pin['a0']).put()
        nd.Pin('b0', pin=bend3.pin['b0']).put()
    return trombone

def OPAarray(N, offset, distribution, width, length):
    with nd.Cell(name='OPAarray') as OPAarray:
        for i in range(N):
            input_name = "a" + str(i)
            output_name = "b" + str(i)
            i = i + 1
            print("Position of waveguide", i)
            straight1   = nd.strt(length=i*N, width = width).put(0, i*offset, 0)
            bend1       = nd.bend(angle = -90, radius = 10, width = width).put(straight1.pin['b0'])
            straight2   = nd.strt(length = length, width = width).put(bend1.pin['b0'])
    return OPAarray
    
# OPAarray1 = OPAarray(N=6, offset=5, width=2, length=20).put()
# runway1 = runway(N=7, offset=5, width=2, length=20).put()
# print("ending...")
# print("debugging process...")
# x1 = runway1.pin['b0'].x
# x2 = runway1.pin['b1'].x
# x_avg = np.mean([x1,x2])
# print("average x", x_avg)
# print(runway1.pin['a1'].x)
# print(runway1.pin['b3'].y)

# nd.export_plt()
# nd.export_gds(filename = 'test.gds')


# tromb1 = trombone(10, 50, 0.3).put()
# tromb2 = trombone(10, 50, 0.3).put(tromb1.pin['b0'])
# tromb3 = trombone(10, 50, 0.3).put(tromb2.pin['b0'])

# runway1 = runway(N=16, offset=20, width=0.3, length=20).put()
# nd.export_gds(filename="components.gds")
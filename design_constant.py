import nazca as nd
import nazca.demofab as demo
import numpy as np
from nazca.interconnects import Interconnect
import math
import components

ic = Interconnect(width=0.3, radius=10.0)

nd.logfile(__file__)  # create logfile that will list DRC errors
nd.pin2pin_drc_on()  # switch on pin2pin connection drc

SIN = (1, 0)
nd.add_layer('SIN', SIN)
nd.add_xsection('SIN Waveguide')
nd.add_layer2xsection('SIN Waveguide', layer=SIN)

M1H = (11, 0)
nd.add_layer('M1H', M1H)
nd.add_xsection('Metal Heater')
nd.add_layer2xsection('Metal Heater', layer=M1H)

M1R = (12, 0)  # heater 
nd.add_layer('M1R', M1R)
nd.add_xsection('Top Metal')
nd.add_layer2xsection('Top Metal', layer=M1R)

M1P = (13, 0)
nd.add_layer('M1P', M1P)
nd.add_xsection('Metal Pad')
nd.add_layer2xsection('Metal Pad', layer=M1P)

DT = (201, 0)
nd.add_layer('DeepTrench', DT)
nd.add_xsection('Deep Trench')
nd.add_layer2xsection('Deep Trench', layer=DT)

DTE = (202, 0)
nd.add_layer('DeepTrenchExc', DTE)
nd.add_xsection('Deep Trench Exclusion')
nd.add_layer2xsection('Deep Trench Exclusion', layer=DTE)

ANTF = (290, 0)
nd.add_layer('ANT_FRAME', ANTF)
nd.add_xsection('ANT Frame')
nd.add_layer2xsection(xsection='ANT Frame', layer=ANTF)

# print(nd.show_layers())
# raise_pin
# print(nd.show_xsection_layer_map())

# create interconnect objects and set minimum radii!
Minimum_Radius = 50
Minimum_Width = 0.3
IndivLength = 20

Frame1 = nd.interconnects.Interconnect(xs='ANT Frame', width=50)
Frame2 = nd.interconnects.Interconnect(xs='Deep Trench', width=50)
WG_route = nd.interconnects.Interconnect(width=Minimum_Width, radius=Minimum_Radius, xs='SIN Waveguide')
Metal_route = nd.interconnects.Interconnect(width=10, radius=2.5, xs='Metal Heater') #
Metal_layer = nd.interconnects.Interconnect(width=10, radius=2.5, xs='Top Metal')
ContactCut = nd.interconnects.Interconnect(width=10, radius=2.5, xs='Metal Pad')
with nd.Cell('9x9_Frame') as frame:
    Frame1.strt(width=9000, length=9000).put(0, 4500, 0)

    Frame2.strt(width=200, length=8880+300).put(-100, 0, 0)
    Frame2.strt(width=200, length=8880+200).put(8880+100, 0, 90)

    Frame2.strt(width=200, length=8880+100).put(0, 8880+50, 270)
    Frame2.strt(width=200, length=8880+300).put(-100, 8980, 0)

def mmi(offset,length, width):
    with nd.Cell(name='myMMI') as mymmi:
        elm1 = WG_route.strt(length= length, width=width).put()
        elm2 = WG_route.sbend(offset=offset, width=width, radius = 50).put(elm1.pin['b0'])
        elm3 = WG_route.sbend(offset=-offset,width=width, radius = 50).put(elm1.pin['b0'])

        nd.Pin('a0', pin=elm1.pin['a0']).put()
        nd.Pin('b0', pin=elm2.pin['b0']).put()
        nd.Pin('b1', pin=elm3.pin['b0']).put()
    return mymmi

def laser_input (width, length):
    with nd.Cell(name='laser') as laserinput:
        elm1 = WG_route.strt(length=length, width=width).put(0,0,-90)
        blm1 = WG_route.bend(angle=90, radius=length, width=width).put()

        nd.Pin('a0', pin=elm1.pin['a0']).put()
        nd.Pin('b0', pin=blm1.pin['b0']).put()
    return laserinput

def split_tree (N,offset, length, width):
    with nd.Cell(name="tree") as split_tree:
        if (N == 32):
            mmi1  = mmi(offset=offset, length = length, width = width).put()
            mmi2a = mmi(offset=offset/2, length =length, width = width).put(mmi1.pin['b0'])
            mmi2b = mmi(offset=offset/2, length =length, width = width).put(mmi1.pin['b1'])
            mmi3a = mmi(offset=offset/4, length =length, width = width).put(mmi2a.pin['b0'])
            mmi3b = mmi(offset=offset/4, length =length, width = width).put(mmi2a.pin['b1'])
            mmi3c = mmi(offset=offset/4, length =length, width = width).put(mmi2b.pin['b0'])
            mmi3d = mmi(offset=offset/4, length =length, width = width).put(mmi2b.pin['b1'])

            mmi4a = mmi(offset=offset/8, length =length, width = width).put(mmi3a.pin['b0'])
            mmi4b = mmi(offset=offset/8, length =length, width = width).put(mmi3a.pin['b1'])
            mmi4c = mmi(offset=offset/8, length =length, width = width).put(mmi3b.pin['b0'])
            mmi4d = mmi(offset=offset/8, length =length, width = width).put(mmi3b.pin['b1'])
            mmi4e = mmi(offset=offset/8, length =length, width = width).put(mmi3c.pin['b0'])
            mmi4f = mmi(offset=offset/8, length =length, width = width).put(mmi3c.pin['b1'])
            mmi4g = mmi(offset=offset/8, length =length, width = width).put(mmi3d.pin['b0'])
            mmi4h = mmi(offset=offset/8, length =length, width = width).put(mmi3d.pin['b1'])

            mmi5a = mmi(offset=offset/16, length = length, width = width).put(mmi4a.pin['b0'])
            mmi5b = mmi(offset=offset/16, length = length, width = width).put(mmi4a.pin['b1'])
            mmi5c = mmi(offset=offset/16, length = length, width = width).put(mmi4b.pin['b0'])
            mmi5d = mmi(offset=offset/16, length = length, width = width).put(mmi4b.pin['b1'])
            mmi5e = mmi(offset=offset/16, length = length, width = width).put(mmi4c.pin['b0'])
            mmi5f = mmi(offset=offset/16, length = length, width = width).put(mmi4c.pin['b1'])
            mmi5g = mmi(offset=offset/16, length = length, width = width).put(mmi4d.pin['b0'])
            mmi5h = mmi(offset=offset/16, length = length, width = width).put(mmi4d.pin['b1'])
            mmi5i = mmi(offset=offset/16, length = length, width = width).put(mmi4e.pin['b0'])
            mmi5k = mmi(offset=offset/16, length = length, width = width).put(mmi4e.pin['b1'])
            mmi5l = mmi(offset=offset/16, length = length, width = width).put(mmi4f.pin['b0'])
            mmi5m = mmi(offset=offset/16, length = length, width = width).put(mmi4f.pin['b1'])
            mmi5n = mmi(offset=offset/16, length = length, width = width).put(mmi4g.pin['b0'])
            mmi5o = mmi(offset=offset/16, length = length, width = width).put(mmi4g.pin['b1'])
            mmi5p = mmi(offset=offset/16, length = length, width = width).put(mmi4h.pin['b0'])
            mmi5q = mmi(offset=offset/16, length = length, width = width).put(mmi4h.pin['b1'])

            nd.Pin('a0', pin=mmi1.pin['a0']).put()
            nd.Pin('b0', pin=mmi5a.pin['b0']).put()
            nd.Pin('b1', pin=mmi5a.pin['b1']).put() 
            nd.Pin('b2', pin=mmi5b.pin['b0']).put()
            nd.Pin('b3', pin=mmi5b.pin['b1']).put()
            nd.Pin('b4', pin=mmi5c.pin['b0']).put() 
            nd.Pin('b5', pin=mmi5c.pin['b1']).put()
            nd.Pin('b6', pin=mmi5d.pin['b0']).put()
            nd.Pin('b7', pin=mmi5d.pin['b1']).put() 
            nd.Pin('b8', pin=mmi5e.pin['b0']).put()
            nd.Pin('b9', pin=mmi5e.pin['b1']).put()
            nd.Pin('b10', pin=mmi5f.pin['b0']).put() 
            nd.Pin('b11', pin=mmi5f.pin['b1']).put()
            nd.Pin('b12', pin=mmi5g.pin['a0']).put()
            nd.Pin('b13', pin=mmi5g.pin['b1']).put()
            nd.Pin('b14', pin=mmi5h.pin['b0']).put() 
            nd.Pin('b15', pin=mmi5h.pin['b1']).put()
            nd.Pin('b16', pin=mmi5i.pin['b0']).put()
            nd.Pin('b17', pin=mmi5i.pin['b1']).put() 
            nd.Pin('b18', pin=mmi5k.pin['b0']).put()
            nd.Pin('b19', pin=mmi5k.pin['b1']).put()
            nd.Pin('b20', pin=mmi5l.pin['b0']).put()
            nd.Pin('b21', pin=mmi5l.pin['b1']).put() 
            nd.Pin('b22', pin=mmi5m.pin['b0']).put()
            nd.Pin('b23', pin=mmi5m.pin['b1']).put()
            nd.Pin('b24', pin=mmi5n.pin['b0']).put() 
            nd.Pin('b25', pin=mmi5n.pin['b1']).put()
            nd.Pin('b26', pin=mmi5o.pin['b0']).put()
            nd.Pin('b27', pin=mmi5o.pin['b1']).put()
            nd.Pin('b28', pin=mmi5p.pin['b0']).put() 
            nd.Pin('b29', pin=mmi5p.pin['b1']).put()
            nd.Pin('b30', pin=mmi5q.pin['b0']).put()
            nd.Pin('b31', pin=mmi5q.pin['b1']).put()
        elif (N==16):
            mmi1  = mmi(offset=offset, length = length, width = width).put()
            mmi2a = mmi(offset=offset/2, length =length, width = width).put(mmi1.pin['b0'])
            mmi2b = mmi(offset=offset/2, length =length, width = width).put(mmi1.pin['b1'])
            mmi3a = mmi(offset=offset/4, length =length, width = width).put(mmi2a.pin['b0'])
            mmi3b = mmi(offset=offset/4, length =length, width = width).put(mmi2a.pin['b1'])
            mmi3c = mmi(offset=offset/4, length =length, width = width).put(mmi2b.pin['b0'])
            mmi3d = mmi(offset=offset/4, length =length, width = width).put(mmi2b.pin['b1'])

            mmi4a = mmi(offset=offset/8, length =length, width = width).put(mmi3a.pin['b0'])
            mmi4b = mmi(offset=offset/8, length =length, width = width).put(mmi3a.pin['b1'])
            mmi4c = mmi(offset=offset/8, length =length, width = width).put(mmi3b.pin['b0'])
            mmi4d = mmi(offset=offset/8, length =length, width = width).put(mmi3b.pin['b1'])
            mmi4e = mmi(offset=offset/8, length =length, width = width).put(mmi3c.pin['b0'])
            mmi4f = mmi(offset=offset/8, length =length, width = width).put(mmi3c.pin['b1'])
            mmi4g = mmi(offset=offset/8, length =length, width = width).put(mmi3d.pin['b0'])
            mmi4h = mmi(offset=offset/8, length =length, width = width).put(mmi3d.pin['b1'])
            nd.Pin('a0', pin=mmi1.pin['a0']).put()
            nd.Pin('b15', pin=mmi4a.pin['b0']).put()
            nd.Pin('b14', pin=mmi4a.pin['b1']).put() 
            nd.Pin('b13', pin=mmi4b.pin['b0']).put()
            nd.Pin('b12', pin=mmi4b.pin['b1']).put()
            nd.Pin('b11', pin=mmi4c.pin['b0']).put() 
            nd.Pin('b10', pin=mmi4c.pin['b1']).put()
            nd.Pin('b9', pin=mmi4d.pin['b0']).put()
            nd.Pin('b8', pin=mmi4d.pin['b1']).put() 
            nd.Pin('b7', pin=mmi4e.pin['b0']).put()
            nd.Pin('b6', pin=mmi4e.pin['b1']).put()
            nd.Pin('b5', pin=mmi4f.pin['b0']).put() 
            nd.Pin('b4', pin=mmi4f.pin['b1']).put()
            nd.Pin('b3', pin=mmi4g.pin['b0']).put()
            nd.Pin('b2', pin=mmi4g.pin['b1']).put()
            nd.Pin('b1', pin=mmi4h.pin['b0']).put() 
            nd.Pin('b0', pin=mmi4h.pin['b1']).put()
    return split_tree

def curve_bend(width, length1, length2, radius):
    with nd.Cell(name='curve') as curve:
        straight1   = WG_route.strt(length= length1, width = width).put()
        bend1       = WG_route.bend(angle = -90, radius = radius, width = width).put(straight1.pin['b0'])
        straight2   = WG_route.strt(length = length2, width = width).put(bend1.pin['b0'])
        nd.Pin('a0', pin=straight1.pin['a0']).put()
        nd.Pin('b0', pin=straight2.pin['b0']).put()
    return curve

def curve_bend_cterclk(width, length1, length2, radius):
    with nd.Cell(name='curve_ctclk') as curve_ctclk:
        straight1   = WG_route.strt(length= length1, width = width).put()
        bend1       = WG_route.bend(angle = 90, radius = radius, width = width).put(straight1.pin['b0'])
        straight2   = WG_route.strt(length = length2, width = width).put(bend1.pin['b0'])
        nd.Pin('a0', pin=straight1.pin['a0']).put()
        nd.Pin('b0', pin=straight2.pin['b0']).put()
    return curve_ctclk

def trombone (length, radius, width):
    # bend(90) - straight - bend(180) - straight - bend(90)
    with nd.Cell(name='trombone') as trombone:
        bend1 = WG_route.bend(angle=-90, radius=radius, width=width).put()
        strt1 = WG_route.strt(length = length, width=width).put(bend1.pin['b0'])
        bend2 = WG_route.bend(angle=180, radius = radius, width=width).put()
        strt2 = WG_route.strt(length = length, width=width).put()
        bend3 = WG_route.bend(angle=-90, radius=radius, width=width).put()
        nd.Pin('a0', pin=bend1.pin['a0']).put()
        nd.Pin('b0', pin=bend3.pin['b0']).put()
    return trombone

@nd.bb_util.hashme('spiral')
def spiral(layer, length, inner_length=0, sep=2):
    """
    Pins - top_in, bot_in, top_out, bot_out
    :return: nazca Cell
    """
    with nd.Cell(hashme=True) as C:
        l=0
        b0=layer.bend(angle=180).put()
        nd.Pin('c0').put(b0.pin['b0'])
        s0=layer.strt(length=inner_length).put('a0', b0.pin['b0'])
        l+=layer.radius*np.pi+inner_length
        b1=layer.bend(angle=-180, radius=2*layer.radius+2*sep, length1=inner_length).put('a0', b0.pin['a0'])
        b2=layer.bend(angle=-180, radius=layer.radius+sep).put('a0', s0.pin['b0'])
        l+=(2*layer.radius+2*sep)*np.pi+(layer.radius+sep)*np.pi+inner_length
        n=1
        while l<length:
            b1=layer.bend(angle=-180, radius=2*layer.radius+2*(n+1)*sep, length1=inner_length).put('a0', b1.pin['b0'])
            b2=layer.bend(angle=-180, radius=2*layer.radius+2*n*sep, length1=inner_length).put('a0', b2.pin['b0'])
            n+=1
            l+=(n*layer.radius+2*(n+1)*sep)*np.pi+(n*layer.radius+2*n*sep)*np.pi+2*inner_length
        b2=layer.bend(angle=-180, radius=2*layer.radius+2*n*sep, length1=inner_length).put('a0', b2.pin['b0'])
        l+=(n*layer.radius+2*n*sep)*np.pi+inner_length
        nd.Pin('a0').put(b1.pin['b0'])
        nd.Pin('b0').put(b2.pin['b0'])
    return C, l


############################## Start of Code ################################

# ================= Parameter ======================= #
N = 16
width_start = 0.1 # laser input width
width_end = 0.3 # target waveguide width
offset_curve = 80      # horizontal offset between 2 adjacent wg
offset = offset_curve*4
width = 0.3     # target wg width
length_laser = 50     # input laser length
radius_curve = 50 
radius_tromb = 50 
length  =   20     # length of the straight portion before the trombones

frame.put(0, 0, 0)
####### laser input - split tree #######
with nd.Cell("16-const-const") as Sixteen_const_const:
    laser1  = laser_input(width = width_start, length = length_laser).put(0,0,-90)
    elm1    = nd.taper(length=5, width1=width_start, width2= width_end).put(laser1.pin['b0'])
    split   = split_tree(N= N ,offset = offset, length=length, width=width).put(elm1.pin['b0'])

    ###### Parameters (Cont) ############

    offset_split = split.pin['b1'].y - split.pin['b0'].y    # vertical offset between wg at the last stage of the split
    offset_cross_split = split.pin['b2'].y - split.pin['b1'].y  # vertical offset between 2 adjacent wg not stemmed from same previous-stage wg
    y_avg = ((split.pin['b0'].y - 2*radius_curve - length - offset_split - (N-1)*offset_curve) + (split.pin['b15'].y - length - 2*radius_curve - N*offset_split))/2# y location of the horizontal mid-point in the array

    distribution = [-6.75,-5.85,-4.95,-4.05,-3.15,-2.25,-1.35,-0.45,0.45, 1.35, 2.25, 3.15, 4.05, 4.95, 5.85, 6.75]
    trace_compensation = np.zeros(N)
    trace_compensation = [0, 74.80797157, 149.61592654, 224.4238898, 299.23185307, 374.03981634, 448.84777961, 507.78006236, 508.43724581, 453.13225083, 378.33185307, 303.5238898, 228.71592654, 153.90796327,  79.1, 4.29203673]
    # distribution of waveguide in the OPA
    length_OPA = 50 # length of the OPA
    trace_array = np.zeros(N) # checking total trace length of the each waveguide.
    to_OPA_space = 200
    for i in range(N):
        nd.trace.trace_start()
        # name of input and output pin i.e 'a0' 'b0' 'a1' 'b1' etc.
        input_pin = "a" + str(i)
        output_pin = "b" + str(i) 
        OPA_y = y_avg + distribution[i] # y-location of OPA array given a distribution
        i = i + 1
        print("Position of waveguide", i)
        curve = curve_bend(width=width, length1=i*offset_curve, length2=length+i*offset_split, radius=radius_curve).put(split.pin[output_pin])
        curve_ctclk = curve_bend_cterclk(width=width, length1=(N-i)*offset_curve, length2=length+(N-i)*offset_curve, radius=radius_curve).put(curve.pin["b0"])
        for j in range(6):
            path_diff = trace_compensation[i-1]
            tromb = trombone(length=path_diff/(12), radius=radius_tromb, width=0.3).put()

        OPA_x = tromb.pin['b0'].x + to_OPA_space
        strt2 = WG_route.strt(length = length_OPA, width =width).put(OPA_x, OPA_y)
        sbend1  = WG_route.sbend_p2p(pin1=tromb.pin['b0'] , pin2=strt2.pin['a0'], radius=(radius_tromb+ np.abs((i-8)*5))).put()

        nd.trace.trace_stop()
        trace_array[i-1] =  nd.trace.trace_length()

with nd.Cell("16-golomb-const") as Sixteen_golomb_const:
    laser1  = laser_input(width = width_start, length = length).put(0,0,-90)
    elm1    = nd.taper(length=5, width1=width_start, width2= width_end).put(laser1.pin['b0'])
    split   = split_tree(N= N ,offset = offset, length=length, width=width).put(elm1.pin['b0'])

    ###### Parameters (Cont) ############

    offset_split = split.pin['b1'].y - split.pin['b0'].y    # vertical offset between wg at the last stage of the split
    offset_cross_split = split.pin['b2'].y - split.pin['b1'].y  # vertical offset between 2 adjacent wg not stemmed from same previous-stage wg
    y_avg = ((split.pin['b0'].y -2*radius_curve-offset_split-(N-1)*offset_curve) + (split.pin['b15'].y-2*radius_curve-16*offset_split))/2# y location of the horizontal mid-point in the array
    length=20     # length of the straight portion before the trombones
    distribution = [-73.01252, -72.1125,-69.4125, -63.1125,	-49.6125, -44.2125,	-22.6125, -11.8125,	-4.6125, 30.4875, 32.2875, 47.5875,	61.9875, 73.6875, 78.1875, 86.2875]
    trace_compensation = np.zeros(N)
    trace_compensation = [0, 74.80794327, 147.81590654, 217.2238698, 279.43183307, 349.73979634, 403.84775961, 456.93944267, 468.33853396, 446.4995239, 382.10683307, 321.6988698, 260.39090654, 196.38294327, 125.17498, 57.56701673]
    # distribution of waveguide in the OPA
    length_OPA = 50 # length of the OPA
    trace_array = np.zeros(N) # checking total trace length of the each waveguide.
    to_OPA_space = 200
    for i in range(N):
        nd.trace.trace_start()
        # name of input and output pin i.e 'a0' 'b0' 'a1' 'b1' etc.
        input_pin = "a" + str(i)
        output_pin = "b" + str(i) 
        OPA_y = y_avg + distribution[i] # y-location of OPA array given a distribution
        i = i + 1
        print("Position of waveguide", i)
        curve = curve_bend(width=width, length1=i*offset_curve, length2=length+i*offset_split, radius=radius_curve).put(split.pin[output_pin])
        curve_ctclk = curve_bend_cterclk(width=width, length1=(N-i)*offset_curve, length2=length+(N-i)*offset_curve, radius=radius_curve).put(curve.pin["b0"])
        for j in range(6):
            path_diff = trace_compensation[i-1]
            tromb = trombone(length=path_diff/(12), radius=radius_tromb, width=0.3).put()

        OPA_x = tromb.pin['b0'].x + to_OPA_space
        strt2 = WG_route.strt(length = length_OPA, width =width).put(OPA_x, OPA_y)
        sbend1  = WG_route.sbend_p2p(pin1=tromb.pin['b0'] , pin2=strt2.pin['a0'], radius=(radius_tromb+ np.abs((i-8)*5))).put()

        nd.trace.trace_stop()
        trace_array[i-1] =  nd.trace.trace_length()

# with nd.Cell('TOP') as TOP:
#     frame.put(0, 0, 0)
#     Sixteen_const_const.put(0, 0,0)
Sixteen_const_const. put(1000,8000,0)
Sixteen_golomb_const.put(1000,6000,0)
print("end wg width", width)
print("trace length of waveguides: ", trace_array)
print("difference trace length of waveguides: ", np.abs(trace_array-np.max(trace_array)))
print("Offset split: ", offset_split)
print("Offset cross split", offset_cross_split)
nd.export_gds( filename="constant-design.gds")


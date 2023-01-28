'''
RACER-AIMChip_Layout.py
Hector Rubio
Stefan Preble
RIT Integrated Photonics
Started: August 22, 2022

TODO:

RACER-AIM chip for sensor and laser interface to MCU/CPU.
'''
import numpy as np
import nazca as nd
import AIMPhotonics.RIT_Pcells as ritpcells
from AIMPhotonics.RIT_route_utils import Connector

# show all the BBs and layers and xsections
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

with nd.Cell('Splitter') as spl:
    WG_route.sbend().put()
    WG_route.sbend().put('a0', flop=True)

    spl.default_pins('opt1')
    nd.Pin('opt1', xs='SIN Waveguide', width=Minimum_Width).put((0.000, 0.000, 180))
    nd.Pin('opt2', xs='SIN Waveguide', width=Minimum_Width).put((0.000, 40.000, 180))
    nd.Pin('opt3', xs='SIN Waveguide', width=Minimum_Width).put((60.000, 20.000, 0))
    nd.put_stub(length=0)

with nd.Cell('Metal_Pad') as metalpad:
    Metal_layer.strt(length=80, width=80).put(0, 0, 0)
    ContactCut.strt(length=70, width=70).put(5, 0, 0)

    nd.Pin('North', xs='Top Metal', width=Minimum_Width).put((40.000, 40.000, 90))
    nd.Pin('South', xs='Top Metal', width=Minimum_Width).put((40.000, -40.000, 270))
    nd.Pin('East', xs='Top Metal', width=Minimum_Width).put((0.000, 0.000, 180))
    nd.Pin('West', xs='Top Metal', width=Minimum_Width).put((80.000, 0.000, 0))
    nd.put_stub(length=0)

"""
    Splitting Trees
"""
with nd.Cell('SplittingTree4') as SplittingTree4:
    FirstSpl = spl.put(0, 0, 180)
    SecondSpl = [spl.put(180, -120+240*i, 180) for i in range(2)]
    WG_route.sbend_p2p(pin1=FirstSpl.pin['opt1'], pin2=SecondSpl[1].pin['opt3']).put()
    WG_route.sbend_p2p(pin1=FirstSpl.pin['opt2'], pin2=SecondSpl[0].pin['opt3']).put()

    FirstSpl.raise_pins(['opt3'], ['in'])
    [SecondSpl[i].raise_pins(['opt1'], ['SplTree_4_{:}'.format(2*i)]) for i in range(2)]
    [SecondSpl[i].raise_pins(['opt2'], ['SplTree_4_{:}'.format(2*i+1)]) for i in range(2)]

with nd.Cell('SplittingTree8') as SplittingTree8:
    FirstSpl = spl.put(0, 120, 180)
    SecondSpl = [spl.put(180, -120+480*i, 180) for i in range(2)]
    WG_route.sbend_p2p(pin1=FirstSpl.pin['opt1'], pin2=SecondSpl[1].pin['opt3']).put()
    WG_route.sbend_p2p(pin1=FirstSpl.pin['opt2'], pin2=SecondSpl[0].pin['opt3']).put()

    ThirdSpl = [spl.put(360, -240+240*i, 180) for i in range(4)]
    WG_route.sbend_p2p(pin1=SecondSpl[0].pin['opt1'], pin2=ThirdSpl[1].pin['opt3']).put()
    WG_route.sbend_p2p(pin1=SecondSpl[1].pin['opt1'], pin2=ThirdSpl[3].pin['opt3']).put()
    WG_route.sbend_p2p(pin1=SecondSpl[0].pin['opt2'], pin2=ThirdSpl[0].pin['opt3']).put()
    WG_route.sbend_p2p(pin1=SecondSpl[1].pin['opt2'], pin2=ThirdSpl[2].pin['opt3']).put()

    FirstSpl.raise_pins(['opt3'], ['in'])
    [ThirdSpl[i].raise_pins(['opt1'], ['SplTree_8_{:}'.format(2*i)]) for i in range(4)]
    [ThirdSpl[i].raise_pins(['opt2'], ['SplTree_8_{:}'.format(2*i+1)]) for i in range(4)]

with nd.Cell('SplittingTree16') as SplittingTree16:
    FirstSpl = spl.put(0, 480, 180)
    SecondSpl = [spl.put(180, 960*i, 180) for i in range(2)]
    WG_route.sbend_p2p(pin1=FirstSpl.pin['opt1'], pin2=SecondSpl[1].pin['opt3']).put()
    WG_route.sbend_p2p(pin1=FirstSpl.pin['opt2'], pin2=SecondSpl[0].pin['opt3']).put()

    ThirdSpl = [spl.put(360, -240+480*i, 180) for i in range(4)]
    WG_route.sbend_p2p(pin1=SecondSpl[0].pin['opt1'], pin2=ThirdSpl[1].pin['opt3']).put()
    WG_route.sbend_p2p(pin1=SecondSpl[1].pin['opt1'], pin2=ThirdSpl[3].pin['opt3']).put()
    WG_route.sbend_p2p(pin1=SecondSpl[0].pin['opt2'], pin2=ThirdSpl[0].pin['opt3']).put()
    WG_route.sbend_p2p(pin1=SecondSpl[1].pin['opt2'], pin2=ThirdSpl[2].pin['opt3']).put()

    FourthSpl = [spl.put(540, -360+240*i, 180) for i in range(8)]
    WG_route.sbend_p2p(pin1=ThirdSpl[0].pin['opt1'], pin2=FourthSpl[1].pin['opt3']).put()
    WG_route.sbend_p2p(pin1=ThirdSpl[1].pin['opt1'], pin2=FourthSpl[3].pin['opt3']).put()
    WG_route.sbend_p2p(pin1=ThirdSpl[0].pin['opt2'], pin2=FourthSpl[0].pin['opt3']).put()
    WG_route.sbend_p2p(pin1=ThirdSpl[1].pin['opt2'], pin2=FourthSpl[2].pin['opt3']).put()

    WG_route.sbend_p2p(pin1=ThirdSpl[2].pin['opt1'], pin2=FourthSpl[5].pin['opt3']).put()
    WG_route.sbend_p2p(pin1=ThirdSpl[3].pin['opt1'], pin2=FourthSpl[7].pin['opt3']).put()
    WG_route.sbend_p2p(pin1=ThirdSpl[2].pin['opt2'], pin2=FourthSpl[4].pin['opt3']).put()
    WG_route.sbend_p2p(pin1=ThirdSpl[3].pin['opt2'], pin2=FourthSpl[6].pin['opt3']).put()

    FirstSpl.raise_pins(['opt3'], ['in'])
    [FourthSpl[i].raise_pins(['opt1'], ['SplTree_16_{:}'.format(2*i)]) for i in range(8)]
    [FourthSpl[i].raise_pins(['opt2'], ['SplTree_16_{:}'.format(2*i+1)]) for i in range(8)]

"""
    Thermo-Optic Phase Shifter
"""
with nd.Cell('PhaseShifter') as thermal_phaseshifter:
    wg = ritpcells.wg_spiral(radius=50,
                             num_bends_per_turn=5,
                             inside_wg_length=1,
                             wg_separation=10,
                             wg_width=0.3,
                             interconnect=WG_route,
                             trace=True).put(0, 0, 0)

    Metal_route.strt(length=220).put(145, -75, 90)
    for i in range(7):
        Metal_route.bend(radius=10, angle=180).put('a0')
        Metal_route.strt(length=200).put('a0')
        Metal_route.bend(radius=10, angle=-180).put('a0')
        Metal_route.strt(length=200).put('a0')
    Metal_route.strt(length=20).put('a0')

    wg.raise_pins(['in'], ['opt_in'])
    wg.raise_pins(['out'], ['opt_out'])

"""
    Edge Coupler
"""
with nd.Cell('EdgeCoupler') as edgecoupler:
    WG_route.strt(length=10, width=0.1).put(0, 0, 0)
    WG_route.taper(length=100, width1=0.1, width2=0.3).put()

    nd.Pin('opt', xs='SIN Waveguide', width=Minimum_Width).put((110.000, 0.000, 0))
    nd.put_stub(length=0)

"""
    Frame
"""
with nd.Cell('9x9_Frame') as frame:
    Frame1.strt(width=9000, length=9000).put(0, 4500, 0)

    Frame2.strt(width=200, length=8880+300).put(-100, 0, 0)
    Frame2.strt(width=200, length=8880+200).put(8880+100, 0, 90)

    Frame2.strt(width=200, length=8880+100).put(0, 8880+50, 270)
    Frame2.strt(width=200, length=8880+300).put(-100, 8980, 0)

"""
    I/O pins
"""
with nd.Cell('IO_pins') as IO_Pins:
    MetalPads = [metalpad.put(300+150*i, 400, 0).raise_pins(['North'], ['Pad_{:}'.format(i)]) for i in range(54)]


"""
    4-splitter design
"""
with nd.Cell('4-Splitter') as FourSplit:
    SplTree = SplittingTree4.put(200, 0, 0)
    PS = [[thermal_phaseshifter.put(600+400*i, -400+1100*j, 270, flip=True) for i in range(2)] if j == 0 else
          [thermal_phaseshifter.put(600+400*i, -700+1100*j, 90) for i in range(2)]
          for j in range(2)]

    WG_route.strt_bend_strt_p2p(pin1=SplTree.pin['SplTree_4_1'], pin2=PS[0][0].pin['opt_in']).put()
    WG_route.strt_bend_strt_p2p(pin1=SplTree.pin['SplTree_4_0'], pin2=PS[0][1].pin['opt_in']).put()

    WG_route.strt_bend_strt_p2p(pin1=SplTree.pin['SplTree_4_2'], pin2=PS[1][0].pin['opt_in']).put()
    WG_route.strt_bend_strt_p2p(pin1=SplTree.pin['SplTree_4_3'], pin2=PS[1][1].pin['opt_in']).put()

    """
        Variable Termination for beam steering
    """
    with nd.Cell('VariableTermination') as variable_termination:
        WidthList = [2, 4, 6, 8]
        DeltaList = [0, 10, 20, 10]

        accum = 0
        for i in range(len(WidthList)):
            accum = accum + DeltaList[i] + WidthList[i]
            print(list(range(i, i - len(WidthList), -1)))
            for j in range(i, i - len(WidthList), -1):
                if j == i:
                    WG_route.strt(length=IndivLength, width=WidthList[j]).put(0, accum, 0)
                    WG_route.taper(length=IndivLength, width1=WidthList[j], width2=0.3).put('a0')
                    WG_route.strt(length=IndivLength, width=0.3).put('a0')
                    WG_route.taper(length=IndivLength, width2=WidthList[j - 1], width1=0.3).put('a0')
                elif j == i - len(WidthList) + 1:
                    WG_route.taper(length=IndivLength, width1=WidthList[j], width2=0.3).put('a0')
                    WG_route.strt(length=IndivLength, width=0.3).put('a0').raise_pins(['b0'], ['P_{:}'.format(i)])
                else:
                    WG_route.taper(length=IndivLength, width1=WidthList[j], width2=0.3).put('a0')
                    WG_route.strt(length=IndivLength, width=0.3).put('a0')
                    WG_route.taper(length=IndivLength, width2=WidthList[j - 1], width1=0.3).put('a0')

    VT = variable_termination.put(1500, -40, 0, flop=True)

    WG_route.strt_bend_strt_p2p(pin1=PS[1][1].pin['opt_out'], pin2=VT.pin['P_2']).put()
    WG_route.strt_bend_strt_p2p(pin1=PS[0][1].pin['opt_out'], pin2=VT.pin['P_1']).put()

    instructions = ['bend', 60, 180, Minimum_Width,
                    'strt', 250, Minimum_Width,
                    'bend', 50, -90, Minimum_Width,
                    'strt', 250, Minimum_Width,
                    ]
    Connector(pin1=PS[1][0].pin['opt_out'],
              pin2=VT.pin['P_3'],
              instructions=instructions,
              interconnect=WG_route,
              final_route_style='sbend_p2p').route()

    instructions = ['bend', 60, -180, Minimum_Width,
                    'strt', 250, Minimum_Width,
                    'bend', 50, 90, Minimum_Width,
                    'strt', 250, Minimum_Width,
                    ]
    Connector(pin1=PS[0][0].pin['opt_out'],
              pin2=VT.pin['P_0'],
              instructions=instructions,
              interconnect=WG_route,
              final_route_style='sbend_p2p').route()


"""
    8-splitter design
"""
with nd.Cell('8-Splitter') as EightSplit:
    SplTree = SplittingTree8.put(200, 0, 0)
    PS = [[thermal_phaseshifter.put(800+400*i, -600+1100*j, 270, flip=True) for i in range(4)] if j == 0 else
          [thermal_phaseshifter.put(800+400*i, -300+1100*j, 90) for i in range(4)]
          for j in range(2)]

    WG_route.strt_bend_strt_p2p(pin1=SplTree.pin['SplTree_8_1'], pin2=PS[0][0].pin['opt_in']).put()
    WG_route.strt_bend_strt_p2p(pin1=SplTree.pin['SplTree_8_0'], pin2=PS[0][1].pin['opt_in']).put()

    WG_route.strt_bend_strt_p2p(pin1=SplTree.pin['SplTree_8_2'], pin2=PS[0][3].pin['opt_in']).put()
    WG_route.strt_bend_strt_p2p(pin1=SplTree.pin['SplTree_8_3'], pin2=PS[0][2].pin['opt_in']).put()

    WG_route.strt_bend_strt_p2p(pin1=SplTree.pin['SplTree_8_4'], pin2=PS[1][2].pin['opt_in']).put()
    WG_route.strt_bend_strt_p2p(pin1=SplTree.pin['SplTree_8_5'], pin2=PS[1][3].pin['opt_in']).put()

    WG_route.strt_bend_strt_p2p(pin1=SplTree.pin['SplTree_8_6'], pin2=PS[1][0].pin['opt_in']).put()
    WG_route.strt_bend_strt_p2p(pin1=SplTree.pin['SplTree_8_7'], pin2=PS[1][1].pin['opt_in']).put()


    """
        Variable Termination for beam steering
    """
    with nd.Cell('VariableTermination') as variable_termination:
        WidthList = [2, 4, 6, 8, 10, 12, 14, 16]
        DeltaList = [0, 10, 20, 10, 30, 60, 80, 90]

        accum = 0
        for i in range(len(WidthList)):
            accum = accum + DeltaList[i] + WidthList[i]
            print(list(range(i, i - len(WidthList), -1)))
            for j in range(i, i - len(WidthList), -1):
                if j == i:
                    WG_route.strt(length=IndivLength, width=WidthList[j]).put(0, accum, 0)
                    WG_route.taper(length=IndivLength, width1=WidthList[j], width2=0.3).put('a0')
                    WG_route.strt(length=IndivLength, width=0.3).put('a0')
                    WG_route.taper(length=IndivLength, width2=WidthList[j - 1], width1=0.3).put('a0')
                elif j == i - len(WidthList) + 1:
                    WG_route.taper(length=IndivLength, width1=WidthList[j], width2=0.3).put('a0')
                    WG_route.strt(length=IndivLength, width=0.3).put('a0').raise_pins(['b0'], ['P_{:}'.format(i)])
                else:
                    WG_route.taper(length=IndivLength, width1=WidthList[j], width2=0.3).put('a0')
                    WG_route.strt(length=IndivLength, width=0.3).put('a0')
                    WG_route.taper(length=IndivLength, width2=WidthList[j - 1], width1=0.3).put('a0')
    VT = variable_termination.put(3000, -40, 0, flop=True)

    instructions = ['bend', 60, 180, Minimum_Width,
                    'strt', 250, Minimum_Width,
                    'bend', 50, -90, Minimum_Width,
                    'strt', 1250, Minimum_Width,
                    ]
    Connector(pin1=PS[1][0].pin['opt_out'],
              pin2=VT.pin['P_7'],
              instructions=instructions,
              interconnect=WG_route,
              final_route_style='sbend_p2p').route()

    instructions = ['bend', 60, -180, Minimum_Width,
                    'strt', 250, Minimum_Width,
                    'bend', 50, 90, Minimum_Width,
                    'strt', 1250, Minimum_Width,
                    ]
    Connector(pin1=PS[0][0].pin['opt_out'],
              pin2=VT.pin['P_0'],
              instructions=instructions,
              interconnect=WG_route,
              final_route_style='sbend_p2p').route()


"""
    16-splitter design
"""
with nd.Cell('16-splitter') as SixteenSplit:
    SplTree = SplittingTree16.put(200, 0, 0)
    PS = [[thermal_phaseshifter.put(1100+400*i, -800+1100*j, 270, flip=True) for i in range(8)] if j == 0 else
          [thermal_phaseshifter.put(1100+400*i, 500+1100*j, 90) for i in range(8)]
          for j in range(2)]

    WG_route.strt_bend_strt_p2p(pin1=SplTree.pin['SplTree_16_1'], pin2=PS[0][0].pin['opt_in']).put()
    WG_route.strt_bend_strt_p2p(pin1=SplTree.pin['SplTree_16_0'], pin2=PS[0][1].pin['opt_in']).put()

    WG_route.strt_bend_strt_p2p(pin1=SplTree.pin['SplTree_16_2'], pin2=PS[0][3].pin['opt_in']).put()
    WG_route.strt_bend_strt_p2p(pin1=SplTree.pin['SplTree_16_3'], pin2=PS[0][2].pin['opt_in']).put()

    WG_route.strt_bend_strt_p2p(pin1=SplTree.pin['SplTree_16_4'], pin2=PS[0][5].pin['opt_in']).put()
    WG_route.strt_bend_strt_p2p(pin1=SplTree.pin['SplTree_16_5'], pin2=PS[0][4].pin['opt_in']).put()

    WG_route.strt_bend_strt_p2p(pin1=SplTree.pin['SplTree_16_6'], pin2=PS[0][7].pin['opt_in']).put()
    WG_route.strt_bend_strt_p2p(pin1=SplTree.pin['SplTree_16_7'], pin2=PS[0][6].pin['opt_in']).put()

    WG_route.strt_bend_strt_p2p(pin1=SplTree.pin['SplTree_16_8'], pin2=PS[1][6].pin['opt_in']).put()
    WG_route.strt_bend_strt_p2p(pin1=SplTree.pin['SplTree_16_9'], pin2=PS[1][7].pin['opt_in']).put()

    WG_route.strt_bend_strt_p2p(pin1=SplTree.pin['SplTree_16_10'], pin2=PS[1][4].pin['opt_in']).put()
    WG_route.strt_bend_strt_p2p(pin1=SplTree.pin['SplTree_16_11'], pin2=PS[1][5].pin['opt_in']).put()

    WG_route.strt_bend_strt_p2p(pin1=SplTree.pin['SplTree_16_12'], pin2=PS[1][2].pin['opt_in']).put()
    WG_route.strt_bend_strt_p2p(pin1=SplTree.pin['SplTree_16_13'], pin2=PS[1][3].pin['opt_in']).put()

    WG_route.strt_bend_strt_p2p(pin1=SplTree.pin['SplTree_16_14'], pin2=PS[1][0].pin['opt_in']).put()
    WG_route.strt_bend_strt_p2p(pin1=SplTree.pin['SplTree_16_15'], pin2=PS[1][1].pin['opt_in']).put()


    """
        Variable Termination for beam steering
    """
    with nd.Cell('VariableTermination') as variable_termination:
        WidthList = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32]
        DeltaList = [0, 10, 20, 10, 30, 60, 80, 90, 10, 10, 10, 1, 6, 8, 2, 1]

        accum = 0
        for i in range(len(WidthList)):
            accum = accum + DeltaList[i] + WidthList[i]
            print(list(range(i, i - len(WidthList), -1)))
            for j in range(i, i - len(WidthList), -1):
                if j == i:
                    WG_route.strt(length=IndivLength, width=WidthList[j]).put(0, accum, 0)
                    WG_route.taper(length=IndivLength, width1=WidthList[j], width2=0.3).put('a0')
                    WG_route.strt(length=IndivLength, width=0.3).put('a0')
                    WG_route.taper(length=IndivLength, width2=WidthList[j - 1], width1=0.3).put('a0')
                elif j == i - len(WidthList) + 1:
                    WG_route.taper(length=IndivLength, width1=WidthList[j], width2=0.3).put('a0')
                    WG_route.strt(length=IndivLength, width=0.3).put('a0').raise_pins(['b0'], ['P_{:}'.format(i)])
                else:
                    WG_route.taper(length=IndivLength, width1=WidthList[j], width2=0.3).put('a0')
                    WG_route.strt(length=IndivLength, width=0.3).put('a0')
                    WG_route.taper(length=IndivLength, width2=WidthList[j - 1], width1=0.3).put('a0')
    VT = variable_termination.put(6000, 100, 0, flop=True)

    # instructions = ['bend', 60, 180, Minimum_Width,
    #                 'strt', 250, Minimum_Width,
    #                 'bend', 50, -90, Minimum_Width,
    #                 'strt', 1250, Minimum_Width,
    #                 ]
    # Connector(pin1=PS[1][0].pin['opt_out'],
    #           pin2=VT.pin['P_7'],
    #           instructions=instructions,
    #           interconnect=WG_route,
    #           final_route_style='sbend_p2p').route()
    #
    # instructions = ['bend', 60, -180, Minimum_Width,
    #                 'strt', 250, Minimum_Width,
    #                 'bend', 50, 90, Minimum_Width,
    #                 'strt', 1250, Minimum_Width,
    #                 ]
    # Connector(pin1=PS[0][0].pin['opt_out'],
    #           pin2=VT.pin['P_0'],
    #           instructions=instructions,
    #           interconnect=WG_route,
    #           final_route_style='sbend_p2p').route()


with nd.Cell('TOP') as TOP:
    frame.put(0, 0, 0)
    IO_Pins.put(0, 0, 0)
    FourSplit.put(400, 2000, 0)
    EightSplit.put(1500, 4000, 0)
    SixteenSplit.put(3000, 6500, 0)

# Export GDS
nd.export_gds(topcells=[TOP], filename='2023_SiN_PhaseArray.gds')

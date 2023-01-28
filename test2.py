# create multiple instance from a mask
# concatenate instances from pins


import nazca as nd
import nazca.demofab as demo

with nd.Cell(name='myMMI') as mmi:
    mmi1 = demo.mmi1x2_sh().put()
    elm1 = demo.shallow.strt(length=50).put(mmi1.pin['a0'])
    elm2 = demo.shallow.sbend(offset=40).put(mmi1.pin['b0'])
    elm3 = demo.shallow.sbend(offset=-40).put(mmi1.pin['b1'])

    nd.Pin('a0', pin=elm1.pin['b0']).put()
    nd.Pin('b0', pin=elm2.pin['b0']).put()
    nd.Pin('b1', pin=elm3.pin['b0']).put()

mmi.put('a0', 0) # same as mmi.put(0), 'a0' is the default.
mmi.put('b0', 0, 100) # connect pin 'b0' of 'mmi' at (0, 100)

nd.export_plt()
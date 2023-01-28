"Adam Ignaciuk for Photonic integrated circuits"
"Submitted 12/09/2022"
""



import nazca as nd
import nazca.geometries as shape
import nazca.demofab as demo
import nazca.interconnects as IC


cell_length = 3500
cell_width = 2500
DC_pads_count = 36
DC_pads_offset = 400
Optical_outputs_offset = 600

scale_factor = 3.0
location_a = 403.113
where_mmi_x = 520
where_mmi_y = 1000
where_laser_x = 1820

def dbr_laser(Ldbr1=50, Ldbr2=500, Lsoa=750, Lpm=70):
    """Create a parametrized dbr laser building block."""
    with nd.Cell(name='laser') as laser:
        #create an isolation cell for reuse
        iso = demo.isolation_act(length=20)

        #draw the laser
        s2a   = demo.s2a().put(0)
        dbr1  = demo.dbr(length=Ldbr1).put()
        iso.put()
        soa   = demo.soa(length=Lsoa).put()
        iso.put()
        phase = demo.phase_shifter(length=Lpm).put()
        iso.put()
        dbr2  = demo.dbr(length=Ldbr2).put()
        a2s   = demo.a2s().put()

        # add pins to the laser building block
        nd.Pin('a0', pin=s2a.pin['a0']).put()
        nd.Pin('b0', pin=a2s.pin['b0']).put()
        nd.Pin('c0', pin=dbr1.pin['c0']).put()
        nd.Pin('c1', pin=soa.pin['c0']).put()
        nd.Pin('c2', pin=phase.pin['c0']).put()
        nd.Pin('c3', pin=dbr2.pin['c0']).put()
    return laser

with nd.Cell(name='Chip_template') as Chip_template:
    # Define cell boundaries
    boundaries = nd.Polygon(layer=7, points=shape.frame(sizew=200, sizel=cell_length + 200, sizeh=cell_width + 200, grow=0))
    boundaries.put()

    # load GDS BB
    mmi = nd.load_gds(
        filename='./NazcaPIC-main/AWG_template.gds',
    )
    mmi.put(where_mmi_x,where_mmi_y,0)
    # Add Pins
    nd.Pin('a0', width=2).put(where_mmi_x, -187.1 * scale_factor+where_mmi_y, 180)
    nd.Pin('b0', width=2).put(location_a*scale_factor+where_mmi_x, -257.089 * scale_factor+where_mmi_y, 0)
    nd.Pin('b1', width=2).put(location_a*scale_factor+where_mmi_x, -247.089 * scale_factor+where_mmi_y, 0)
    nd.Pin('b2', width=2).put(location_a*scale_factor+where_mmi_x, -237.089 * scale_factor+where_mmi_y, 0)
    nd.Pin('b3', width=2).put(location_a*scale_factor+where_mmi_x, -227.089 * scale_factor+where_mmi_y, 0)
    nd.Pin('b4', width=2).put(location_a*scale_factor+where_mmi_x, -217.089 * scale_factor+where_mmi_y, 0)
    nd.Pin('b5', width=2).put(location_a*scale_factor+where_mmi_x, -207.089 * scale_factor+where_mmi_y, 0)
    nd.Pin('b6', width=2).put(location_a*scale_factor+where_mmi_x, -197.089 * scale_factor+where_mmi_y, 0)
    nd.Pin('b7', width=2).put(location_a*scale_factor+where_mmi_x, -187.089 * scale_factor+where_mmi_y, 0)

    # Put stubs
    nd.put_stub()
    laser1 = dbr_laser(Lsoa=750).put(where_laser_x, -257.089 * scale_factor+where_mmi_y)
    laser2 = dbr_laser(Lsoa=750).put(where_laser_x, -247.089 * scale_factor + where_mmi_y)
    laser3 = dbr_laser(Lsoa=750).put(where_laser_x, -237.089 * scale_factor+where_mmi_y)
    laser4 = dbr_laser(Lsoa=750).put(where_laser_x, -227.089 * scale_factor+where_mmi_y)
    laser5 = dbr_laser(Lsoa=750).put(where_laser_x, -217.089 * scale_factor+where_mmi_y)
    laser6 = dbr_laser(Lsoa=750).put(where_laser_x, -207.089 * scale_factor+where_mmi_y)
    laser7 = dbr_laser(Lsoa=750).put(where_laser_x, -197.089 * scale_factor+where_mmi_y)
    laser8 = dbr_laser(Lsoa=750).put(where_laser_x, -187.089 * scale_factor+where_mmi_y)
    # Put boundary around the mmi bb
    #nd.put_boundingbox('org', length=403.113 * scale_factor, width=540.0 * scale_factor)

    ic1 = IC.Interconnect(width=2.0, radius=20)
    ic1.strt(length=(where_laser_x-where_mmi_x)/4).put(location_a*scale_factor+where_mmi_x,
                                                       -257.089*scale_factor+where_mmi_y, 0)
    ic2 = IC.Interconnect(width=2.0, radius=20)
    ic2.strt(length=(where_laser_x - where_mmi_x) / 4).put(location_a * scale_factor + where_mmi_x,
                                                        -247.089 * scale_factor + where_mmi_y, 0)
    ic3 = IC.Interconnect(width=2.0, radius=20)
    ic3.strt(length=(where_laser_x - where_mmi_x) / 4).put(location_a * scale_factor + where_mmi_x,
                                                        -237.089 * scale_factor + where_mmi_y, 0)
    ic4 = IC.Interconnect(width=2.0, radius=20)
    ic4.strt(length=(where_laser_x - where_mmi_x) / 4).put(location_a * scale_factor + where_mmi_x,
                                                        -227.089 * scale_factor + where_mmi_y, 0)
    ic5 = IC.Interconnect(width=2.0, radius=20)
    ic5.strt(length=(where_laser_x - where_mmi_x) / 4).put(location_a * scale_factor + where_mmi_x,
                                                        -217.089 * scale_factor + where_mmi_y, 0)
    ic6 = IC.Interconnect(width=2.0, radius=20)
    ic6.strt(length=(where_laser_x - where_mmi_x) / 4).put(location_a * scale_factor + where_mmi_x,
                                                        -207.089 * scale_factor + where_mmi_y, 0)
    ic7 = IC.Interconnect(width=2.0, radius=20)
    ic7.strt(length=(where_laser_x - where_mmi_x) / 4).put(location_a * scale_factor + where_mmi_x,
                                                        -197.089 * scale_factor + where_mmi_y, 0)
    ic8 = IC.Interconnect(width=2.0, radius=20)
    ic8.strt(length=(where_laser_x - where_mmi_x) / 4).put(location_a * scale_factor + where_mmi_x,
                                                        -187.089 * scale_factor + where_mmi_y, 0)


    Optical_pad = demo.shallow.strt(length=250).put(0, -187.1 * scale_factor+where_mmi_y ,0)
    nd.Pin(str('Optical_OUT_{0}'), width=2 ).put(Optical_pad.pin['b0'])
    nd.put_stub()

    ic0 = IC.Interconnect(width=2.0, radius=20)
    ic0.strt(length=(where_mmi_x) / 1.9).put(where_mmi_x-270,-187.1 * scale_factor+where_mmi_y,0)


nd.text('Adams Chip', height=500, align='cc', layer=2).put(cell_length/2-400, cell_width-800)

Chip_template.put(0,0)


nd.export_plt()
#nd.export_gds(filename='Created/Adams Chip')





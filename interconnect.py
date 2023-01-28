import nazca as nd
import nazca.interconnects as IC

ic1 = IC.Interconnect(width=2.0, radius=20)
ic2 = IC.Interconnect(width=1.0, radius=50)

# use the interconnect objects to create layout:
ic1.strt(length=10).put(0)
ic1.bend(angle=45).put()

ic2.strt(length=20).put(20)
ic2.bend(angle=45).put()

nd.export_plt()
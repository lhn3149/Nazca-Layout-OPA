import nazca as nd
print(nd.__version__)


nd.strt(length=20).put()
nd.bend(angle=90).put()
nd.bend(angle=-180).put()
nd.strt(length=10).put()

nd.export_plt()
from atomicplot2.data import XYDataObject
from atomicplot2.plot import MatPlot


d = XYDataObject([1,2,3], [4,5,6])
mp = MatPlot()

mp += d

d.plot.updated = True
d.plot.updated = True

print(d.plot._y_dict)
print(d.plot._x_dict)

d.plot.norm = True

print(d.plot._y_dict)
print(d.plot._x_dict)

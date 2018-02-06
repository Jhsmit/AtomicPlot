import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes, SubplotBase
from matplotlib.axes import subplot_class_factory


fig, axes = plt.subplots()

fake_cls = subplot_class_factory()
print(type(fake_cls))
print(fake_cls)



#
# print(type(fig))
# print(type(axes))
#
# print('super")')
# print(super(axes))
# print(Axes.mro())
# #print(axes.__bases__())
# print(axes.mro())
# print(type(Axes) in Axes.mro())

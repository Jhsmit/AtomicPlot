__author__ = 'Smit'
import numpy as np

import seaborn as sns
import os


from collections import OrderedDict
import operator
from atom.api import Atom, Dict, Str, Typed, Float, Event, List

from itertools import repeat
from .base import UpdateArray
from atomicplot2.plot import Plot1D
from atomicplot2.fit import Fit1D


# todo allow subslicing of dataset and dataobjects
# todo create general api thing to do operations on list in dataset (isnt that a for loop)


class DataBase(Atom):
    """ base class for all objects holding data, DataObject and DataSet. Not to be confused with a database.
    """

    metadata = Dict # todo special metadata dict? what did i mean with this?

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class DataObjectBase(DataBase):
    """Base class for DataObjects. Provides core functionality such as arithmetic operators
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __sub__(self, other):
        return self.operate(other, operator.sub, self.func_op)

    def __add__(self, other):
        return self.operate(other, operator.add, self.func_op)

    def __mul__(self, other):
        return self.operate(other, operator.mul, self.func_op)

    def __truediv__(self, other):
        return self.operate(other, operator.truediv, self.func_op)

    def __floordiv__(self, other):
        return self.operate(other, operator.floordiv, self.func_op)

    def __pow__(self, power, modulo=None):
        if modulo is not None:
            return XYDataObject(self.x, pow(self.y, power, modulo))  # todo add test for this
        else:
            return self.operate(power, operator.pow, self.func_op)

    def __neg__(self):
        return XYDataObject(self.x, -self.y)

    def __abs__(self):
        return XYDataObject(self.x, np.absolute(self.y))

    def __isub__(self, other):
        return self.operate(other, operator.sub, self.func_iop)

    def __iadd__(self, other):
        return self.operate(other, operator.add, self.func_iop)

    def __imul__(self, other):
        return self.operate(other, operator.mul, self.func_iop)

    def __itruediv__(self, other):
    # todo WARNING: numpy division rules are applied. Dividing array of ints gives floored result
        return self.operate(other, operator.truediv, self.func_iop)

    def __ifloordiv__(self, other):
        return self.operate(other, operator.floordiv, self.func_iop)

    def __ipow__(self, other):
        return self.operate(other, operator.pow, self.func_iop)

    def operate(self, other, op, func):
        try:
            y = other.y
            assert np.array_equal(self.x, other.x) or ValueError('Unequal x arrays')
        except AttributeError:
            y = other

        return func(self.x, op(self.y, y))

    def func_iop(self, x, y): #kwargs?
        self.y = y  # This can be done sexier by using internal operators, but that wont trigger traits
        return self

    def func_op(self, x, y):
        return XYDataObject(x, y)  #todo if in the future different types of dataobjects are supported, find correct type and return it

    def max(self):
        return np.max(self.y)

    def argmax(self):
        #Todo this might be confusing because it returns the x value not the index like the numpy function
        return self.x[np.argmax(self.y)]

    def min(self):
        return np.min(self.y)

    def argmin(self):
        return self.x[np.argmin(self.y)]

    def mean(self):
        return np.mean(self.y)

    def std(self):
        return np.std(self.y)

    def var(self):
        return np.var(self.y)

    def median(self):
        return np.median(self.y)

# todo allows resizing of _xdata and _ydata simultaneously without breaking plotting
#todo allow saving to file


class XYDataObject(DataObjectBase):
    #might be up for a refactoring of the name if theres also going to be 2d data objects (XYDataObject, ListObject?)
    """ has x and y array"""
    label = Str('')
    x = Typed(np.ndarray)
    y = Typed(np.ndarray)
    x_updated = Event(kind=bool)
    y_updated = Event(kind=bool)

    from atomicplot2.fit import Fit1D
    from atomicplot2.plot import Plot1D

    fit = Typed(Fit1D)
    plot = Typed(Plot1D)

    file_path = Str # Optional file path pointing to original data file

    def __init__(self, x, y, *args, **kwargs):
        if not isinstance(x, (np.ndarray, list)):
            raise TypeError("xdata needs to be list or numpy array")
        if not isinstance(y, (np.ndarray, list)):
            raise TypeError("ydata needs to be list or numpy array")
        if isinstance(x, np.ndarray):
            if not len(x) == x.size:
                raise ValueError("xdata is not an one-dimensional array")
        if isinstance(y, np.ndarray):
            if not len(y) == y.size:
                raise ValueError("ydata is not an one-dimensional array")
        if not len(x) == len(y):
            raise ValueError("xdata, ydata have unequal length; found {}, {}".format(len(x), len(y)))

        self.x = UpdateArray(x, self.x_updated)
        self.y = UpdateArray(y, self.y_updated)

        self.fit = Fit1D(self)
        self.plot = Plot1D(self)

        super(XYDataObject, self).__init__(*args, **kwargs)


    def savetxt(self, file_path, **kwargs):
        pass
        #todo implement this



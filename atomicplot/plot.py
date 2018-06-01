from matplotlib.lines import Line2D
from matplotlib.axes import Axes, SubplotBase, subplot_class_factory
from matplotlib.figure import Figure
from atom.api import Atom, Event, Bool, Str, Float, Typed, ForwardInstance, Dict, Property, Instance, observe, List, Enum
import atomicplot2 as ap
from .base import PlotFunctionsDict
import numpy as np
import matplotlib.pyplot as plt
import warnings
from matplotlib.gridspec import GridSpec


class Plot1D(Atom):
    """plot attribute on dataobject"""
    updated = Event()

    x = Property()
    y = Property()

    _x_dict = Instance(PlotFunctionsDict)  #todo make this public?
    _y_dict = Instance(PlotFunctionsDict)

    parent = ForwardInstance(lambda: ap.data.XYDataObject)

    norm = Bool(False)
    zero = Bool(False)

    def __init__(self, parent, *args, **kwargs):
        super(Plot1D, self).__init__(*args, **kwargs)
        self.parent = parent

        self._x_dict = PlotFunctionsDict({})
        self._y_dict = PlotFunctionsDict({})

    def _get_x(self):
        x = np.copy(self.parent.x)
        result = self._apply_functions(self._x_dict, x)
        return result

    def _get_y(self):
        y = np.copy(self.parent.y)
        result = self._apply_functions(self._y_dict, y)
        return result

    @observe('norm')
    def _norm_changed(self, change):
        if change['value']:
            #todo needs to be diffent for normalizing the fit, should be the same factor. but how!?!? -> same functions on fit!
            self._y_dict['_norm'] = (lambda y: y / y.max(), [], {})
        else:
            del self._y_dict['_norm']

    @observe('zero')
    def _zero_changed(self, change):
        if change['value']:
            self._y_dict['_zero'] = (lambda x: x - x.min(), [], {})
            self._y_dict.move_to_end('_zero', last=False)  # Move zeroing to be the first operation
        else:
            del self._y_dict['_zero']

    def _apply_functions(self, functions, result):
        if functions:
            for f_key, content in functions.items():
                func, args, kwargs = content  # todo make args kwargs optional
                result = func(result, *args, **kwargs)
        return result


class AtomAxes(Atom):
    """axis for matplot, has reference to which plots, takes care of updateing etc"""

    mp_parent = ForwardInstance(lambda: MatPlot)  #todo figure out if its needed
    axes = Instance(Axes)
    data_objects = Dict(default={})

    def __init__(self, mp_parent, axes):
        self.mp_parent = mp_parent
        self.axes = axes
        super(AtomAxes, self).__init__()

    def __add__(self, other):
        #add a dataobject to these axes
        self.add_dataobject(other)

    def __sub__(self, other):
        # remove a dataobject from these axes
        self.remove_dataobject(other)

    def add_dataobject(self, data_obj):

        uid = id(data_obj)
        if uid in self.data_objects:
            raise KeyError('Data object already added') #todo print the label and shite

        self.data_objects[uid] = data_obj

        data_obj.plot.observe('updated', self.redraw_plot)

    def remove_dataobject(self, uid):
        assert type(uid) == int
        data_obj = self.data_objects.pop(uid)
        data_obj.plot.unobserve('updated')

    def redraw_plot(self, change):
        print(change)
        print('redrawing')


class MatPlot(Atom):
    """
    Overall class for matplotlib figure. can have several child axes instances.

    allow slider and next/prev buttons, interactive fitting?
    """

    fig = Typed(Figure)
    _axes = Instance(subplot_class_factory(), np.ndarray)
    axes = Instance(AtomAxes, np.ndarray)

    def __init__(self, nrows=1, ncols=1, sharex=False, sharey=False, squeeze=True,
                subplot_kw=None, gridspec_kw=None, **fig_kw):
        super(MatPlot, self).__init__()

        self.fig, self._axes = plt.subplots(nrows=1, ncols=1, sharex=sharex, sharey=sharey, squeeze=squeeze,
                                            subplot_kw=subplot_kw, gridspec_kw=gridspec_kw, **fig_kw)

        if isinstance(self._axes, np.ndarray):
            self.axes = np.array([AtomAxes(self, ax) for ax in self._axes]).reshape(nrows, ncols)
        else:
            self.axes = AtomAxes(self, self._axes)

    def __add__(self, other):
        if isinstance(self.axes, AtomAxes):
            self.axes.add_dataobject(other)
        else:
            raise ValueError('Please add the DataObject to the appropriate axes')

    def __sub__(self, other):
        if isinstance(self.axes, AtomAxes):
            self.axes.remove_dataobject(other)
        else:
            raise ValueError('Please add the DataObject to the appropriate axes')






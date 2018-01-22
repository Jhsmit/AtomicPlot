from matplotlib.lines import Line2D
from matplotlib.axes import Axes

from atom.api import Atom, Event, Bool, Str, Float, Typed, ForwardInstance
import atomicplot2 as ap

class Plot1D(Atom):
    """plot attribute on dataobject"""


    updated = Event()

    parent = ForwardInstance(lambda: ap.data.DataObject)

    def __init__(self, parent):
        self.parent = parent
        super()


class MatPlot(Atom):
    def __init__(self,):
        pass



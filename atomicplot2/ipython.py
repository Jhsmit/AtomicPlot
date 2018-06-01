from ipywidgets import widgets
from IPython.display import display, clear_output
import numpy as np
from atom.api import Atom, Event, Bool, Str, Float, Typed, ForwardInstance, Dict, Property, Instance, observe, List, Enum, Callable, Range, ContainerList, Int

from matplotlib.figure import Figure

class BrowseGraph(object):

    def __init__(self, iterable, func, fig):
        self._iterable = iterable
        self.func = func
        self.fig = fig
        self.axes = np.array(self.fig.axes).flatten()
        self.idx = 0

        self.btn_first = widgets.Button(description='First')
        self.btn_prev = widgets.Button(description='Prev')
        self.int_box = widgets.BoundedIntText(value=0, min=0, max=len(iterable) - 1)
        self.btn_next = widgets.Button(description='Next')
        self.btn_last = widgets.Button(description='Last')
        self.btn_random = widgets.Button(description='Random')

        self.int_box.observe(self.handle_int_box, names='value')

        self.btn_first.on_click(self.on_first)
        self.btn_prev.on_click(self.on_prev)
        self.btn_next.on_click(self.on_next)
        self.btn_last.on_click(self.on_last)
        self.btn_random.on_click(self.on_random)

        btn_hbox = widgets.HBox()
        btn_hbox.children = [self.btn_first, self.btn_prev, self.int_box, self.btn_next, self.btn_last, self.btn_random]
        self.update_graph()
        display(btn_hbox)

    def handle_int_box(self, change):
        self.idx = int(change.new)
        self.update_graph()

    def on_first(self, b):
        self.int_box.value = 0

    def on_prev(self, b):
        val = self.idx - 1
        self.int_box.value = 0 if val < 0 else val

    def on_next(self, b):
        val = self.idx + 1
        self.int_box.value = len(self._iterable) - 1 if val >= len(self._iterable) else val

    def on_last(self, b):
        self.int_box.value = len(self._iterable) - 1

    def on_random(self, b):
        self.int_box.value = np.random.randint(0, len(self._iterable))

    def update_graph(self):
        for ax in self.axes:
            ax.clear()

        self.func(self.fig, self._iterable[self.idx])

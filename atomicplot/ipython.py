import matplotlib.pyplot as plt
from ipywidgets import widgets
from IPython.display import display
import numpy as np
from ipywidgets import interact
class ImgSlider(object):
    """view image stacks in jupyter notebook"""
    #todo pyqtgraph?

    #defaults
    cmap = 'viridis'

    def __init__(self, img_stack):
        self.img_stack = img_stack
        self.fig, self.axes = plt.subplots()
        self.img_mpl = self.axes.imshow(self.img_stack[0])

        self.idx = 0

        vbox = widgets.VBox()

        frame_slider = widgets.IntSlider(
            value=0,
            min=0,
            max=len(img_stack),
            step=1,
            disabled=False,
            continuous_update=True,
            orientation='horizontal',
            readout=True,
            readout_format='d'
)
        frame_slider.observe(self.update, names='value')

        vmin = self.img_stack[0].min()
        vmax = self.img_stack[0].max()
        self.vrange_slider = widgets.FloatRangeSlider(
            value=[vmin, vmax],
            min=vmin,
            max=vmax,
            step=(vmax - vmin) / 1000,
            disabled=False,
            continuous_update=True,
            orientation='horizontal',
            readout=True,
            readout_format='.1f',
        )

        self.vrange_slider.observe(self.v_update, names='value')

        vbox.children = [frame_slider, self.vrange_slider]
        display(vbox)

    def update(self, change):
        new = change['new']
        self.idx = new
        new_img = self.img_stack[new]
        self.img_mpl.set_data(new_img)

        vmin, vmax = new_img.min(), new_img.max()
        self.img_mpl.set_clim(vmin=vmin, vmax=vmax)
        self.vrange_slider.min = vmin
        self.vrange_slider.max = vmax
        self.vrange_slider.value = (vmin, vmax)

    def v_update(self, change):
        vmin, vmax = change.new
        self.img_mpl.set_clim(vmin=vmin, vmax=vmax)

class BrowseGraph(object):
    """Does magic on your data in jupyter notebooks"""
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

        self.func(self._iterable[self.idx], self.fig)

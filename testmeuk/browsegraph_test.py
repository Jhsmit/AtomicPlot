import matplotlib.pyplot as plt
from ipywidgets import widgets 
from IPython.display import display, clear_output
import numpy as np
from atomicplot.ipython import BrowseGraph

interable = [(np.arange(5), np.arange(5)**i) for i in range(10)]

def plot_func(figure, data):
    x, y = data
    figure.axes[0].plot(x, y)
    figure.axes[1].plot(x, y, color='r')
    figure.tight_layout()

fig, axes = plt.subplots(1, 2)
bg = BrowseGraph(interable, plot_func, fig)
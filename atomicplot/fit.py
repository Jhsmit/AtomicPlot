from atom.api import Atom, Bool, Typed, observe, Value, ForwardInstance
from symfit.api import Fit, Model, Parameter, Variable, exp
import numpy as np

import atomicplot as ap




class FitObject(Atom):
    pass


class Fit1D(FitObject):
    'class for fitting 1d datasets'

    parent = ForwardInstance(lambda: ap.data.XYDataObject)
    plot = ForwardInstance(lambda: ap.plot.Plot1D)

    fitted = Bool(default=False) # boolean which indicates if current model and data are fitted

    _model = Value()
    result = Value()

    _fit = Typed(Fit)

    def __init__(self, parent, *args, **kwargs):
        self.parent = parent
        super(Fit1D, self).__init__(*args, **kwargs)

        self.result = None

    def add_model(self, model):
        if self._model: del self._model

        if isinstance(model, str):
            self._model = get_model(model, self.parent.x, self.parent.y)
        else:
            self._model = model

        self.fitted = False

    @observe('parent.x', 'parent.x_updated', 'parent.y', 'parent.y_updated')
    def _data_updated(self, change):
        self.fitted = False

    def execute(self, *options, **kwoptions):
        self._fit = Fit(self._model, self.parent.x, self.parent.y)
        self.result = self._fit.execute(*options, **kwoptions)


def get_model(model, xdata, ydata):  # todo classfactory, and xdata y data optional (is already classfactory)
    if model == 'exp_decay':
        a = Parameter(name='a', value=ydata[0], min=0)
        b = Parameter(name='b', value=ydata[-1], min=0)

        tau_pos = np.abs(ydata - (ydata[0] / np.e + ydata[-1])).argmin()
        tau = Parameter(name='tau', value=xdata[tau_pos], min=0)

        x = Variable(name='x')
        m = a * exp(-x / tau) + b
        return m

    elif model == 'double_exp_decay':
        a1 = Parameter(name='a1', value=ydata[0] / 2.1, min=0)
        a2 = Parameter(name='a2', value=ydata[0] / 1.9, min=0)
        b = Parameter(name='b', value=ydata[-1], min=0)

        tau_pos = np.abs(ydata - (ydata[0] / np.e + ydata[-1])).argmin()
        tau1 = Parameter(name='tau1', value=0.5 * xdata[tau_pos], min=0)
        tau2 = Parameter(name='tau2', value=2 * xdata[tau_pos], min=0)

        x = Variable(name='x')

        m = a1 * exp(-x / tau1) + a2 * exp(-x / tau2) + b
        return m

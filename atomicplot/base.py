import numpy as np
from collections import OrderedDict


class UpdateArray(np.ndarray):

    def __new__(cls, input_array, updated, info=None):
        obj = np.asarray(input_array).view(cls)
        obj.updated = updated
        return obj

    def __setitem__(self, key, value):
        self.updated = True
        super(UpdateArray, self).__setitem__(key, value)

    def __array_finalize__(self, obj):
        if obj is None: return
        self.updated = getattr(obj, 'updated', None)


class PlotFunctionsDict(OrderedDict):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __getitem__(self, item):
        if isinstance(item, int):
            print('whoooo')
        else:
            return super().__getitem__(item)

    def __setitem__(self, key, content):
        self._add_entry(key, content)

    def add(self, add_dic):
        for key, content in add_dic.items():

            i = 1
            while key in self:
                key += ('_' + str(i))
                i += 1

            self._add_entry(key, content)

    def _add_entry(self, key, content):
        func, args, kwargs = content
        assert isinstance(key, str)
        assert hasattr(func, '__call__')
        assert isinstance(args, list)
        assert isinstance(kwargs, dict)

        super().__setitem__(key, content)

        # norm always has to be last
        if '_norm' in self:
            self.move_to_end('_norm')

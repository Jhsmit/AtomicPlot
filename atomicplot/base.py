import numpy as np


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
from atom.api import Typed, Int, List, Atom, observe, Value, Event
import numpy as np


class Arr(np.ndarray):




    def __new__(cls, input_array, updated, info=None):
        obj = np.asarray(input_array).view(cls)
        obj.updated = updated
        return obj


    def __setitem__(self, key, value):
        print('woei')
        print(id(self.updated))
        print(self.updated)
        self.updated = True
        super(Arr, self).__setitem__(key, value)

    @observe('updated')
    def _updated_chagned(self, new):
        print('updated in ndarray')

    def __array_finalize__(self, obj):
        # see InfoArray.__array_finalize__ for comments
        if obj is None: return
        self.updated = getattr(obj, 'updated', None)


class TestClass(Atom):
    arr = Typed(np.ndarray)
    val = Value(default=np.arange(10))
    number = Int(default=10)
    x_arr = Typed(np.ndarray)
    x_arr_updated = Event(kind=bool)

    def __init__(self, x, *args, **kwargs):
        super(TestClass, self).__init__(*args, **kwargs)
      #  print(id(self.x_arr_updated))
        print(self.number)
        print(self.x_arr_updated)
        self.x_arr = Arr(x, self.x_arr_updated)

    @observe('x_arr')
    def _x_arr_changed(self, new):
        print('xarr')

    @observe('x_arr_updated')
    def _xarr_setitem(self, new):
        print('setitem')

    @observe('number')
    def _number_changed(self, new_value):
        print(new_value)
        print('number')

    @observe('arr')
    def _arr_changed(self, new_value):
        print(new_value)
        print(type(new_value))
        print('arr')

if __name__ == '__main__':
    tc = TestClass([1,2,3,4])
    #tc.number = 10
    #tc.arr = np.arange(5)
    # tc.arr = np.arange(10)**2 #updated
    # tc.arr = np.arange(10) #updated
    # tc.arr = np.arange(10) #updated
    #
    # tc.arr[2] = 10 #nothing

    # narr = Arr([1,2,3])
    # print(narr)
    # narr[2] = 10
    # print(narr)

    print('setitem on outer')
    tc.x_arr[1] = 100
    print(tc.x_arr)
    tc.x_arr[2] = 100
    print(tc.x_arr)
    tc.x_arr[2] = 100
    print(tc.x_arr)
  #  tc.x_arr.updated = 200
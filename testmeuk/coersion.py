#------------------------------------------------------------------------------
# Copyright (c) 2013-2017, Nucleic Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#------------------------------------------------------------------------------
from __future__ import (division, unicode_literals, print_function,
                        absolute_import)

from atom.api import Atom, Coerced, observe, Typed
import numpy as np

class Demo(Atom):

    cint = Coerced(int)
    cfloat = Coerced(float)
    cstr = Coerced(str)
    #carr = Coerced(np.ndarray, coercer=np.asarray)
    carr = Typed(np.ndarray)

    @observe('carr')
    def _carr(self, new):
        print(new)
        print('joehoe')

if __name__ == '__main__':
    demo = Demo()

    print('CInt Demo')
    demo.cint = '1'
    print(demo.cint)
    demo.cint = 51.5
    print(demo.cint)

    print('\nCFloat Demo')
    demo.cfloat = '1.5'
    print(demo.cfloat)
    demo.cfloat = 100
    print(demo.cfloat)

    print('\nCStr Demo')
    demo.cstr = 100
    print(demo.cstr)
    demo.cstr = Demo
    print(demo.cstr)

    print('test')
    b = np.array([1, 2, 3, 4])


    demo.carr = b
    print(demo.carr)
    print(type(demo.carr))
    print(demo.carr.shape)

    demo.carr[2] = 5
    print(demo.carr)

    a = np.arange(4)
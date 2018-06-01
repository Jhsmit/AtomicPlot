from atom.api import Atom, List, ContainerList, Coerced, Delegator
import numpy as np

class TestClass(Atom):
    l1 = ContainerList()



tc =  TestClass()

tc.l1 = [1,23,3]
tc.l1 = np.array([])
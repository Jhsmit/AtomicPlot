import numpy as np
import matplotlib.pyplot as plt




f = plt.figure(1)
plt.hist(np.random.rand(100))
f.show()

g = plt.figure(2)
plt.plot(np.arange(10), np.arange(10)**2)
g.show()

plt.show()
#input()
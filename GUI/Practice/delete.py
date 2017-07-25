import matplotlib.pyplot as plt
import numpy as np

x,y = np.loadtxt ('/Users/Filmon/UW/Set2/Film12topo_0058.txt', delimiter=',', unpack=True)
plt.plot(x,y, label='Loaded from file')


plt.xlabel('x')
plt.ylabel('y')
plt.title('Interesting Graph\nCheck it out')
plt.legend()
plt.show()

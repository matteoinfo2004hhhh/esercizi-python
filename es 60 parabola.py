import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

x = np.arange(-10, 10, 0.1)

y = x**2

plt.plot(x, y, color='b', label='y = x^2')

plt.xlabel('x')
plt.ylabel('y')
plt.legend()

plt.savefig(sys.stdout.buffer)
sys.stdout.flush()


import sys
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np

ypoints = np.array([1, 2, 3, 4, 5,10])

plt.plot(ypoints, 'o:r')
plt.show()

plt.savefig(sys.stdout.buffer)
sys.stdout.flush()

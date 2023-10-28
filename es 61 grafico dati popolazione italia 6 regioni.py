import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

città = ['Torino', 'Roma', 'Napoli', 'Sicilia', 'Sardegna', 'Trentino']
popolazione = [900000, 2800000, 980000, 5000000, 1600000, 540000]

x = np.arange(len(città))

plt.bar(x, popolazione, align='center', alpha=0.7)
plt.xticks(x, città)
plt.ylabel('Popolazione')
plt.title('Popolazione delle città italiane')

plt.savefig(sys.stdout.buffer)
sys.stdout.flush()


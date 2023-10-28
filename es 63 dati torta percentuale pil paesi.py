import sys
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt

paesi = ['USA', 'Cina', 'Giappone', 'Germania']
valori = [25, 30, 23, 15]

plt.figure(figsize=(6, 6))
plt.pie(valori, labels=paesi, autopct='%1.1f%%', startangle=140)
plt.title('Percentuale del PIL per i 4 paesi più ricchi')
plt.axis('equal') 

plt.savefig(sys.stdout.buffer)
sys.stdout.flush()


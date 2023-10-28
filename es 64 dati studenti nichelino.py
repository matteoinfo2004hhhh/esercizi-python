import sys
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt

rimandati = 16
bocciati = 45
promossi = 75

categorie = ['Rimandati', 'Bocciati', 'Promossi']
valori = [rimandati, bocciati, promossi]

plt.figure(figsize=(6, 6))
plt.pie(valori, labels=categorie, autopct='%1.1f%%', startangle=140)
plt.title('Distribuzione degli studenti a Nichelino')
plt.axis('equal') 

plt.savefig(sys.stdout.buffer)
sys.stdout.flush()
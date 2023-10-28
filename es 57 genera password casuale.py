import random
import string

n = int(input("Inserisci la lunghezza della password: "))
password = ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(n))
print("Password casuale:", password)

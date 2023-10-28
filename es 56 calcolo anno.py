mese = input("Inserisci un mese: ").lower()
year = int(input("L'anno è bisestile? (1 per Sì, 0 per No): ")) == 1

if mese in {"gennaio", "marzo", "maggio", "luglio", "agosto", "ottobre", "dicembre"}:
    print("31 giorni.")
elif mese in {"aprile", "giugno", "settembre", "novembre"}:
    print("30 giorni.")
elif mese == "febbraio":
    if year:
        print("29 giorni.")
    else:
        print("28 giorni.")
else:
    print("Mese non valido.")
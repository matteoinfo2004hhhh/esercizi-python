def calcola_stipendio(ore_lavorate, stipendio_orario):
    stipendio = ore_lavorate * stipendio_orario
    return stipendio
    
def main():
    try:
        ore_lavorate = float(input("Inserisci il numero di ore lavorate: "))
        stipendio_orario = float(input("Inserisci lo stipendio orario: "))
        
        stipendio = calcola_stipendio(ore_lavorate, stipendio_orario)
        
        print(f"Lo stipendio per {ore_lavorate} ore lavorate è: {stipendio} euro")
        
    except ValueError:
        print("Errore: Assicurati di inserire numeri validi per le ore lavorate e lo stipendio orario.")

if __name__ == "__main__":
    main()

import pygame
import random
import sys

pygame.init()
SCHERMO_LARGHEZZA, SCHERMO_ALTEZZA = 588, 512

# Caricamento immagini
sfondo_originale = pygame.image.load('immagini/sfondo.png')
sfondo = pygame.transform.scale(sfondo_originale, (SCHERMO_LARGHEZZA, SCHERMO_ALTEZZA))
uccello = pygame.image.load('immagini/uccello.png')
base = pygame.image.load('immagini/base.png')
sfondo = pygame.transform.scale(sfondo_originale, (SCHERMO_LARGHEZZA, SCHERMO_ALTEZZA))
gameover = pygame.image.load('immagini/gameover.png')
tubo_giu = pygame.image.load('immagini/tubo.png')
tubo_su = pygame.transform.flip(tubo_giu, False, True)

# Schermo e parametri
SCHERMO = pygame.display.set_mode((588, 512))
FPS = 60
VEL_AVANZ = 3
FONT = pygame.font.SysFont('Comic Sans MS', 40, bold=True)
FONT_PULSANTI = pygame.font.Font(pygame.font.get_default_font(), 30)  # Font "pixelato" se disponibile

# Colori
COLORE_BIANCO = (255, 255, 255)
COLORE_NERO = (0, 0, 0)
COLORE_GIALLO = (255, 255, 0)  # Colore per i pulsanti

# Classe dei tubi
class tubi_classe:
    def __init__(self):
        self.x = 550
        self.y = random.randint(-75, 150)
        self.superato = False  # Aggiunta variabile per verificare se il tubo è stato superato

    def avanzadisegna(self):
        self.x -= VEL_AVANZ
        SCHERMO.blit(tubo_giu, (self.x, self.y + 210))  # Tubo inferiore
        SCHERMO.blit(tubo_su, (self.x, self.y - 210))  # Tubo superiore

    def collisione(self, uccello, uccellox, uccelloy):
        tolleranza = 5
        ucello_lato_dx = uccellox + uccello.get_width() - tolleranza
        ucello_lato_sx = uccellox + tolleranza
        tubi_lato_ds = self.x + tubo_giu.get_width()
        tubi_lato_sx = self.x
        uccello_lato_su = uccelloy + tolleranza
        uccello_lato_giu = uccelloy + uccello.get_height() - tolleranza
        tubi_lato_su = self.y + 110
        tubi_lato_giu = self.y + 210
        if ucello_lato_dx > tubi_lato_sx and ucello_lato_sx < tubi_lato_ds:
            if uccello_lato_su < tubi_lato_su or uccello_lato_giu > tubi_lato_giu:
                hai_perso()

# Funzione per disegnare gli oggetti
def disegnaoggetti():
    SCHERMO.blit(sfondo, (0, 0))
    for t in tubi:
        t.avanzadisegna()
    SCHERMO.blit(uccello, (uccellox, uccelloy))
    SCHERMO.blit(base, (basex, 400))

    # Disegna il testo "Punteggio"
    punteggio_testo = FONT.render("Punteggio:", True, (0, 0, 0))
    SCHERMO.blit(punteggio_testo, (130, 430))

    # Disegna il valore del punteggio
    punti_render = FONT.render(str(punti), True, (0, 0, 0))
    SCHERMO.blit(punti_render, (330, 430))  # Posiziona il punteggio accanto al testo "Punteggio"


# Funzione per disegnare gli oggetti



# Funzione per aggiornare lo schermo
def aggiorna():
    pygame.display.update()
    pygame.time.Clock().tick(FPS)


# Funzione per disegnare un pulsante con bordo
def disegna_pulsante(testo, x, y, larghezza, altezza, colore_sfondo, colore_testo):
    pygame.draw.rect(SCHERMO, colore_sfondo, (x, y, larghezza, altezza))  # Pulsante
    pygame.draw.rect(SCHERMO, COLORE_NERO, (x, y, larghezza, altezza), 2)  # Bordo del pulsante
    testo_render = FONT_PULSANTI.render(testo, True, colore_testo)
    SCHERMO.blit(testo_render,
                 (x + (larghezza - testo_render.get_width()) // 2, y + (altezza - testo_render.get_height()) // 2))


# Funzione per gestire i clic sui pulsanti
def cliccato(x, y, larghezza, altezza):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x < mouse[0] < x + larghezza and y < mouse[1] < y + altezza:
        if click[0] == 1:
            return True
    return False


# Funzione per disegnare il titolo
def disegna_titolo(testo, x, y, larghezza):
    titolo_render = FONT.render(testo, True, COLORE_BIANCO)
    # Calcola la posizione centrata
    x_pos = x + (larghezza - titolo_render.get_width()) // 2
    y_pos = y
    SCHERMO.blit(titolo_render, (x_pos, y_pos))


# Funzione per iniziare il gioco
def inizia():
    global uccellox, uccelloy, uccello_vely
    global basex
    global tubi
    global punti
    uccellox, uccelloy = 60, 150
    uccello_vely = 0
    basex = 0
    punti = 0
    tubi = []
    tubi.append(tubi_classe())


# Funzione per gestire la fine del gioco
def hai_perso():
    while True:
        SCHERMO.blit(gameover, (120, 180))
        disegna_pulsante('Riprova', 150, 300, 300, 70, COLORE_GIALLO, COLORE_NERO)
        aggiorna()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Gestione del clic sul pulsante "Riprova"
        if cliccato(150, 300, 300, 70):
            inizia()
            return  # Uscita dalla funzione per ricominciare il gioco


# Funzione per mostrare la schermata iniziale
def schermata_iniziale():
    while True:
        SCHERMO.blit(sfondo, (0, 0))

        # Disegna il titolo "Matteo" sopra il pulsante
        titolo_x = 230
        titolo_y = 50
        pulsante_larghezza = 100
        disegna_titolo('Matteo Barcellona', titolo_x, titolo_y, pulsante_larghezza)

        # Disegna il pulsante "Gioca"
        disegna_pulsante('Gioca', 150, 300, 300, 70, COLORE_GIALLO, COLORE_NERO)
        aggiorna()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Gestione del clic sul pulsante "Gioca"
        if cliccato(150, 300, 300, 70):
            inizia()
            return  # Uscita dalla funzione per iniziare il gioco


# Inizio del gioco
schermata_iniziale()

# Ciclo principale
while True:
    basex -= VEL_AVANZ
    if basex < -45:
        basex = 0
    uccello_vely += 1
    uccelloy += uccello_vely

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            uccello_vely = -10
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Aggiunta di nuovi tubi
    if tubi[-1].x < 150:
        tubi.append(tubi_classe())

    # Controllo collisioni e aggiornamento punteggio
    for t in tubi:
        t.collisione(uccello, uccellox, uccelloy)

        # Aggiungi un punto se l'uccello ha superato il tubo
        if not t.superato and t.x + tubo_giu.get_width() < uccellox:
            punti += 1
            t.superato = True

    # Controllo se l'uccello tocca il suolo
    if uccelloy > 380:
        hai_perso()

    disegnaoggetti()
    aggiorna()

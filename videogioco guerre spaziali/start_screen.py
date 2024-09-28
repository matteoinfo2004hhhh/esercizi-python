import pygame
import sys

# Inizializza Pygame
pygame.init()

# Dimensioni iniziali della finestra
WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Schermo di Avvio")

# Colori
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Funzione per disegnare un pulsante
def draw_button(text, x, y, width, height):
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, BLUE, button_rect)
    font = pygame.font.SysFont(None, int(36 * (width / 200)))  # Ridimensiona il font in base alla larghezza del pulsante
    button_text = font.render(text, True, WHITE)
    text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, text_rect)
    return button_rect

# Funzione per disegnare il titolo, il nome dello sviluppatore e i pulsanti
def draw_start_screen(scale_factor):
    screen.fill(BLACK)

    # Font per il titolo e il nome dello sviluppatore
    font_title = pygame.font.SysFont(None, int(72 * scale_factor))
    font_developer = pygame.font.SysFont(None, int(36 * scale_factor))

    # Titolo del gioco
    title_text = font_title.render('Gioco Spaziale', True, WHITE)
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100 * scale_factor))
    screen.blit(title_text, title_rect)

    # Nome dello sviluppatore
    developer_text = font_developer.render('Sviluppato da Matteo Barcellona', True, WHITE)
    developer_rect = developer_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40 * scale_factor))
    screen.blit(developer_text, developer_rect)

    # Disegna pulsanti
    button_width = 200 * scale_factor
    button_height = 50 * scale_factor
    play_button = draw_button('Gioca', WIDTH // 2 - button_width // 2, HEIGHT // 2 + 20 * scale_factor, button_width, button_height)
    exit_button = draw_button('Esci', WIDTH // 2 - button_width // 2, HEIGHT // 2 + 100 * scale_factor, button_width, button_height)

    return play_button, exit_button

# Funzione principale dello schermo di avvio
def main():
    global WIDTH, HEIGHT, screen
    clock = pygame.time.Clock()
    scale_factor = 1  # Fattore di scala iniziale

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.VIDEORESIZE:
                WIDTH, HEIGHT = event.w, event.h
                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
                scale_factor = WIDTH / 800  # Calcola il fattore di scala in base alla larghezza

        play_button, exit_button = draw_start_screen(scale_factor)

        # Controllo per passare al gioco principale o uscire
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        if play_button.collidepoint(mouse_pos) and mouse_click[0]:  # Clicca su "Gioca"
            import game  # Importa il file del gioco principale
            game.main()  # Avvia la funzione principale del gioco
        elif exit_button.collidepoint(mouse_pos) and mouse_click[0]:  # Clicca su "Esci"
            pygame.quit()
            sys.exit()

        pygame.display.flip()
        clock.tick(60)

# Avvia lo schermo di avvio
if __name__ == "__main__":
    main()

import pygame
import sys

# Inizializza Pygame
pygame.init()

# Dimensioni iniziali della finestra
WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

# Colori
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Funzione per disegnare un pulsante
def draw_button(text, x, y, width, height):
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, BLUE, button_rect)
    font = pygame.font.SysFont(None, int(36 * (width / 200)))  # Ridimensiona il font
    button_text = font.render(text, True, WHITE)
    text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, text_rect)
    return button_rect

# Funzione per disegnare la schermata di Game Over
def draw_game_over_screen(scale_factor):
    screen.fill(BLACK)

    # Font per il titolo
    font_title = pygame.font.SysFont(None, int(72 * scale_factor))
    game_over_text = font_title.render('Game Over', True, RED)
    title_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100 * scale_factor))
    screen.blit(game_over_text, title_rect)

    # Disegna pulsanti
    button_width = 200 * scale_factor
    button_height = 50 * scale_factor
    retry_button = draw_button('Riprova', WIDTH // 2 - button_width // 2, HEIGHT // 2 + 20 * scale_factor, button_width, button_height)
    exit_button = draw_button('Esci', WIDTH // 2 - button_width // 2, HEIGHT // 2 + 100 * scale_factor, button_width, button_height)

    return retry_button, exit_button

# Funzione principale della schermata di Game Over
def game_over_screen():
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
                scale_factor = WIDTH / 800  # Calcola il fattore di scala

        retry_button, exit_button = draw_game_over_screen(scale_factor)

        # Controllo per clic sui pulsanti
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        if retry_button.collidepoint(mouse_pos) and mouse_click[0]:  # Clicca su "Riprova"
            return True  # Ritorna per riprovare
        elif exit_button.collidepoint(mouse_pos) and mouse_click[0]:  # Clicca su "Esci"
            pygame.quit()
            sys.exit()

        pygame.display.flip()
        clock.tick(60)

# Esempio di utilizzo
if __name__ == "__main__":
    game_over_screen()

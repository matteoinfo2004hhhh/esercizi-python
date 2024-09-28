import pygame
import random
from game_over import game_over_screen  # Importa la schermata di Game Over

# Inizializza Pygame
pygame.init()

# Dimensioni iniziali della finestra
WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Gioco Spaziale")

# Colori
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Carica i suoni
shoot_sound = pygame.mixer.Sound('shot.wav')
explosion_sound = pygame.mixer.Sound('Explosion.wav')

# Funzione per caricare e ridimensionare le immagini
def load_and_scale_image(image_path, width, height):
    image = pygame.image.load(image_path)
    return pygame.transform.scale(image, (width, height))

# Carica e ridimensiona le immagini
ship_img = load_and_scale_image('ship.png', 150, 150)
meteor_img = load_and_scale_image('meteor.png', 100, 100)
bullet_img = load_and_scale_image('bullet.png', 20, 40)

# Classi per navicella, proiettili e meteoriti
class Ship:
    def __init__(self):
        self.original_image = ship_img
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        self.speed = 15
        self.last_shot = 0

    def move(self, dx):
        self.rect.x += dx
        # Assicura che la navicella rimanga all'interno dei limiti dello schermo
        self.rect.x = max(0, min(WIDTH - self.rect.width, self.rect.x))

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot >= 270:
            self.last_shot = current_time
            shoot_sound.play()  # Riproduci il suono dello sparo
            return Bullet(self.rect.centerx, self.rect.top)
        return None

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def resize(self, scale_factor):
        new_width = int(100 * scale_factor)  # Dimensione navicella scalata
        new_height = int(100 * scale_factor)
        # Centra la navicella nella parte inferiore della finestra ridimensionata
        self.rect = self.image.get_rect(center=(min(self.rect.centerx, WIDTH - new_width // 2), HEIGHT - new_height - 20))

class Bullet:
    def __init__(self, x, y):
        self.original_image = bullet_img
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 20

    def update(self):
        self.rect.y -= self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def resize(self, scale_factor):
        new_width = int(20 * scale_factor)  # Dimensione proiettile scalata
        new_height = int(40 * scale_factor)
        self.rect = self.image.get_rect(center=self.rect.center)

class Meteor:
    def __init__(self):
        self.original_image = meteor_img
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(random.randint(0, WIDTH), 0))
        self.speed = random.randint(1, 17)

    def update(self):
        self.rect.y += self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def resize(self, scale_factor):
        new_width = int(80 * scale_factor)  # Dimensione meteorite scalata
        new_height = int(80 * scale_factor)
        self.rect = self.image.get_rect(center=self.rect.center)

# Funzione per disegnare il punteggio
def draw_score(surface, score, scale_factor):
    font = pygame.font.SysFont(None, int(36 * scale_factor))
    score_text = font.render(f'PUNTEGGIO: {score}', True, WHITE)
    surface.blit(score_text, (10, 10))

# Funzione principale del gioco
def main():
    global WIDTH, HEIGHT, screen
    clock = pygame.time.Clock()
    running = True

    while running:
        game_over = False
        score = 0

        ship = Ship()
        bullets = []
        meteors = []

        scale_factor = 1  # Fattore di scala iniziale

        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.VIDEORESIZE:
                    WIDTH, HEIGHT = event.w, event.h
                    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
                    scale_factor = WIDTH / 1000  # Calcola il fattore di scala in base alla larghezza
                    ship.resize(scale_factor)
                    for bullet in bullets:
                        bullet.resize(scale_factor)
                    for meteor in meteors:
                        meteor.resize(scale_factor)

            keys = pygame.key.get_pressed()
            if not game_over:
                if keys[pygame.K_LEFT]:
                    ship.move(-ship.speed)
                if keys[pygame.K_RIGHT]:
                    ship.move(ship.speed)
                if keys[pygame.K_SPACE]:
                    new_bullet = ship.shoot()
                    if new_bullet:
                        bullets.append(new_bullet)

                # Aggiorna proiettili
                for bullet in bullets[:]:
                    bullet.update()
                    if bullet.rect.y < 0:
                        bullets.remove(bullet)

                # Aggiorna meteoriti
                if random.random() < 0.02:
                    meteors.append(Meteor())

                for meteor in meteors[:]:
                    meteor.update()
                    if meteor.rect.y > HEIGHT:
                        meteors.remove(meteor)

                    # Collisione navicella-meteorite
                    if meteor.rect.colliderect(ship.rect):
                        game_over = True

                    # Collisione proiettile-meteorite
                    for bullet in bullets[:]:
                        if bullet.rect.colliderect(meteor.rect):
                            bullets.remove(bullet)
                            meteors.remove(meteor)
                            explosion_sound.play()  # Riproduci il suono di esplosione
                            score += 1

            # Disegna lo schermo
            screen.fill(BLACK)
            ship.draw(screen)
            for bullet in bullets:
                bullet.draw(screen)
            for meteor in meteors:
                meteor.draw(screen)

            # Disegna il punteggio
            draw_score(screen, score, scale_factor)

            # Game over
            if game_over:
                if not game_over_screen():  # Mostra la schermata di Game Over
                    running = False  # Esci dal ciclo principale
                else:
                    main()  # Riavvia il gioco

            pygame.display.flip()
            clock.tick(60)

    pygame.quit()

# Avvia il gioco
if __name__ == "__main__":
    main()

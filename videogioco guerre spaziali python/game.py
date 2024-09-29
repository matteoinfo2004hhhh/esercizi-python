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
explosion_sound = pygame.mixer.Sound('Explosion.wav')  # Suono dell'esplosione
power_up_sound = pygame.mixer.Sound('power_up.wav')

# Funzione per caricare e ridimensionare le immagini
def load_and_scale_image(image_path, width, height):
    image = pygame.image.load(image_path)
    return pygame.transform.scale(image, (width, height))


# Carica e ridimensiona le immagini
ship_img = load_and_scale_image('ship.png', 80, 91)
bullet_img = load_and_scale_image('bullet.png', 20, 40)
power_up_img = pygame.image.load('power_up.png')
# Carica l'immagine del meteorite
meteor_img = pygame.image.load('meteor.png')


# Classi per navicella, proiettili e meteoriti
class Ship:
    def __init__(self):
        self.original_image = ship_img
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        self.speed = 15
        self.last_shot = 0
        self.life = 100  # Vita iniziale della navicella

    def move(self, dx):
        self.rect.x += dx
        # Assicura che la navicella rimanga all'interno dei limiti dello schermo
        self.rect.x = max(0, min(WIDTH - self.rect.width, self.rect.x))

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot >= 220:
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
        self.rect = self.image.get_rect(
            center=(min(self.rect.centerx, WIDTH - new_width // 2), HEIGHT - new_height - 20))


class Bullet:
    def __init__(self, x, y):
        self.original_image = bullet_img
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 25

    def update(self):
        self.rect.y -= self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def resize(self, scale_factor):
        new_width = int(20 * scale_factor)  # Dimensione proiettile scalata
        new_height = int(40 * scale_factor)
        self.rect = self.image.get_rect(center=self.rect.center)


class Meteor:
    def __init__(self, size=None, x=None, y=None):
        # Se le dimensioni non sono specificate, genera casualmente
        if size is None:
            self.size = random.randint(40, 130)  # Dimensioni da 40 a 130
        else:
            self.size = size

        # Numero di colpi necessari per distruggerlo, proporzionale alla dimensione
        self.life = max(10, min(20, self.size // 8))  # Varia da 10 a 20

        # Se la posizione non è specificata, genera casualmente
        if x is None or y is None:
            x = random.randint(0, WIDTH)
            y = 0  # Inizia dall'alto dello schermo

        self.original_image = pygame.transform.scale(meteor_img, (self.size, self.size))
        self.angle = 0
        self.rotation_speed = random.randint(-5, 5)  # Rotazione casuale in gradi per frame
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = random.randint(1, 7)

    def update(self):
        self.rect.y += self.speed
        self.angle = (self.angle + self.rotation_speed) % 360  # Rotazione continua
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def resize(self, scale_factor):
        new_size = int(self.size * scale_factor)
        self.image = pygame.transform.scale(self.original_image, (new_size, new_size))
        self.rect = self.image.get_rect(center=self.rect.center)

    def is_destroyed(self):
        return self.life >= -30

    def hit(self):
        """Riduce la vita del meteorite e ridimensiona se necessario."""
        self.life -= 8
        if self.life > 0:
            new_size = max(self.size - 18, 20)  # Riduce la dimensione ma non sotto i 20 pixel
            self.size = new_size
            self.image = pygame.transform.scale(meteor_img, (self.size, self.size))
            self.rect = self.image.get_rect(center=self.rect.center)  # Mantieni il centro del meteorite
            return False  # Non distrutto, quindi restituisce False
        else:
            return True  # Distrutto, quindi restituisce True



class PowerUp:
    def __init__(self, x, y):
        self.image = pygame.transform.scale(power_up_img, (80, 80))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 5  # Velocità di caduta del potenziamento

    def update(self):
        self.rect.y += self.speed  # Muovi il potenziamento verso il basso

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Funzione per disegnare il punteggio
def draw_score(surface, score, scale_factor):
    font = pygame.font.SysFont(None, int(36 * scale_factor))
    score_text = font.render(f'PUNTEGGIO: {-score}', True, WHITE)
    surface.blit(score_text, (10, 10))


# Funzione principale del gioco
def main():
    global WIDTH, HEIGHT, screen
    clock = pygame.time.Clock()
    running = True

    while running:
        game_over = False
        score = 0
        power_ups = []  # Lista dei potenziamenti

        ship = Ship()
        bullets = []
        meteors = [Meteor()]  # Inizia con un meteorite

        scale_factor = 1  # Fattore di scala iniziale
        power_up_timer = 0  # Timer per generare potenziamenti

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
                        # Calcola danno in base alla dimensione del meteorite
                        if meteor.size < 50:  # Meteorite piccolo
                            damage = random.randint(2, 6)  # Danno da -2 a -6
                        else:  # Meteorite grande
                            damage = random.randint(50, 80)  # Danno da -50 a -80

                        ship.life -= damage
                        explosion_sound.play()  # Riproduci il suono di esplosione quando la navicella tocca il meteorite
                        meteors.remove(meteor)  # Rimuovi il meteorite dopo la collisione

                        if ship.life <= 0:  # Se la vita scende a 0, game over
                            game_over = True

                # Aggiorna potenziamenti
                power_up_timer += clock.get_time()
                if power_up_timer >= 20000:  # Ogni 20 secondi
                    power_up_x = random.randint(0, WIDTH)
                    power_ups.append(PowerUp(power_up_x, 0))  # Aggiungi un nuovo potenziamento
                    power_up_timer = 0

                for power_up in power_ups[:]:
                    power_up.update()
                    if power_up.rect.y > HEIGHT:  # Rimuovi il potenziamento se esce dallo schermo
                        power_ups.remove(power_up)

                    # Collisione navicella-potenziaento
                    if power_up.rect.colliderect(ship.rect):
                        power_ups.remove(power_up)  # Rimuovi il potenziamento
                        ship.life += 50  # Aggiungi vita alla navicella
                        power_up_sound.play()  # Riproduci il suono del potenziamento

            # Collisione proiettile-meteorite
            for bullet in bullets[:]:  # Itera su una copia della lista
                for meteor in meteors[:]:  # Itera sui meteoriti
                    if bullet.rect.colliderect(meteor.rect):
                        bullets.remove(bullet)  # Rimuovi il proiettile dalla lista
                        if meteor.hit():
                            explosion_sound.play()  # Riproduci il suono di esplosione
                            score += meteor.life  # Aumenta il punteggio basato sulla vita
                            meteors.remove(meteor)  # Rimuovi il meteorite dalla lista

                            # Se il meteorite è grande, genera 2 meteoriti più piccoli
                            if meteor.size > 50:
                                meteors.append(Meteor(meteor.size // 2, meteor.rect.x, meteor.rect.y))
                                meteors.append(Meteor(meteor.size // 2, meteor.rect.x, meteor.rect.y))
                        break  # Esci dal ciclo meteor per evitare di rimuovere più volte lo stesso proiettile

            # Disegna lo schermo
            screen.fill(BLACK)
            ship.draw(screen)
            for bullet in bullets:
                bullet.draw(screen)
            for meteor in meteors:
                meteor.draw(screen)
            for power_up in power_ups:
                power_up.draw(screen)  # Disegna il potenziamento

            # Disegna il punteggio e la vita della navicella
            draw_score(screen, score, scale_factor)
            life_text = pygame.font.SysFont(None, int(36 * scale_factor)).render(f'VITA: {ship.life}', True, WHITE)
            screen.blit(life_text, (10, 60))

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

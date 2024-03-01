
import pygame
import sys
import random

# Initialize Pygame and Mixer for Sound
pygame.init()
pygame.mixer.init()

# Set up the display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Space Defender')

# Colors
black = (0, 0, 0)
white = (255, 255, 255)

# Load images
player_img = pygame.image.load('player.png')
enemy_img = pygame.image.load('enemy.png')
bullet_img = pygame.image.load('bullet.png')
powerup_img = pygame.image.load('powerup.png')

# Load sounds
shoot_sound = pygame.mixer.Sound('shoot.wav')
explosion_sound = pygame.mixer.Sound('explosion.wav')
pygame.mixer.music.load('background.mp3')
pygame.mixer.music.play(-1)  # Play background music indefinitely

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.centerx = screen_width / 2
        self.rect.bottom = screen_height - 10
        self.speed_x = 0

    def update(self):
        self.speed_x = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speed_x = -5
        if keystate[pygame.K_RIGHT]:
            self.speed_x = 5
        self.rect.x += self.speed_x
        self.rect.x = max(0, min(self.rect.x, screen_width - self.rect.width))

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        shoot_sound.play()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = random.randint(50, 150)
        self.speed_x = random.randint(-3, 3)
        self.speed_y = random.randint(1, 2)

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.right > screen_width or self.rect.left < 0:
            self.speed_x = -self.speed_x
        if self.rect.top > screen_height:
            self.rect.x = random.randint(0, screen_width - self.rect.width)
            self.rect.y = random.randint(50, 150)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speed_y = -10

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.image = powerup_img
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speed_y = 2

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > screen_height:
            self.kill()

# Game Initialization
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
powerups = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

for i in range(8):  # Increase number of enemies
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

score_value = 0
font_name = pygame.font.match_font('arial')

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, white)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def show_score(x, y):
    draw_text(screen, "Score: " + str(score_value), 18, x, y)

# Main game loop
running = True
while running:
    # Keep loop running at the right speed
    pygame.time.Clock().tick(60)

    # Process input (events)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # Update
    all_sprites.update()

    # Check to see if a bullet hit an enemy
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for hit in hits:
        score_value += 10  # Increase score
        explosion_sound.play()
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)
        if random.random() > 0.9:  # Chance to spawn a power-up
            pow = PowerUp(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)

    # Draw / render
    screen.fill(black)
    all_sprites.draw(screen)
    show_score(10, 10)

    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
sys.exit()
# Path: Scripts/SpaceDefender_v2.py
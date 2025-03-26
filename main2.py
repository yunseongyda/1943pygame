import pygame  
import random  

# Initialize Pygame  
pygame.init()

# Game Constants  
WIDTH, HEIGHT = 480, 640  
FPS = 60  

# Colors  
WHITE = (255, 255, 255)  
RED = (255, 0, 0)  
BLACK = (0, 0, 0)  
BLUE = (0, 0, 255)  

# Create game window  
screen = pygame.display.set_mode((WIDTH, HEIGHT))  
pygame.display.set_caption("Strikers 1945 Clone")  

# Load images  
player_img = pygame.image.load("player.png")  
player_img = pygame.transform.scale(player_img, (50, 50))  
enemy_img = pygame.image.load("enemy1.png")  
enemy_img = pygame.transform.scale(enemy_img, (50, 50))  

# Fonts  
font = pygame.font.Font(None, 40)  

# Bullet settings  
BULLET_SPEED = -10  

# Game States  
MENU = "menu"  
PLAYING = "playing"  
SETTINGS = "settings"  
state = MENU  

# Player class  
class Player(pygame.sprite.Sprite):  
    def __init__(self):  
        super().__init__()  
        self.image = player_img  
        self.rect = self.image.get_rect()  
        self.rect.center = (WIDTH // 2, HEIGHT - 60)  
        self.speed = 5  

    def update(self):  
        keys = pygame.key.get_pressed()  
        if keys[pygame.K_LEFT] and self.rect.left > 0:  
            self.rect.x -= self.speed  
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:  
            self.rect.x += self.speed  
        if keys[pygame.K_UP] and self.rect.top > 0:  
            self.rect.y -= self.speed  
        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:  
            self.rect.y += self.speed  

    def shoot(self):  
        bullet = Bullet(self.rect.centerx, self.rect.top)  
        all_sprites.add(bullet)  
        bullets.add(bullet)  

# Bullet class  
class Bullet(pygame.sprite.Sprite):  
    def __init__(self, x, y):  
        super().__init__()  
        self.image = pygame.Surface((5, 15))  
        self.image.fill(RED)  
        self.rect = self.image.get_rect()  
        self.rect.center = (x, y)  

    def update(self):  
        self.rect.y += BULLET_SPEED  
        if self.rect.bottom < 0:  
            self.kill()  

# Enemy class  
class Enemy(pygame.sprite.Sprite):  
    def __init__(self):  
        super().__init__()  
        self.image = enemy_img  
        self.rect = self.image.get_rect()  
        self.rect.x = random.randint(0, WIDTH - self.rect.width)  
        self.rect.y = random.randint(-100, -40)  
        self.speed = random.randint(2, 5)  

    def update(self):  
        self.rect.y += self.speed  
        if self.rect.top > HEIGHT:  
            self.rect.y = random.randint(-100, -40)  
            self.rect.x = random.randint(0, WIDTH - self.rect.width)  

# Create sprite groups  
all_sprites = pygame.sprite.Group()  
enemies = pygame.sprite.Group()  
bullets = pygame.sprite.Group()  

player = Player()  
all_sprites.add(player)  

# Spawn enemies  
for i in range(5):  
    enemy = Enemy()  
    all_sprites.add(enemy)  
    enemies.add(enemy)  

# Button function  
def draw_text(text, font, color, x, y):  
    label = font.render(text, True, color)  
    screen.blit(label, (x, y))  

def button(text, x, y, w, h, color, hover_color):  
    mouse = pygame.mouse.get_pos()  
    click = pygame.mouse.get_pressed()  

    if x < mouse[0] < x + w and y < mouse[1] < y + h:  
        pygame.draw.rect(screen, hover_color, (x, y, w, h))  
        if click[0] == 1:  
            return True  
    else:  
        pygame.draw.rect(screen, color, (x, y, w, h))  

    draw_text(text, font, WHITE, x + 20, y + 10)  
    return False  

# Game loop  
running = True  
clock = pygame.time.Clock()  

while running:  
    clock.tick(FPS)  

    # Process events ONCE per frame  
    events = pygame.event.get()  
    for event in events:  
        if event.type == pygame.QUIT:  
            running = False  

    # Check game state  
    if state == MENU:  
        screen.fill(BLACK)  
        draw_text("Strikers 1945", font, WHITE, WIDTH//2 - 80, 50)  

        # Buttons  
        if button("Play Game", 160, 200, 160, 50, BLUE, RED):  
            state = PLAYING  
        if button("Settings", 160, 300, 160, 50, BLUE, RED):  
            state = SETTINGS  
        if button("Exit", 160, 400, 160, 50, BLUE, RED):  
            running = False  

    elif state == PLAYING:  
        # Use events list to check keys (prevents missing input)  
        for event in events:  
            if event.type == pygame.QUIT:  
                running = False  
            if event.type == pygame.KEYDOWN:  
                if event.key == pygame.K_SPACE:  
                    player.shoot()  

        # Update  
        all_sprites.update()  

        # Check for collisions  
        hits = pygame.sprite.groupcollide(enemies, bullets, True, True)  
        for hit in hits:  
            enemy = Enemy()  
            all_sprites.add(enemy)  
            enemies.add(enemy)  

        # Draw  
        screen.fill(WHITE)  
        all_sprites.draw(screen)  

    elif state == SETTINGS:  
        screen.fill(BLACK)  
        draw_text("Settings (Coming Soon)", font, WHITE, WIDTH//2 - 100, HEIGHT//2 - 20)  

        if button("Back", 160, 500, 160, 50, BLUE, RED):  
            state = MENU  

    # Display update  
    pygame.display.flip()  

pygame.quit()  
import pygame  
import random  

# Pygame 초기화
pygame.init()

# 게임 창 크기
WIDTH, HEIGHT = 480, 640  
FPS = 60  

# 색상
WHITE = (255, 255, 255)  
RED = (255, 0, 0)  
BLACK = (0, 0, 0)  
BLUE = (0, 0, 255)  
GREEN = (0, 255, 0)  

# 게임 창 생성
screen = pygame.display.set_mode((WIDTH, HEIGHT))  
pygame.display.set_caption("Strikers 1945 Clone")  

# 이미지 로드
player_img = pygame.image.load("player.png")  
player_img = pygame.transform.scale(player_img, (50, 50))  

enemy_images = {
    "normal": pygame.image.load("enemy1.png"),
    "kamikaze": pygame.image.load("enemy2.png"),
    "shotgun": pygame.image.load("enemy3.png"),
    "sniper": pygame.image.load("enemy4.png"),
    "zigzag": pygame.image.load("enemy5.png")
}

# 폰트 설정
font = pygame.font.Font(None, 40)  

# 최대 체력
MAX_HP = 5

# 게임 상태
MENU = "menu"  
PLAYING = "playing"  
SETTINGS = "settings"  
state = MENU  

# 플레이어 클래스
class Player(pygame.sprite.Sprite):  
    def __init__(self):  
        super().__init__()  
        self.image = player_img  
        self.rect = self.image.get_rect()  
        self.rect.center = (WIDTH // 2, HEIGHT - 60)  
        self.speed = 5  
        self.hp = MAX_HP  
        self.invincible = False  
        self.invincible_timer = 0  

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

        # 무적 상태 업데이트
        if self.invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible = False  

    def shoot(self):  
        bullet = Bullet(self.rect.centerx, self.rect.top)  
        all_sprites.add(bullet)  
        bullets.add(bullet)  

    def take_damage(self):
        if not self.invincible:
            self.hp -= 1
            self.invincible = True
            self.invincible_timer = 60  # 1초 동안 무적

# 플레이어 총알 클래스
class Bullet(pygame.sprite.Sprite):  
    def __init__(self, x, y):  
        super().__init__()  
        self.image = pygame.Surface((5, 15))  
        self.image.fill(RED)  
        self.rect = self.image.get_rect()  
        self.rect.center = (x, y)  

    def update(self):  
        self.rect.y -= 10  
        if self.rect.bottom < 0:  
            self.kill()  

# 적 클래스 (일반 적)
class Enemy(pygame.sprite.Sprite):  
    def __init__(self, enemy_type):  
        super().__init__()  
        self.image = enemy_images[enemy_type]  
        self.rect = self.image.get_rect()  
        self.rect.x = random.randint(0, WIDTH - self.rect.width)  
        self.rect.y = random.randint(-100, -40)  
        self.speed = random.randint(2, 5)  
        self.enemy_type = enemy_type  

    def update(self):  
        self.rect.y += self.speed  
        if self.rect.top > HEIGHT:  
            self.kill()  

# 카미카제 적
class KamikazeEnemy(Enemy):
    def __init__(self):
        super().__init__("kamikaze")

    def update(self):
        super().update()
        if player.rect.centerx > self.rect.centerx:
            self.rect.x += 2
        elif player.rect.centerx < self.rect.centerx:
            self.rect.x -= 2

# 샷건 적
class ShotgunEnemy(Enemy):
    def __init__(self):
        super().__init__("shotgun")

    def update(self):
        super().update()
        if random.randint(1, 100) == 1:
            self.shoot()

    def shoot(self):
        for angle in [-10, 0, 10]:
            bullet = EnemyBullet(self.rect.centerx, self.rect.bottom, angle)
            all_sprites.add(bullet)
            enemy_bullets.add(bullet)

# 저격수 적
class SniperEnemy(Enemy):
    def __init__(self):
        super().__init__("sniper")

    def update(self):
        super().update()
        if random.randint(1, 150) == 1:
            bullet = EnemyBullet(self.rect.centerx, self.rect.bottom, 0)
            all_sprites.add(bullet)
            enemy_bullets.add(bullet)

# 지그재그 적
class ZigzagEnemy(Enemy):
    def __init__(self):
        super().__init__("zigzag")
        self.direction = random.choice([-3, 3])

    def update(self):
        super().update()
        self.rect.x += self.direction
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.direction *= -1

# 적 총알 클래스
class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        self.image = pygame.Surface((5, 15))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed_y = 5
        self.speed_x = angle / 2  

    def update(self):
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x
        if self.rect.top > HEIGHT:
            self.kill()

# 스프라이트 그룹 생성
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

# 적을 랜덤 생성할 때 올바르게 객체 생성하기
enemy_types = ["normal", "kamikaze", "shotgun", "sniper", "zigzag"]

for _ in range(5):
    enemy_type = random.choice(enemy_types)
    if enemy_type == "kamikaze":
        enemy = KamikazeEnemy()
    elif enemy_type == "shotgun":
        enemy = ShotgunEnemy()
    elif enemy_type == "sniper":
        enemy = SniperEnemy()
    elif enemy_type == "zigzag":
        enemy = ZigzagEnemy()
    else:  # "normal"
        enemy = Enemy("normal")

    all_sprites.add(enemy)
    enemies.add(enemy)

# 게임 루프
running = True  
clock = pygame.time.Clock()  

while running:  
    clock.tick(FPS)  

    events = pygame.event.get()  
    for event in events:  
        if event.type == pygame.QUIT:  
            running = False  
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:  
            player.shoot()  

    all_sprites.update()  

    # 충돌 감지
    for bullet in bullets:
        hits = pygame.sprite.spritecollide(bullet, enemies, True)
        if hits:
            bullet.kill()

    screen.fill(WHITE)
    all_sprites.draw(screen)  
    pygame.display.flip()  

pygame.quit()

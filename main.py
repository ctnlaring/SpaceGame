import pygame, sys, random
from pygame.locals import *
from fractions import Fraction

pygame.init()
pygame.mixer.init()
pygame.font.init
screen = pygame.display.set_mode((550, 600))
health=5
shots=0
misses=0
kills=0
deaths=0
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 550)
font = pygame.font.SysFont("monospace", 55)
pygame.display.set_caption('Space Game')
explosion=pygame.image.load("img/explosion.png")
explosionsnd = pygame.mixer.Sound('img/explosion.wav')
laser=pygame.mixer.Sound("img/laser.wav")
background = pygame.image.load("img/back.png")
healthlabel = font.render(str(health), 1, (255,255,255))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.image = pygame.image.load('img/ship.png').convert()
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.image.get_rect(
            center=(275,500))
    def update(self, pressed_keys):
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-6, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(6, 0)
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > 550:
            self.rect.right = 550
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= 600:
            self.rect.bottom = 600

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.image = pygame.image.load('img/enemy.png').convert()
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.image.get_rect(
            center=(random.randint(0,550-32),0))
    def update(self):
        global health
        global deaths
        self.rect.move_ip(0, 1.75)
        if self.rect.bottom > 500:
            self.kill()
            explosionsnd.play()
            for entity in enemies:
                screen.blit(entity.image, entity.rect)
            screen.blit(explosion, (player.rect.x-4,player.rect.y))
            pygame.display.flip()
            pygame.time.delay(150)
            health-=1
            deaths+=1


class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super(Bullet, self).__init__()
        self.image = pygame.image.load('img/bullet.png').convert()
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.image.get_rect(
            center=(player.rect.x+8,player.rect.y+8))
    def update(self):
        self.rect.move_ip(0, -8)
        if self.rect.right < 0:
            self.kill()

player = Player()
enemies = pygame.sprite.Group()
bullets=pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

while True:
    pygame.time.delay(20)
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                sys.exit()
            elif event.key == K_SPACE:
                laser.play()
                shots+=1
                new_bullet = Bullet()
                bullets.add(new_bullet)
                all_sprites.add(new_bullet)
        elif event.type == QUIT:
            sys.exit()
        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

    healthlabel = font.render(str(health), 1, (255,255,255))
    screen.blit(background, (0, 0))
    screen.blit(healthlabel, (500, 10))
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    enemies.update()
    bullets.update()
    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)
    if pygame.sprite.groupcollide(bullets, enemies, True, True, collided = None):
        kills+=1
    if health==0:
        kdr = Fraction(kills, deaths)
        hmr = Fraction(kills, shots-kills)
        kdrlabel = font.render("KDR - "+str(kdr.numerator)+":"+str(kdr.denominator), 1, (255,255,255))
        hmrlabel = font.render("HMR - "+str(hmr.numerator)+":"+str(hmr.denominator), 1, (255,255,255))
        screen.blit(background, (0,0))
        screen.blit(font.render("You Failed", 1, (255,255,255)), (50,150))
        screen.blit(kdrlabel, (50,250))
        screen.blit(hmrlabel, (50,350))
        pygame.display.flip()
        pygame.time.delay(5000)
        sys.exit()

    pygame.display.flip()

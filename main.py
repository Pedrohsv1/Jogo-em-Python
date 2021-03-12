import pygame
import random
import math
from pygame import mixer

# iniciando o pygame
pygame.init()

# criação da tela
screen = pygame.display.set_mode((800, 600))

#backgound
background = pygame.image.load('background1.png')

#background sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# title and Icon
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('001-ufo.png')
pygame.display.set_icon(icon)

# player
player_img = pygame.image.load('spaceship.png')
playerX = 370
playerY = 480
playerX_change = 0


# enemy
enemy_img = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemys = 6

for i in range(num_of_enemys):
    enemy_img.append(pygame.image.load('monster.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.3)
    enemyY_change.append(40)

# bullet
bullet_img = pygame.image.load('bullet (1).png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 1
bullet_state = 'ready'

#score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
texX = 10
texY = 10

#game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)


def game_over_text():
    over = over_font.render('GAME OVER', True, (255, 255, 255))
    screen.blit(over, (230, 250))


def show_score(x, y):
    score = font.render('Score : ' + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(player_img, (x, y))


def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bullet_img, (x + 16, y + 10))


def isCollision(enemyX, bulletX, enemyY, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# loop do jogo
running = True
while running:

    # RGB = Red - Green - Blue
    screen.fill((0, 10, 30,))

    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # se a tecla é direita ou esquerda
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.3
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.3
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    #player boundaries
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    #enemy movement
    for i in range(num_of_enemys):
        #game over
        if enemyY[i] > 440:
            for j in range(num_of_enemys):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] >= 736:
            enemyX_change[i] = -0.3
            if enemyY[i] > 150:
                enemyX_change[i] = -0.8
            elif enemyY[i] >100:
                enemyX_change[i] = -0.5

            enemyY[i] += enemyY_change[i]
        elif enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            if enemyY[i] > 150:
                enemyX_change[i] = 0.8
            elif enemyY[i] > 100:
                enemyX_change[i] = 0.5
            enemyY[i] += enemyY_change[i]
        # collision:
        collision = isCollision(enemyX[i], bulletX, enemyY[i], bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = 'ready'
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)
    #bullet moviment:
    if bulletY <= 0:
        bulletY = 480
        bullet_state = 'ready'
    if bullet_state == 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(texX, texY)
    pygame.display.update()

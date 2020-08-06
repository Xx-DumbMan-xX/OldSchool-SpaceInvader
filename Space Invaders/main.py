import pygame
import random
import math
from pygame import mixer

pygame.mixer.init()
pygame.font.init()
# Creating Screen for game
screen = pygame.display.set_mode((800, 600))

# Background for game
background = pygame.image.load('background.png')

# Background sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# title and icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('SpaceInvader Icon.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('SpaceInvaders Player.png')
playerX = 370
playerY = 500
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
enemy_num = 4

for i in range(enemy_num):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(30)

# Bullet
# Ready - Ready to fire but not visible on screen
# Fire - Firing the bullet and visible on screen
bulletImg = pygame.image.load('bullet.png')
bulletX = 370
bulletY = 500
bulletX_change = 0
bulletY_change = 10
bullet_state = 'ready'

# Score
score_value = 0
font = pygame.font.SysFont('Arial', 28)

textX = 10
textY = 10

# Game Over Text
game_over = pygame.font.SysFont('Arial', 64)


# Score Function
def show_score(x, y):
    score = font.render('Score :' + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


# Game Over Text Function
def game_over_text():
    over_text = game_over.render('GAME OVER', True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


# Player Function
def player(x, y):
    screen.blit(playerImg, (x, y))


# Enemy Function
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


# Bullet function
def bullet_fire(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 16, y + 10))


# Collision Function
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:

    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                bullet_sound = mixer.Sound('shoot.wav')
                bullet_sound.play()
                bulletX = playerX
                bullet_fire(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            playerX_change = 0

    # Player Boundary
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy Boundary
    for i in range(enemy_num):
        if enemyY[i] > 440:
            for j in range(enemy_num):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]
            # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = 'ready'
            score_value += 1

            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)
    # Bullet Boundary
    if bullet_state == 'fire':
        bullet_fire(bulletX, bulletY)
        bulletY -= bulletY_change
    if bulletY <= 0:
        bulletY = 500
        bullet_state = 'ready'

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()

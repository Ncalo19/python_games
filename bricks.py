import pygame
import sys
import random

pygame.init()

WIDTH = 900
HEIGHT = 600

PLAYER = (11, 68, 53)
ENEMY = (133, 32, 12)
score_color = (11, 68, 53)
BACKGROUND_COLOR = (244, 164, 96)

player_size = 50
player_pos = [WIDTH/2, HEIGHT-2*player_size]

enemy_size = 50
enemy_pos = [random.randint(0,WIDTH-enemy_size), 0]
enemy_list = [enemy_pos]

SPEED = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))

game_over = False

score = 0

clock = pygame.time.Clock()

def set_level(score, SPEED):
    SPEED = score/8 + 10
    return SPEED

def drop_enemies(enemy_list):
    delay = random.random()
    if len(enemy_list) < 10 and delay < .15:
        x_pos = random.randint(0, WIDTH-enemy_size)
        y_pos = 0
        enemy_list.append([x_pos, y_pos])

def draw_enemies(enemy_list):
    for enemy_pos in enemy_list:
            pygame.draw.rect(screen, ENEMY, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))

def update_enemy_positions(enemy_list, score):
    for idx, enemy_pos in enumerate(enemy_list):
        if enemy_pos[1] >= 0 and enemy_pos[1] < HEIGHT:
            enemy_pos[1] += SPEED
        else:
            enemy_list.pop(idx)
            score += 1
    return score

def collission_check(enemy_list, player_pos):
    for enemy_pos in enemy_list:
        if detect_collission(enemy_pos, player_pos):
            return True
    return False

def detect_collission(player_pos, enemy_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]

    e_x = enemy_pos[0]
    e_y = enemy_pos[1]

    if (e_x >= p_x and e_x < (p_x + player_size)) or (p_x >= e_x and p_x < (e_x+enemy_size)):
        if (e_y >= p_y and e_y < (p_y + player_size)) or (p_y >= e_y and p_y < (e_y + enemy_size)):
            return True
    return False

while not game_over:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            x = player_pos[0]
            y = player_pos[1]

            if event.key == pygame.K_LEFT:
                x -= player_size

            elif event.key == pygame.K_RIGHT:
                x += player_size

            player_pos = [x,y]

    screen.fill(BACKGROUND_COLOR)

    # update position of enemy
    # if enemy_pos[1] >= 0 and enemy_pos[1] < HEIGHT:
    #     enemy_pos[1] += SPEED
    # else:
    #     enemy_pos[0] = random.randint(0, WIDTH - enemy_size)
    #     enemy_pos[1] = 1

    if detect_collission(player_pos, enemy_pos):
        game_over = True
    myFont = pygame.font.SysFont("monospace", 35)
    drop_enemies(enemy_list)
    score = update_enemy_positions(enemy_list, score)
    SPEED = set_level(score, SPEED)
    text = "score:" + str(score)
    label = myFont.render(text, 1, score_color)
    screen.blit(label, (WIDTH-200, HEIGHT -40))

    if collission_check(enemy_list, player_pos):
        game_over = True
    if game_over is True:
        print(score)

    draw_enemies(enemy_list)
    pygame.draw.rect(screen, PLAYER, (player_pos[0], player_pos[1], player_size, player_size))

    clock.tick(30)



    pygame.display.update()

import sys
import pygame
import random

# color define
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 155, 0)

# window size
display_width = 400
display_height = 600

# snake block size
block_size = 10

# init pygame
pygame.init()
pygame.display.set_caption('My Snake Game')

gameDisplay = pygame.display.set_mode((display_width, display_height))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 20)

snake_unit = []
snake_body = []
snake_init_size = 0
snake_head = []
# default move step
step_x = 0
step_y = 0
# food
isEaten = True
# is finished
isFinished = False
# score
score = 0
message = ''
food_x = 0
food_y = 0

def init():
    global snake_unit, snake_body, snake_init_size, i, snake_head, step_x, step_y, isEaten, isFinished, score, message
    # snake unit (x, y), body is the list of the unit.
    snake_unit = []
    snake_body = []
    snake_init_size = 5
    # init snake
    for i in range(0, snake_init_size):
        snake_unit = [200 + i * block_size, 300]
        snake_body.append(snake_unit)
    snake_head = snake_body[snake_init_size - 1]
    # default move step
    step_x = block_size
    step_y = 0
    # food
    isEaten = True
    # is finished
    isFinished = False
    # score
    score = 0
    message = 'RUNNING'


def handle_key_event():
    global snake_size, step_x, step_y
    # handle key event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit(0)
            if event.key == pygame.K_SPACE:
                init()
                snake_size = len(snake_body)
            if event.key == pygame.K_DOWN:
                step_x = 0
                step_y = block_size
            if event.key == pygame.K_UP:
                step_x = 0
                step_y = -block_size
            if event.key == pygame.K_LEFT:
                step_x = -block_size
                step_y = 0
            if event.key == pygame.K_RIGHT:
                step_x = block_size
                step_y = 0


def check_status():
    global snake_size, isFinished, message, i
    snake_size = len(snake_body)
    # check game status
    if (snake_head[0] <= 0 or snake_head[0] >= display_width) or (
            snake_head[1] <= 0 or snake_head[1] >= display_height - 80):
        isFinished = True
        message = 'GOOD PLAY, GAME OVER!'
    # check if the snake bit himself
    for i in range(0, snake_size - 2):
        if snake_body[i][0] == snake_head[0] and snake_body[i][1] == snake_head[1]:
            isFinished = True
            message = 'YOU BITE YOURSELF!'
            break


def snake_move():
    global snake_head, isEaten, score, food_x, food_y
    if not isFinished:
        snake_head = [snake_body[snake_size - 1][0] + step_x, snake_body[snake_size - 1][1] + step_y]
        snake_body.append(snake_head)

        # check food status
        if food_x == snake_head[0] and food_y == snake_head[1]:
            isEaten = True
            score += 10
        else:
            del (snake_body[0])


def display_info():
    pygame.draw.line(gameDisplay, white, [0, display_height - 75], [display_width, display_height - 75], 2)
    info = font.render(f"SCORE:{score} | X:{snake_head[0]} Y:{snake_head[1]}", True, white)
    msg = font.render(f"MESSAGE:{message}", True, white)
    help = font.render(f"PRESS Q: QUITE GAME | PRESS SPACE: PLAY AGAIN", True, white)
    gameDisplay.blit(info, [10, display_height - 45])
    gameDisplay.blit(help, [10, display_height - 65])
    gameDisplay.blit(msg, [10, display_height - 25])


def draw_sname():
    global i
    # display
    # draw snake
    for i in snake_body:
        pygame.draw.rect(gameDisplay, green, [i[0], i[1], block_size, block_size])


def draw_food():
    global food_x, food_y, isEaten
    if isEaten:
        food_x = round(random.randrange(0, display_width - block_size) / 10.0) * 10.0
        food_y = round(random.randrange(0, display_height - block_size - 75) / 10.0) * 10.0
        isEaten = False
    # draw food
    pygame.draw.rect(gameDisplay, red, [food_x, food_y, block_size, block_size])


init()

while True:

    check_status()

    handle_key_event()

    gameDisplay.fill(black)
    clock.tick(20)

    snake_move()

    draw_food()

    draw_sname()

    display_info()

    pygame.display.flip()

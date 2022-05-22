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

# snake unit (x, y), body is the list of the unit.
snake_unit = []
snake_body = []
snake_size = 5
# init snake
for i in range(0, snake_size):
    snake_unit = [200 + i * block_size, 300]
    snake_body.append(snake_unit)
snake_head = snake_body[snake_size - 1]

# default move step
step_x = block_size
step_y = 0

# food
isEaten = True

# is finished
isFinished = False

# score
score = 0
message = 'Running'
while True:

    gameDisplay.fill(black)
    snake_size = len(snake_body)

    # check game status
    if (snake_head[0] <= 0 or snake_head[0] >= display_width) or (
            snake_head[1] <= 0 or snake_head[1] >= display_height - 30):
        isFinished = True
        message = 'GOOD PLAY, GAME OVER!'

    # handle key event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit(0)
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

    clock.tick(30)

    if not isFinished:
        snake_head = [snake_body[snake_size - 1][0] + step_x, snake_body[snake_size - 1][1] + step_y]
        snake_body.append(snake_head)

        if isEaten:
            food_x = round(random.randrange(0, display_width - block_size) / 10.0) * 10.0
            food_y = round(random.randrange(0, display_height - block_size - 30) / 10.0) * 10.0
            isEaten = False

        # draw food
        pygame.draw.rect(gameDisplay, red, [food_x, food_y, block_size, block_size])

        # check food status
        if food_x == snake_head[0] and food_y == snake_head[1]:
            isEaten = True
            score += 10
        else:
            del(snake_body[0])



    pygame.draw.line(gameDisplay, white, [0, display_height - 30], [display_width, display_height - 30], 2)
    text = font.render(f"SCORE:{score} | X:{snake_head[0]} Y:{snake_head[1]} | MESSAGE:{message}", True, white)
    gameDisplay.blit(text, [10, display_height - 25])

    # display
    # draw snake
    for i in snake_body:
        pygame.draw.rect(gameDisplay, green, [i[0], i[1], block_size, block_size])

    pygame.display.flip()

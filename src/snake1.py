import sys
import pygame

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
font = pygame.font.SysFont(None, 35)
font_large = pygame.font.SysFont(None, 75)

snake_unit = []
snake_body = []


for i in range(0, 10):
    snake_unit = [200 + i * block_size, 300]
    snake_body.append(snake_unit)

while True:
    snake_size = 10
    gameDisplay.fill(black)
    clock.tick(20)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_DOWN:
                snake_head = [snake_body[snake_size - 1][0], snake_body[snake_size - 1][1] + block_size]
                snake_body.append(snake_head)
                del(snake_body[0])

            if event.key == pygame.K_UP:
                snake_head = [snake_body[snake_size - 1][0], snake_body[snake_size - 1][1] - block_size]
                snake_body.append(snake_head)
                del(snake_body[0])

            if event.key == pygame.K_LEFT:
                snake_head = [snake_body[snake_size - 1][0] - block_size, snake_body[snake_size - 1][1]]
                snake_body.append(snake_head)
                del(snake_body[0])

            if event.key == pygame.K_RIGHT:
                snake_head = [snake_body[snake_size - 1][0] + block_size, snake_body[snake_size - 1][1]]
                snake_body.append(snake_head)
                del(snake_body[0])

    for i in snake_body:
        pygame.draw.rect(gameDisplay, green, [i[0], i[1], block_size, block_size])

    pygame.display.update()
    pygame.display.flip()

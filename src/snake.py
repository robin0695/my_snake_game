import sys
import pygame

# color define
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

while True:

    for i in range(0, 10):
        pygame.draw.rect(gameDisplay, green, [200 + i * block_size, 100, block_size, block_size])

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
    pygame.display.flip()

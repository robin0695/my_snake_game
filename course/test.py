
import sys
import pygame
import random

# 变量初始化
# snake的颜色
green = (0, 155, 0)
black = (0, 0, 0)
red = (255, 0, 0)
white = (255, 255, 255)

# snake block size
block_size = 10

# window size 初始化
display_width = 400
display_height = 600

# 初始化pygame，包括时钟，字体等
pygame.init()
pygame.mixer.init()
pygame.display.set_caption("My Snake Game")
game_display = pygame.display.set_mode((display_width, display_height))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 20)

# ---------------------------------------------------------------------
# 定义蛇的身体和节点的数据结构
# unit = [x, y] 节点的坐标。
# snake boday = [unit, unit ......]
snake_unit = []
snake_body = []
snake_body_size = 10
# 初始化蛇的身体
for i in range(0, snake_body_size) :
    snake_unit = [20 + i * block_size, 300]
    snake_body.append(snake_unit)
# ---------------------------------------------------------------------

# 移动的方向和数值
move_step = [block_size, 0]

# food
isEaten = True
food_x = 0
food_y = 0

# 游戏是否结束
is_finished = False

# 信息， 分数
msg_from_game = "Running..."
score = 0
level = 0
speed_up = 0
food_color = 255

# image
bg_img = pygame.image.load('bg.png')
bg_img = pygame.transform.scale(bg_img, (400, 520))

# music
food_music = 'music.mp3'
eat_food_sound = pygame.mixer.Sound(food_music)

back_music = 'background.mp3'
back_music_sound = pygame.mixer.Sound(back_music)
back_music_sound.play(-1)

# main loop，主循环
while True:
    
    # 画布填充黑色
    game_display.fill(black)
    game_display.blit(bg_img, (0, 0))
    
    # 设置时钟
    clock.tick(20 + level * 5 + speed_up)

    # 每次获取蛇的长度
    snake_body_size = len(snake_body)
    snake_head = snake_body[snake_body_size - 1]
    snake_head_new = [snake_head[0] + move_step[0], snake_head[1] + move_step[1]]

    if (snake_head[0] <= 0 or snake_head[0] >= display_width) or (snake_head[1] <= 0 or snake_head[1] >= display_height - 80):
        is_finished = True
        msg_from_game = "Good play, game over!"
        
    # 添加关闭窗口事件处理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("Close the window!")
            pygame.quit()
            sys.exit(0)

        # 处理键盘上下左右的事件，移动snake
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_DOWN, pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT):
                if event.key == pygame.K_DOWN:
                    move_step = [0, block_size]
                if event.key == pygame.K_UP:
                    move_step = [0, - block_size]
                if event.key == pygame.K_LEFT:
                    move_step = [-block_size, 0]
                if event.key == pygame.K_RIGHT:
                    move_step = [block_size, 0]
                # 增加刷新速度
                speed_up = 20
                print(snake_body)

            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit(0)
            
            if event.key == pygame.K_SPACE:
                # 重置游戏变量
                snake_unit = []
                snake_body = []
                snake_body_size = 10
                for i in range(0, snake_body_size) :
                    snake_unit = [20 + i * block_size, 300]
                    snake_body.append(snake_unit)
                move_step = [block_size, 0]
                isEaten = True
                is_finished = False
                msg_from_game = "Running..."
                score = 0
                level = 0
                snake_head = snake_body[snake_body_size - 1]
                snake_head_new = [snake_head[0] + move_step[0], snake_head[1] + move_step[1]]
            
        # 当按键抬起取消加速效果，只处理上下左右
        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_DOWN, pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT):
                speed_up = 0
                
    if not is_finished:
        snake_body.append(snake_head_new)

        # 画出食物
        if isEaten:
            food_x = round(random.randrange(0, display_width - block_size - 75) / 10) * 10
            food_y = round(random.randrange(0, display_height - block_size - 75) / 10) * 10
            isEaten = False
            
        if food_x == snake_head_new[0] and food_y == snake_head_new[1]:
            isEaten = True
            score += 10
            level = int(score / 100)
            eat_food_sound.play()
        else:
            del(snake_body[0])

    # 通过draw 矩形，形成蛇的身体 
    for i in snake_body:
        pygame.draw.rect(game_display, green, [i[0], i[1], block_size, block_size])
    
    food_color -= 20
    if food_color < 10:
        food_color = 255
    pygame.draw.rect(game_display, (255, food_color, food_color), [food_x, food_y, block_size, block_size])

    pygame.draw.line(game_display, white, [0, display_height - 75], [display_width, display_height - 75], 2)
    
    msg = font.render(f"MESSAGE:{msg_from_game}", True, white)
    info = font.render(f"SCORE:{score} | LEVEL:{level + 1}| X:{snake_head[0]} Y:{snake_head[1]}", True, white)
    help_message = font.render(f"Press Q to quite, SPACE to replay", True, white)
    game_display.blit(msg, [10, display_height - 25])
    game_display.blit(info, [10, display_height - 45])
    game_display.blit(help_message, [10, display_height - 65])

    # 更新画布，并翻页
    pygame.display.update()
    pygame.display.flip()
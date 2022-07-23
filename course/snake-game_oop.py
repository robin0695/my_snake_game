
import sys
import pygame
import random
from snake_client import SnakeClient

GREEN = (0, 155, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# window size 初始化
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600

class Snake:
    def __init__(self) -> None:
        self.block_size = 10
        snake_unit = []
        snake_body_size = 10
        self.snake_body = []
        # 初始化蛇的身体
        for i in range(0, snake_body_size) :
            snake_unit = [20 + i * self.block_size, 300]
            self.snake_body.append(snake_unit)

        food_music = 'course/music.mp3'
        self.eat_food_sound = pygame.mixer.Sound(food_music)

    def move(self, move_step, eat_food):
        # 每次获取蛇的长度
        snake_body_size = len(self.snake_body)
        snake_head = self.snake_body[snake_body_size - 1]
        snake_head_new = [snake_head[0] + move_step[0], snake_head[1] + move_step[1]]
        self.snake_body.append(snake_head_new)
        if not eat_food:
            del(self.snake_body[0])
        else:
            self.eat_food_sound.play()
        return self.snake_body
    
    def get_snake_body(self):
        return self.snake_body
    
    def get_snake_unit_size(self):
        return self.block_size

    def get_snake_size(self):
        return len(self.snake_body)

    def get_snake_head(self):
        return self.snake_body[len(self.snake_body) - 1]
    
    def draw(self, game_display):
        # 通过draw 矩形，形成蛇的身体 
        for i in self.snake_body:
            pygame.draw.rect(game_display, GREEN, [i[0], i[1], self.block_size, self.block_size])

    def draw_shadow(self, game_display, new_snake_body):
        # 通过draw 矩形，形成蛇的身体 
        for i in new_snake_body:
            pygame.draw.rect(game_display, (176, 224, 230), [i[0] + DISPLAY_WIDTH / 2, i[1], self.block_size, self.block_size])
        
        
class Food:
    def __init__(self, x, y, basic_color) -> None:
        self.block_size = 10
        self.x = x
        self.y = y
        self.count = 0
        self.basic_color = basic_color
        self.food_color_incr = 255
        food_cod_temp = self.__gen_cod()
        self.food_cod = [food_cod_temp[0], food_cod_temp[1]]

    def __gen_cod(self):
        food_x = round(random.randrange(0, self.x - self.block_size - 75) / 10) * 10
        food_y = round(random.randrange(0, self.y - self.block_size - 75) / 10) * 10
        return [food_x, food_y]

    def refresh(self):
        food_cod_temp = self.__gen_cod()
        self.food_cod = [food_cod_temp[0], food_cod_temp[1]]
        return self.food_cod
        
    def food_eaten(self):
        self.count += 1
        return self.refresh()

    def get_food_count(self):
        return self.count

    def get_food_cod(self):
        return self.food_cod
    
    def draw(self, game_display):
        self.food_color_incr -= 10
        if self.food_color_incr <= 0:
            self.food_color_incr = 255
        pygame.draw.rect(game_display, (self.basic_color, self.food_color_incr, self.food_color_incr),
                         [self.food_cod[0], self.food_cod[1], self.block_size, self.block_size])

    def draw_shadow(self, game_dispaly, cod):
        pygame.draw.rect(game_dispaly, (135,38,87), [cod[0] + DISPLAY_WIDTH / 2, cod[1], self.block_size, self.block_size])
        

class GameInfo:
    def __init__(self, y) -> None:
        self.y = y

    def draw(self, game_display, font, score, level, snake_head, message, com_score):
        pygame.draw.line(game_display, WHITE, [0, DISPLAY_HEIGHT - self.y], [DISPLAY_WIDTH, DISPLAY_HEIGHT - self.y], 2)
        pygame.draw.line(game_display, WHITE, [DISPLAY_WIDTH / 2, 0], [DISPLAY_WIDTH / 2, DISPLAY_HEIGHT - self.y], 2)
        msg = font.render(f"MESSAGE:{message}", True, WHITE)
        if com_score:
            info = font.render(f"SCORE:{score} vs COMPETITOR SCORE:{com_score}| LEVEL:{level + 1}| X:{snake_head[0]} Y:{snake_head[1]}", True, WHITE)
        else:
            info = font.render(f"SCORE:{score} | LEVEL:{level + 1}| X:{snake_head[0]} Y:{snake_head[1]}", True, WHITE)

        help_message = font.render(f"Press Q to quite, SPACE to replay", True, WHITE)
        game_display.blit(msg, [10, DISPLAY_HEIGHT - (self.y - 50)])
        game_display.blit(info, [10, DISPLAY_HEIGHT - (self.y - 30)])
        game_display.blit(help_message, [10, DISPLAY_HEIGHT - (self.y - 10)])


class GameManager:
    def __init__(self, game_display) -> None:
        self.snake = Snake()
        self.food = Food(DISPLAY_WIDTH / 2, DISPLAY_HEIGHT, 255)
        self.game_display = game_display
        self.move_step = [self.snake.get_snake_unit_size(), 0]
        self.game_info = GameInfo(75)
        self.font = pygame.font.SysFont(None, 20)
        self.single = False
        try:
            self.nt_client = SnakeClient()
            self.nt_client.connect()
            self.nt_client.start()
        except ConnectionRefusedError as e:
            print(e)
            self.single = True
            pass
            
    
    def work(self):

        snake_shadow = []
        food_shadow = []
        if not self.check_game_over():
            message = "Running...."
            if self.check_eat_food() :
                self.snake.move(self.move_step, True)
                food_shadow = self.food.food_eaten()
            else:
                self.snake.move(self.move_step, False)
            self.food.draw(self.game_display)
        else:
            message = "Good play, game over!"
            
        self.snake.draw(self.game_display)
        
        # draw shadow
        snake_shadow = self.nt_client.get_competitor_snake()
        food_shadow = self.nt_client.get_competitor_food()
        if snake_shadow:
            self.snake.draw_shadow(self.game_display, snake_shadow)
        if food_shadow:
            self.food.draw_shadow(self.game_display, food_shadow)
            
        self.game_info.draw(self.game_display, self.font, self.food.get_food_count() * 10, 
                            int(self.food.get_food_count() / 10), self.snake.get_snake_head(), message, self.nt_client.get_competitor_score())

        # send snake body
        if not self.single:
            body_dic = []
            for s in self.snake.get_snake_body():
                body_dic.append({'x':s[0], 'y':s[1]})

            snake_data = {'snake_body':body_dic}
            snake_data['snake_food']={'x': self.food.get_food_cod()[0], 'y': self.food.get_food_cod()[1]}
            snake_data['score'] = f'{self.food.get_food_count() * 10}'
            try:
                self.nt_client.send_message(snake_data)
            except ConnectionResetError as e:
                print("lost connection, play as single player.")
                self.single=True

   
    def handle_key_down(self, key):
        if key in (pygame.K_DOWN, pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT):
            if key == pygame.K_DOWN:
                move_step = [0, self.snake.get_snake_unit_size()]
            if key == pygame.K_UP:
                move_step = [0, - self.snake.get_snake_unit_size()]
            if key == pygame.K_LEFT:
                move_step = [-self.snake.get_snake_unit_size(), 0]
            if key == pygame.K_RIGHT:
                move_step = [self.snake.get_snake_unit_size(), 0]
            self.move_step = move_step
    def check_eat_food(self):
        if  self.snake.get_snake_head()[0] == self.food.get_food_cod()[0] and \
            self.snake.get_snake_head()[1] == self.food.get_food_cod()[1]:
            return True
        else:
            return False
            
    def check_game_over(self):
        if  (self.snake.get_snake_head()[0] <= 0 or self.snake.get_snake_head()[0] >= DISPLAY_WIDTH / 2 - 10) or \
            (self.snake.get_snake_head()[1] <= 0 or self.snake.get_snake_head()[1] >= DISPLAY_HEIGHT - 80):
            return True
    
    def close(self):
        self.nt_client.disconnect()

class Game:
    def __init__(self) -> None:
        # 初始化pygame，包括时钟，字体等
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("My Snake Game")
        self.game_display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        self.clock = pygame.time.Clock()
        self.gameManager = GameManager(self.game_display)

        bg_img = pygame.image.load('course/bg.png')
        self.bg_image = pygame.transform.scale(bg_img, (400, 525))

        back_music = 'course/background.mp3'
        back_music_sound = pygame.mixer.Sound(back_music)
        back_music_sound.play(-1)
    
    def play(self):
        while True:
            self.clock.tick(20)
            self.game_display.fill(BLACK)
            pygame.draw.rect(self.game_display, (41, 36, 33), [ DISPLAY_WIDTH / 2, 0, DISPLAY_WIDTH / 2, DISPLAY_HEIGHT - 75])
            self.game_display.blit(self.bg_image, (0, 0))
            # 添加关闭窗口事件处理
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Close the window!")
                    self.gameManager.close()
                    pygame.quit()
                    sys.exit(0)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.gameManager = GameManager(self.game_display)
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit(0)
                    else:
                        self.gameManager.handle_key_down(event.key)
                
            # 更新画布，并翻页
            self.gameManager.work()
            pygame.display.update()
            pygame.display.flip()

game = Game()
game.play()
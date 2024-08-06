import pygame
import sys
import random
import emoji

# 初始化pygame
pygame.init()

# 设置游戏窗口大小
window_width = 800
window_height = 600
cell_size = 20

# 定义颜色
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)

# 彩虹颜色
rainbow_colors = [
    (255, 0, 0), (255, 127, 0), (255, 255, 0), (0, 255, 0),
    (0, 0, 255), (75, 0, 130), (143, 0, 255)
]

# 创建游戏窗口
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('贪吃蛇游戏')

# 定义贪吃蛇和食物
snake = [(window_width // 2, window_height // 2)]
snake_direction = 'RIGHT'

# 食物表情
food_emojis = [emoji.emojize(':beer_mug:'), emoji.emojize(':bread:'), emoji.emojize(':red_apple:')]

def create_food():
    return (random.randint(0, window_width//cell_size-1)*cell_size, 
            random.randint(0, window_height//cell_size-1)*cell_size)

food = create_food()
special_food = None

clock = pygame.time.Clock()

# 创建得分变量和速度变量
score = 0
speed = 10

# 字体设置
font = pygame.font.Font(None, 36)

def draw_score():
    score_surface = font.render(f'得分: {score}', True, white)
    window.blit(score_surface, (10, 10))

def game_over():
    game_over_surface = font.render(f'游戏结束! 得分: {score}', True, white)
    window.blit(game_over_surface, (window_width//2 - 100, window_height//2 - 50))
    pygame.display.update()
    pygame.time.wait(1000)
    for i in range(3, 0, -1):
        window.fill(black)
        countdown_surface = font.render(f'{i}', True, white)
        window.blit(countdown_surface, (window_width//2 - 10, window_height//2 - 20))
        pygame.display.update()
        pygame.time.wait(1000)
    return init_game()

def init_game():
    return [(window_width // 2, window_height // 2)], 'RIGHT', create_food(), None, 0, 10

# 游戏主循环
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_direction != 'DOWN':
                snake_direction = 'UP'
            elif event.key == pygame.K_DOWN and snake_direction != 'UP':
                snake_direction = 'DOWN'
            elif event.key == pygame.K_LEFT and snake_direction != 'RIGHT':
                snake_direction = 'LEFT'
            elif event.key == pygame.K_RIGHT and snake_direction != 'LEFT':
                snake_direction = 'RIGHT'

    # 移动贪吃蛇
    head = snake[0]
    x, y = head
    if snake_direction == 'UP':
        new_head = (x, y - cell_size)
    elif snake_direction == 'DOWN':
        new_head = (x, y + cell_size)
    elif snake_direction == 'LEFT':
        new_head = (x - cell_size, y)
    elif snake_direction == 'RIGHT':
        new_head = (x + cell_size, y)

    # 检查是否撞墙
    if (new_head[0] < 0 or new_head[0] >= window_width or
        new_head[1] < 0 or new_head[1] >= window_height):
        snake, snake_direction, food, special_food, score, speed = game_over()
        continue

    snake.insert(0, new_head)

    # 检查是否吃到食物
    if new_head == food:
        food = create_food()
        score += 10
        speed += 0.5
        if random.random() < 0.2:  # 20%的概率生成特殊食物
            special_food = create_food()
    elif special_food and new_head == special_food:
        special_food = None
        score += 20
        speed -= 0.3 if speed > 10 else 0
    else:
        snake.pop()

    # 渲染背景
    window.fill(black)

    # 绘制贪吃蛇
    for i, segment in enumerate(snake):
        color = rainbow_colors[i % len(rainbow_colors)]
        pygame.draw.rect(window, color, (segment[0], segment[1], cell_size, cell_size))

    # 绘制食物
    food_emoji = random.choice(food_emojis)
    food_surface = font.render(food_emoji, True, white)
    window.blit(food_surface, (food[0], food[1]))

    # 绘制特殊食物
    if special_food:
        pygame.draw.rect(window, blue, (special_food[0], special_food[1], cell_size, cell_size))

    # 显示得分
    draw_score()

    # 更新窗口
    pygame.display.update()

    clock.tick(speed)  # 控制帧率
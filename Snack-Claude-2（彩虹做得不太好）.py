import pygame
import sys
import random
import time

# 初始化pygame
pygame.init()

# 设置游戏窗口大小
window_width = 800
window_height = 600
cell_size = 20

# 定义颜色
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

# 创建游戏窗口
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('贪吃蛇游戏')

# 定义贪吃蛇和食物
snake = [(400, 300)]
snake_direction = 'RIGHT'
food = (random.randint(0, (window_width-cell_size)//cell_size)*cell_size, 
        random.randint(0, (window_height-cell_size)//cell_size)*cell_size)

# 特殊食物
special_food = None
special_food_timer = 0

clock = pygame.time.Clock()

# 创建得分变量和速度变量
score = 0
speed = 10

# 创建字体对象
font = pygame.font.Font(None, 36)

# 生成彩虹颜色
def rainbow_color(i):
    r = int((1 + i * 0.1) * 127) % 256
    g = int((2 + i * 0.1) * 127) % 256
    b = int((3 + i * 0.1) * 127) % 256
    return (r, g, b)

# 游戏结束函数
def game_over():
    global snake, snake_direction, food, special_food, score, speed
    
    # 显示最终得分
    score_text = font.render(f"Final Score: {score}", True, white)
    text_rect = score_text.get_rect(center=(window_width/2, window_height/2))
    window.blit(score_text, text_rect)
    pygame.display.update()
    
    # 3秒倒计时
    for i in range(3, 0, -1):
        window.fill(black)
        window.blit(score_text, text_rect)
        countdown_text = font.render(str(i), True, white)
        countdown_rect = countdown_text.get_rect(center=(window_width/2, window_height/2 + 50))
        window.blit(countdown_text, countdown_rect)
        pygame.display.update()
        time.sleep(1)
    
    # 重置游戏
    snake = [(400, 300)]
    snake_direction = 'RIGHT'
    food = (random.randint(0, (window_width-cell_size)//cell_size)*cell_size, 
            random.randint(0, (window_height-cell_size)//cell_size)*cell_size)
    special_food = None
    score = 0
    speed = 10

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
        game_over()
        continue

    snake.insert(0, new_head)  # 将新的头部添加到贪吃蛇

    # 检查是否吃到食物
    if new_head == food:
        food = (random.randint(0, (window_width-cell_size)//cell_size)*cell_size, 
                random.randint(0, (window_height-cell_size)//cell_size)*cell_size)
        score += 10
        speed += 0.5  # 增加速度
    elif new_head == special_food:
        special_food = None
        score += 50
        speed += 1  # 增加更多速度
    else:
        snake.pop()  # 如果没有吃到食物，移除尾部

    # 特殊食物逻辑
    if special_food is None and random.randint(1, 100) == 1:
        special_food = (random.randint(0, (window_width-cell_size)//cell_size)*cell_size, 
                        random.randint(0, (window_height-cell_size)//cell_size)*cell_size)
        special_food_timer = 100  # 特殊食物持续100帧
    elif special_food:
        special_food_timer -= 1
        if special_food_timer <= 0:
            special_food = None

    # 渲染背景
    window.fill(black)

    # 绘制贪吃蛇
    for i, segment in enumerate(snake):
        pygame.draw.rect(window, rainbow_color(i), (segment[0], segment[1], cell_size, cell_size))

    # 绘制食物
    pygame.draw.rect(window, red, (food[0], food[1], cell_size, cell_size))

    # 绘制特殊食物
    if special_food:
        pygame.draw.rect(window, blue, (special_food[0], special_food[1], cell_size, cell_size))

    # 显示得分
    score_text = font.render(f"Score: {score}", True, white)
    window.blit(score_text, (10, 10))

    # 更新窗口
    pygame.display.update()

    clock.tick(speed)  # 控制帧率
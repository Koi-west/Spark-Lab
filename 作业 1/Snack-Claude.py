import pygame
import sys
import random

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
snake = [(200, 200)]
snake_direction = 'RIGHT'
food = (random.randint(0, window_width//cell_size-1)*cell_size, 
        random.randint(0, window_height//cell_size-1)*cell_size)

clock = pygame.time.Clock()

# 创建得分变量
score = 0

# 创建字体对象
font = pygame.font.Font(None, 36)

# 初始速度
speed = 10

# 特殊道具
special_food = None
special_food_timer = 0

def game_over():
    text = font.render("游戏结束! 得分: " + str(score), True, white)
    text_rect = text.get_rect(center=(window_width/2, window_height/2))
    window.blit(text, text_rect)
    pygame.display.update()
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()

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

    # 检查是否撞到自己
    if new_head in snake[1:]:
        game_over()

    snake.insert(0, new_head)  # 将新的头部添加到贪吃蛇

    # 检查是否吃到食物
    if new_head == food:
        food = (random.randint(0, window_width//cell_size-1)*cell_size, 
                random.randint(0, window_height//cell_size-1)*cell_size)
        score += 10  # 增加得分
        speed += 0.5  # 增加速度
    else:
        snake.pop()  # 如果没有吃到食物，移除尾部

    # 特殊道具逻辑
    if special_food is None and random.random() < 0.02:  # 2%的几率生成特殊道具
        special_food = (random.randint(0, window_width//cell_size-1)*cell_size, 
                        random.randint(0, window_height//cell_size-1)*cell_size)
        special_food_timer = 50  # 特殊道具持续50帧

    if special_food:
        if new_head == special_food:
            score += 50  # 特殊道具得分更高
            speed -= 1  # 减慢速度
            special_food = None
        else:
            special_food_timer -= 1
            if special_food_timer <= 0:
                special_food = None

    # 渲染背景
    window.fill(black)

    # 绘制贪吃蛇
    for segment in snake:
        pygame.draw.rect(window, green, (segment[0], segment[1], cell_size, cell_size))

    # 绘制食物
    pygame.draw.rect(window, red, (food[0], food[1], cell_size, cell_size))

    # 绘制特殊道具
    if special_food:
        pygame.draw.rect(window, blue, (special_food[0], special_food[1], cell_size, cell_size))

    # 显示得分
    score_text = font.render(f"得分: {score}", True, white)
    window.blit(score_text, (10, 10))

    # 更新窗口
    pygame.display.update()

    clock.tick(speed)  # 控制帧率
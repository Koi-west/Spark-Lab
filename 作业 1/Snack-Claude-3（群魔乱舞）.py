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
red = (255, 0, 0)
blue = (0, 0, 255)

# 创建游戏窗口
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('彩虹蛇游戏')

# 创建字体对象
font = pygame.font.Font(None, 36)

# 定义彩虹颜色
rainbow_colors = [
    (255, 0, 0),    # 红
    (255, 127, 0),  # 橙
    (255, 255, 0),  # 黄
    (0, 255, 0),    # 绿
    (0, 0, 255),    # 蓝
    (75, 0, 130),   # 靛
    (143, 0, 255)   # 紫
]

def init_game():
    global snake, snake_direction, food, score, speed, special_food, special_food_timer, ai_snakes
    snake = [(200, 200)]
    snake_direction = 'RIGHT'
    food = get_random_position()
    score = 0
    speed = 10
    special_food = None
    special_food_timer = 0
    ai_snakes = [create_ai_snake() for _ in range(3)]  # 创建3条AI蛇

def get_random_position():
    return (random.randint(0, window_width//cell_size-1)*cell_size, 
            random.randint(0, window_height//cell_size-1)*cell_size)

def create_ai_snake():
    length = random.randint(3, 10)
    head = get_random_position()
    direction = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
    body = [head]
    for _ in range(length - 1):
        if direction == 'UP':
            body.append((body[-1][0], body[-1][1] + cell_size))
        elif direction == 'DOWN':
            body.append((body[-1][0], body[-1][1] - cell_size))
        elif direction == 'LEFT':
            body.append((body[-1][0] + cell_size, body[-1][1]))
        elif direction == 'RIGHT':
            body.append((body[-1][0] - cell_size, body[-1][1]))
    return {'body': body, 'direction': direction}

def move_ai_snake(ai_snake):
    head = ai_snake['body'][0]
    direction = ai_snake['direction']
    if random.random() < 0.1:  # 10%的几率改变方向
        direction = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
    
    if direction == 'UP':
        new_head = (head[0], head[1] - cell_size)
    elif direction == 'DOWN':
        new_head = (head[0], head[1] + cell_size)
    elif direction == 'LEFT':
        new_head = (head[0] - cell_size, head[1])
    elif direction == 'RIGHT':
        new_head = (head[0] + cell_size, head[1])
    
    # 如果新头部超出边界，则从对面出现
    new_head = (new_head[0] % window_width, new_head[1] % window_height)
    
    ai_snake['body'].insert(0, new_head)
    ai_snake['body'].pop()
    ai_snake['direction'] = direction

def draw_snake(snake_body):
    for i, segment in enumerate(snake_body):
        color = rainbow_colors[i % len(rainbow_colors)]
        pygame.draw.rect(window, color, (segment[0], segment[1], cell_size, cell_size))

def game_over():
    global running
    text = font.render("游戏结束! 得分: " + str(score), True, white)
    text_rect = text.get_rect(center=(window_width/2, window_height/2 - 50))
    window.blit(text, text_rect)
    
    restart_text = font.render("点击此处重新开始", True, white)
    restart_rect = restart_text.get_rect(center=(window_width/2, window_height/2 + 50))
    window.blit(restart_text, restart_rect)
    
    pygame.display.update()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_rect.collidepoint(event.pos):
                    init_game()
                    waiting = False

init_game()
clock = pygame.time.Clock()

# 游戏主循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_direction != 'DOWN':
                snake_direction = 'UP'
            elif event.key == pygame.K_DOWN and snake_direction != 'UP':
                snake_direction = 'DOWN'
            elif event.key == pygame.K_LEFT and snake_direction != 'RIGHT':
                snake_direction = 'LEFT'
            elif event.key == pygame.K_RIGHT and snake_direction != 'LEFT':
                snake_direction = 'RIGHT'

    # 移动玩家的蛇
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

    # 如果新头部超出边界，则从对面出现
    new_head = (new_head[0] % window_width, new_head[1] % window_height)

    snake.insert(0, new_head)  # 将新的头部添加到贪吃蛇

    # 检查是否吃到食物
    if new_head == food:
        food = get_random_position()
        score += 10  # 增加得分
        speed += 0.5  # 增加速度
    else:
        snake.pop()  # 如果没有吃到食物，移除尾部

    # 特殊道具逻辑
    if special_food is None and random.random() < 0.02:  # 2%的几率生成特殊道具
        special_food = get_random_position()
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

    # 移动和检查AI蛇
    for ai_snake in ai_snakes:
        move_ai_snake(ai_snake)
        if new_head in ai_snake['body']:
            # 玩家的蛇吃掉AI蛇
            score += len(ai_snake['body']) * 5
            food = ai_snake['body'][0]  # AI蛇的头变成食物
            ai_snakes.remove(ai_snake)
            ai_snakes.append(create_ai_snake())  # 创建新的AI蛇

    # 渲染背景
    window.fill(black)

    # 绘制玩家的蛇
    draw_snake(snake)

    # 绘制AI蛇
    for ai_snake in ai_snakes:
        draw_snake(ai_snake['body'])

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

    # 检查是否撞墙
    if (new_head[0] < 0 or new_head[0] >= window_width or
        new_head[1] < 0 or new_head[1] >= window_height):
        game_over()

pygame.quit()
sys.exit()
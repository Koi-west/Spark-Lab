import pygame
import random

# 初始化 Pygame
pygame.init()

# 设置窗口大小
width = 800
height = 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("贪吃蛇")

# 颜色定义
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)

# 蛇和食物的大小
block_size = 20

# 初始化蛇
snake = [(width/2, height/2)]
snake_direction = (block_size, 0)

# 生成食物
def generate_food():
    while True:
        food = (random.randrange(0, width, block_size),
                random.randrange(0, height, block_size))
        if food not in snake:
            return food

food = generate_food()

# 游戏主循环
clock = pygame.time.Clock()
game_over = False

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and snake_direction[0] == 0:
                snake_direction = (-block_size, 0)
            elif event.key == pygame.K_RIGHT and snake_direction[0] == 0:
                snake_direction = (block_size, 0)
            elif event.key == pygame.K_UP and snake_direction[1] == 0:
                snake_direction = (0, -block_size)
            elif event.key == pygame.K_DOWN and snake_direction[1] == 0:
                snake_direction = (0, block_size)

    # 移动蛇
    new_head = (snake[0][0] + snake_direction[0], snake[0][1] + snake_direction[1])
    snake.insert(0, new_head)

    # 检查是否吃到食物
    if snake[0] == food:
        food = generate_food()
    else:
        snake.pop()

    # 检查游戏是否结束
    if (snake[0][0] < 0 or snake[0][0] >= width or
        snake[0][1] < 0 or snake[0][1] >= height or
        snake[0] in snake[1:]):
        game_over = True

    # 绘制游戏画面
    window.fill(black)
    for segment in snake:
        pygame.draw.rect(window, green, (segment[0], segment[1], block_size, block_size))
    pygame.draw.rect(window, red, (food[0], food[1], block_size, block_size))
    pygame.display.update()

    # 控制游戏速度
    clock.tick(10)

pygame.quit()
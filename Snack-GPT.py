
import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Set game window size
window_width = 800
window_height = 600
cell_size = 20

# Define colors
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)

# Create game window
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('贪吃蛇游戏')

# Define snake and food
snake = [(200, 200)]
snake_direction = 'RIGHT'
food = (random.randint(0, window_width//cell_size-1)*cell_size, 
        random.randint(0, window_height//cell_size-1)*cell_size)

clock = pygame.time.Clock()

# Create score variable
score = 0

# Define font for score display
font = pygame.font.SysFont(None, 35)

# Function to display the score on the screen
def show_score():
    score_text = font.render(f"Score: {score}", True, white)
    window.blit(score_text, [10, 10])

# Function to check if snake hits itself
def check_collision():
    head = snake[0]
    if head in snake[1:]:
        return True
    return False

# Define special items
special_items = []
special_item_timer = 0

# Game main loop
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

    # Move the snake
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
    
    snake = [new_head] + snake[:-1]
    
    # Check for collisions with the wall
    if (x < 0 or x >= window_width or y < 0 or y >= window_height) or check_collision():
        break  # Game over if collision occurs

    # Check if snake eats the food
    if new_head == food:
        score += 1
        snake.append(snake[-1])  # Increase the length of the snake
        food = (random.randint(0, window_width//cell_size-1)*cell_size, 
                random.randint(0, window_height//cell_size-1)*cell_size)
        # Increase speed
        clock.tick(10 + score)

    # Spawn special items occasionally
    special_item_timer += 1
    if special_item_timer > 100:  # Every 100 frames
        special_item_timer = 0
        special_item_position = (random.randint(0, window_width//cell_size-1)*cell_size, 
                                 random.randint(0, window_height//cell_size-1)*cell_size)
        special_items.append(special_item_position)
    
    # Check if snake eats a special item
    for item in special_items:
        if new_head == item:
            special_items.remove(item)
            # Random effect: either speed up or slow down
            if random.choice([True, False]):
                clock.tick(20 + score)  # Speed up
            else:
                clock.tick(5 + score)  # Slow down
    
    # Draw everything
    window.fill(black)
    for segment in snake:
        pygame.draw.rect(window, green, pygame.Rect(segment[0], segment[1], cell_size, cell_size))
    pygame.draw.rect(window, red, pygame.Rect(food[0], food[1], cell_size, cell_size))
    for item in special_items:
        pygame.draw.rect(window, white, pygame.Rect(item[0], item[1], cell_size, cell_size))

    # Display score
    show_score()

    # Update the display
    pygame.display.update()

    # Set the speed of the game
    clock.tick(10 + score)

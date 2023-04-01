import pygame
import random
import pickle

# Initialize Pygame
pygame.init()

# Set up the game window
window_width = 500
window_height = 550  # add extra height for the score display
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Snake Game")

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)

# Set up the game board
cell_size = 10
board_width = window_width // cell_size
board_top = 50  # set the top of the game board to 50 pixels
board_height = (window_height - board_top) // cell_size  # subtract 50 for the score display

# Set up a direction
directions = ["right", "left", "up", "down"]

# Set up the clock
clock = pygame.time.Clock()

# Set up the font
score_font = pygame.font.SysFont(None, 40)


# Reset the game state:
def reset_game():
    initial_snake = [(board_width // 2, board_height // 2)]
    initial_snake_direction = random.choice(directions)
    initial_spawn_food = (random.randint(1, board_width - 2), random.randint((board_top // cell_size) + 1, board_height - 1))
    initial_score = 0

    return initial_snake, initial_snake_direction, initial_spawn_food, initial_score


# Load the best score:
def load_best_score():
    try:
        with open("best_score.pickle", "rb") as bs:
            best_score_loaded = pickle.load(bs)
            return best_score_loaded
    except (OSError, IOError) as e:
        return 0


snake, snake_direction, food, score = reset_game()

# Set up the best score:
best_score = load_best_score()

# Game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and snake_direction != "right":
                snake_direction = "left"
            elif event.key == pygame.K_RIGHT and snake_direction != "left":
                snake_direction = "right"
            elif event.key == pygame.K_UP and snake_direction != "down":
                snake_direction = "up"
            elif event.key == pygame.K_DOWN and snake_direction != "up":
                snake_direction = "down"

    # Move the snake
    head_x, head_y = snake[0]
    if snake_direction == "left":
        head_x -= 1
    elif snake_direction == "right":
        head_x += 1
    elif snake_direction == "up":
        head_y -= 1
    elif snake_direction == "down":
        head_y += 1
    snake.insert(0, (head_x, head_y))

    # Check for collision with food
    if snake[0] == food:
        food = (random.randint(1, board_width - 2), random.randint((board_top // cell_size) + 1, board_height - 1))
        score += 1
        if score > best_score:
            best_score = score
            with open("best_score.pickle", "wb") as f:
                pickle.dump(score, f)
    else:
        snake.pop()

    # Check for collision with walls or snake's body
    if (head_x <= 0 or head_x >= (board_width - 1) or head_y <= 5 or head_y >= (board_height + 4) or
            (head_x, head_y) in snake[1:]):
        snake, snake_direction, food, score = reset_game()

    # Draw the game board
    window.fill(white)
    # Draw the border
    pygame.draw.rect(window, black, (0, board_top, window_width, cell_size))  # Top border
    pygame.draw.rect(window, black, (0, 0, cell_size, window_height))  # Left border
    pygame.draw.rect(window, black, (0, window_height - cell_size, window_width, cell_size))  # Bottom border
    pygame.draw.rect(window, black, (window_width - cell_size, 0, cell_size, window_height))  # Right border
    # Draw the snake
    for cell in snake:
        pygame.draw.rect(window, green, (cell[0] * cell_size, cell[1] * cell_size, cell_size, cell_size))
    # Draw the food
    pygame.draw.rect(window, red, (food[0] * cell_size, food[1] * cell_size, cell_size, cell_size))
    # Draw the score on the screen
    score_text = score_font.render('Score: ' + str(score), True, red)
    window.blit(score_text, (10, 10))
    # Draw the best score on the screen
    best_score_text = score_font.render('Best Score: ' + str(best_score), True, green)
    window.blit(best_score_text, (300, 10))

    # Update the display
    pygame.display.update()

    # Set the game speed
    clock.tick(10)

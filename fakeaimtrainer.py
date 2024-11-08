import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
TARGET_RADIUS = 30
CROSSHAIR_RADIUS = 10
TIMER_LIMIT = 30  # Game time limit in seconds

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Setup screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aim and Shoot Game")  # Window title
clock = pygame.time.Clock()

# Font for score and timer
font = pygame.font.SysFont(None, 36)

# Variables
score = 0
target_position = [random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100)]
target_speed = 3
game_active = False
timer = TIMER_LIMIT

# Function to draw crosshair
def draw_crosshair(mouse_pos):
    pygame.draw.circle(screen, BLUE, mouse_pos, CROSSHAIR_RADIUS)

# Function to draw target
def draw_target(position):
    pygame.draw.circle(screen, RED, position, TARGET_RADIUS)

# Function to check if the crosshair hits the target
def check_hit(target_pos, crosshair_pos):
    distance = math.sqrt((target_pos[0] - crosshair_pos[0])**2 + (target_pos[1] - crosshair_pos[1])**2)
    return distance <= TARGET_RADIUS + CROSSHAIR_RADIUS

# Function to display text (e.g., score, timer, game over)
def display_text(text, x, y, color=BLACK):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Main menu
def main_menu():
    global game_active, score, target_position, timer
    menu_running = True
    while menu_running:
        screen.fill(WHITE)
        
        # Display menu options
        display_text("Aim and Shoot Game", WIDTH // 3, HEIGHT // 4, BLUE)
        display_text("Test Your Skills!!", WIDTH // 2, HEIGHT // 4 + 50, BLACK)  # Added the new text here
        display_text("Press 'Space' to Start", WIDTH // 3, HEIGHT // 2, GREEN)
        display_text("Press 'Q' to Quit", WIDTH // 3, HEIGHT // 2 + 50, RED)
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Changed to Spacebar to start the game
                    game_active = True
                    score = 0
                    timer = TIMER_LIMIT
                    target_position = [random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100)]
                    menu_running = False
                elif event.key == pygame.K_q:
                    menu_running = False

# Game loop
def game_loop():
    global game_active, score, target_position, timer

    while game_active:
        screen.fill(WHITE)
        
        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Draw crosshair
        draw_crosshair(mouse_pos)

        # Draw target
        draw_target(target_position)

        # Move the target randomly
        target_position[0] += random.choice([-1, 1]) * target_speed
        target_position[1] += random.choice([-1, 1]) * target_speed

        # Keep target inside the screen
        if target_position[0] < TARGET_RADIUS or target_position[0] > WIDTH - TARGET_RADIUS:
            target_position[0] = random.randint(100, WIDTH - 100)
        if target_position[1] < TARGET_RADIUS or target_position[1] > HEIGHT - TARGET_RADIUS:
            target_position[1] = random.randint(100, HEIGHT - 100)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_active = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button clicked
                    if check_hit(target_position, mouse_pos):
                        score += 1
                        target_position = [random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100)]

        # Display score
        display_text(f"Score: {score}", 10, 10)

        # Display timer with 2 decimal places
        if timer > 0:
            display_text(f"Time: {timer:.2f}", WIDTH - 150, 10)
            timer -= 1 / FPS  # Decrease timer over time
        else:
            game_active = False  # Time is up, end game

        # Update display
        pygame.display.flip()

        # Set frame rate
        clock.tick(FPS)

    game_over()

# Game Over screen
def game_over():
    global game_active, score
    screen.fill(WHITE)
    display_text(f"Game Over!", WIDTH // 3, HEIGHT // 3, RED)
    display_text(f"Final Score: {score}", WIDTH // 3, HEIGHT // 2, BLUE)
    display_text("Press 'R' to Restart or 'Q' to Quit", WIDTH // 3, HEIGHT // 2 + 50, GREEN)
    pygame.display.flip()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting_for_input = False
                game_active = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_active = True
                    score = 0
                    target_position = [random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100)]
                    timer = TIMER_LIMIT
                    waiting_for_input = False
                    game_loop()  # Restart game
                elif event.key == pygame.K_q:
                    waiting_for_input = False
                    game_active = False

# Main
def main():
    global game_active
    while True:
        if not game_active:
            main_menu()  # Show menu
        if game_active:
            game_loop()  # Start game loop

# Start the game
main()

# Quit Pygame
pygame.quit()
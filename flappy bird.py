import pygame
import sys
import random
import os

# Initialize Pygame
pygame.init()

# Set the dimensions of the window
width, height = 360, 640
screen = pygame.display.set_mode((width, height))

# Set the window title
pygame.display.set_caption("Flappy Bird")

# Define the color (R, G, B)
background_color = (2, 136, 147)  # A shade of blue
input_box_color = (255, 255, 255)  # White
text_color = (0, 0, 0)  # Black

# Load the image
image_path = 'C:/Users/aqeel/OneDrive/Desktop/Flappy Bird/sprites/logo.png'  # Replace with your image file
image = pygame.image.load(image_path)

# Get the dimensions of the image
image_rect = image.get_rect()

# Position the image at the center top of the screen
image_rect.midtop = (width // 2, 0)

# Set up font
font = pygame.font.Font(None, 40)
input_font = pygame.font.Font(None, 30)
prompt_font = pygame.font.Font(None, 30)

# Render the prompt text
prompt_text = font.render("Enter Your Name", True, text_color)
prompt_rect = prompt_text.get_rect(center=(width // 2, height // 2 - 30))

# Input box parameters
input_box_rect = pygame.Rect(width // 2 - 100, height // 2, 200, 50)
input_text = ""
active = False
name_entered = False

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box_rect
            if input_box_rect.collidepoint(event.pos):
                active = True
            else:
                active = False
        elif event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:
                    name_entered = True
                    active = False
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode
            elif name_entered and event.key == pygame.K_SPACE:
                print(f"Starting the game with player name: {input_text}")
                # Proceed to start the game
                running = False  # Exit loop or transition to the next game state

    # Fill the screen with the background color
    screen.fill(background_color)

    # Draw the image on the screen
    screen.blit(image, image_rect)

    if not name_entered:
        # Draw the prompt text
        screen.blit(prompt_text, prompt_rect)

        # Draw the input box with rounded corners
        pygame.draw.rect(screen, input_box_color, input_box_rect, border_radius=10)

        # Render the input text
        txt_surface = input_font.render(input_text, True, text_color)

        # Blit the input text
        screen.blit(txt_surface, (input_box_rect.x + 10, input_box_rect.y + 10))
    else:
        # Show the prompt to press SPACE to start the game
        start_prompt_text = prompt_font.render("Press SPACE to start the game", True, input_box_color)
        start_prompt_rect = start_prompt_text.get_rect(center=(width // 2, height // 2 + 50))
        screen.blit(start_prompt_text, start_prompt_rect)

    # Update the display
    pygame.display.flip()

# Set the dimensions of the window
width, height = 360, 640
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
game_font = pygame.font.Font('freesansbold.ttf', 20)

# Define the color (R, G, B)
background_color = (2, 136, 147)  # A shade of blue
input_box_color = (255, 255, 255)  # White
text_color = (0, 0, 0)  # Black

# Load images
bg_surface = pygame.image.load('C:/Users/aqeel/OneDrive/Desktop/Flappy Bird/sprites/background.jpg').convert()
bg_surface = pygame.transform.scale(bg_surface, (width, height))
floor_surface = pygame.image.load('C:/Users/aqeel/OneDrive/Desktop/Flappy Bird/sprites/base.png').convert()
floor_surface = pygame.transform.scale(floor_surface, (width, 100))

bird_downflap = pygame.image.load('c:/Users/aqeel/OneDrive/Desktop/Flappy Bird/sprites/bird.png').convert_alpha()
bird_midflap = pygame.image.load('c:/Users/aqeel/OneDrive/Desktop/Flappy Bird/sprites/bird.png').convert_alpha()
bird_upflap = pygame.image.load('c:/Users/aqeel/OneDrive/Desktop/Flappy Bird/sprites/bird.png').convert_alpha()
bird_downflap = pygame.transform.scale(bird_downflap, (34, 24))
bird_midflap = pygame.transform.scale(bird_midflap, (34, 24))
bird_upflap = pygame.transform.scale(bird_upflap, (34, 24))
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(50, 320))

pipe_surface = pygame.image.load('C:/Users/aqeel/OneDrive/Desktop/Flappy Bird/sprites/pipe.png').convert()
pipe_surface = pygame.transform.scale(pipe_surface, (52, 320))

game_over_image = pygame.image.load('C:/Users/aqeel/OneDrive/Desktop/Flappy Bird/sprites/game over.jpeg').convert_alpha()
game_over_image = pygame.transform.scale(game_over_image, (width, height))
game_over_rect = game_over_image.get_rect(center=(width // 2, height // 2))

# Set up sound
flap_sound = pygame.mixer.Sound('C:/Users/aqeel/OneDrive/Desktop/Flappy Bird/sounds/flap.mp3')
hit_sound = pygame.mixer.Sound('C:/Users/aqeel/OneDrive/Desktop/Flappy Bird/sounds/hit.mp3')
point_sound = pygame.mixer.Sound('C:/Users/aqeel/OneDrive/Desktop/Flappy Bird/sounds/point.mp3')

# Custom Events
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

# Game Variables
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0
player_name = input_text  # Get the player's name entered in the initial input

pipe_list = []
pipe_height = [300, 400, 500]
floor_x_pos = 0

# High Score File
high_score_file = "high_score.txt"

def read_high_score():
    if os.path.exists(high_score_file):
        with open(high_score_file, 'r') as file:
            try:
                data = file.read().split(',')
                return data[0], float(data[1])
            except (ValueError, IndexError):
                return "", 0.0
    return "", 0.0

def write_high_score(name, score):
    with open(high_score_file, 'w') as file:  # Use 'w' to overwrite the file
        file.write(f'{name},{score:.2f}')

# Functions
def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 540))
    screen.blit(floor_surface, (floor_x_pos + width, 540))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(400, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(400, random_pipe_pos - 200))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 3
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= height:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return False
    if bird_rect.top <= -50 or bird_rect.bottom >= 540:
        hit_sound.play()
        return False
    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    return new_bird

def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(50, bird_rect.centery))
    return new_bird, new_bird_rect

def score_display(game_state, player_name):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(width // 2, 50))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(width // 2, 50))
        screen.blit(score_surface, score_rect)
        high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(width // 2, 100))
        screen.blit(high_score_surface, high_score_rect)
        if player_name:
            player_name_surface = game_font.render(f'High Score By: {player_name}', True, (255, 255, 255))
            player_name_rect = player_name_surface.get_rect(center=(width // 2, 150))
            screen.blit(player_name_surface, player_name_rect)

def update_score(name, score):
    current_name, current_high_score = read_high_score()
    if score > current_high_score:
        write_high_score(name, score)
        return name, score
    return current_name, current_high_score

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 6
                flap_sound.play()
            if event.key == pygame.K_SPACE and not game_active:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (50, 320)
                bird_movement = 0
                score = 0
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird_surface, bird_rect = bird_animation()

    screen.blit(bg_surface, (0, 0))

    if game_active:
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)

        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        score += 0.01
        score_display('main_game', "")

    else:
        screen.blit(game_over_image, game_over_rect)
        high_score_name, high_score = update_score(player_name, score)
        score_display('game_over', high_score_name)

    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -width:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)

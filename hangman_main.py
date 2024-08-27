import pygame
import random
from hangman_words import themes

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 900
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Hangman")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# Font
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

# Load hangman images
hangman_images = []
for i in range(7):
    image = pygame.image.load(f'images\hangman{i}.png')
    image = pygame.transform.scale(image, (300, 300))
    hangman_images.append(image)

# Themes and words
# themes = {
#     "Animals": ["elephant", "giraffe", "hippopotamus", "kangaroo", "alligator"],
#     "Fruits": ["apple", "banana", "cherry", "mango", "strawberry"],
#     "Countries": ["canada", "brazil", "india", "france", "germany"]
# }

# Function to draw text
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

# Function to wait for user input after game over
def wait_for_key():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                return pygame.key.name(event.key).lower()

# Function to display theme selection menu
def choose_theme():
    screen.fill(white)
    draw_text("Choose a theme:", font, black, screen, screen_width / 2, screen_height / 4)

    for i, theme in enumerate(themes):
        draw_text(f"{i+1}. {theme}", small_font, black, screen, screen_width / 2, screen_height / 2 + i * 50)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_1, pygame.K_KP1):
                    return "Animals"
                elif event.key in (pygame.K_2, pygame.K_KP2):
                    return "Fruits"
                elif event.key in (pygame.K_3, pygame.K_KP3):
                    return "Countries"

# Function to display the "Play again?" menu
def play_again_menu():
    screen.fill(white)
    draw_text("Play again? (Y/N)", font, black, screen, screen_width / 2, screen_height / 2)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                response = pygame.key.name(event.key).lower()
                if response == 'y':
                    return True
                elif response == 'n':
                    return False

# Function to display the correct word and handle game over
def game_over(is_winner, correct_word):
    screen.fill(white)
    if is_winner:
        draw_text("You win! 😘", font, black, screen, screen_width / 2, screen_height / 2)
    else:
        draw_text(f"You lose! \n The word was: {correct_word}", font, red, screen, screen_width / 2, screen_height / 2)
    pygame.display.update()
    wait_for_key()

# Main game loop
while True:
    theme = choose_theme()
    chosen_word = random.choice(themes[theme])
    word_length = len(chosen_word)
    display = ["_"] * word_length
    lives = 6
    guessed_letters = []

    running = True
    while running:
        screen.fill(white)
        
        # Display the word with guessed letters
        word_display = " ".join(display)
        draw_text(word_display, font, black, screen, screen_width / 2, screen_height / 4)

        # Display guessed letters
        guessed_display = "Guessed: " + ", ".join(guessed_letters)
        draw_text(guessed_display, small_font, black, screen, screen_width / 2, screen_height / 2)

        # Display hangman image
        screen.blit(hangman_images[6 - lives], (screen_width / 2 - 100, screen_height / 2 + 10))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
            
            if event.type == pygame.KEYDOWN:
                guess = pygame.key.name(event.key).lower()
                
                if guess in guessed_letters:
                    draw_text(f"You've already guessed {guess}", small_font, red, screen, screen_width / 2, screen_height - 100)
                else:
                    guessed_letters.append(guess)
                    if guess in chosen_word:
                        for i in range(word_length):
                            if chosen_word[i] == guess:
                                display[i] = guess
                    else:
                        lives -= 1
                        
                    if lives == 0:
                        running = False
                        game_over(False, chosen_word)  # Show the correct word when losing
                        
                    if "_" not in display:
                        running = False
                        game_over(True, chosen_word)  # Winning scenario
    
        pygame.display.update()

    if not play_again_menu():
        break

pygame.quit()

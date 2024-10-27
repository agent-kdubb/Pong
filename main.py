# Pong by Kimani Muhammad
import sys

import pygame

from Button import Button

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Set the window dimensions
width = 1280
height = 650
screen = pygame.display.set_mode((width, height))  # Initialize the display with height and width
pygame.display.set_caption("Pong")

background = pygame.image.load("assets/backgrounds/Background.png")
level_background = pygame.image.load("assets/backgrounds/Background.png")
menu_music = "assets/music/menu_music.mp3"
gameplay_music = "assets/music/gameplay_music.mp3"
current_screen = 'Main Menu'
volume_level = 0.5
paused = False
is_cpu_controlled = True
ball_color = (255, 255, 255)
# Clock for controlling frame rate
clock = pygame.time.Clock()


def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)


def play():
    global is_cpu_controlled, level_background, paused

    pygame.mixer.music.load(gameplay_music)
    pygame.mixer.music.play(-1)

    # Get player/players name at the start of the game
    if is_cpu_controlled:
        player_name = get_player_name(1)
    else:
        player_name = get_player_name(1)
        player2_name = get_player_name(2)

    # Colors
    black = (0, 0, 0)
    white = (255, 255, 255)

    # Paddle dimensions
    paddle_width = 15
    paddle_height = 90
    paddle_speed = 8

    # Ball dimensions and speed
    ball_radius = 10
    ball_speed_x = 7
    ball_speed_y = 7

    # Create paddles and ball
    left_paddle = pygame.Rect(50, height // 2 - paddle_height // 2, paddle_width, paddle_height)
    right_paddle = pygame.Rect(width - 50 - paddle_width, height // 2 - paddle_height // 2, paddle_width, paddle_height)
    ball = pygame.Rect(width // 2 - ball_radius // 2, height // 2 - ball_radius // 2, ball_radius * 2, ball_radius * 2)

    # Initialize the score
    score = 0
    score_p2 = 0

    # Game Loop
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
        if paused:
            pause()
        else:
            # Handle paddle movement for Player 1
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w] and left_paddle.top > 0:
                left_paddle.y -= paddle_speed
            if keys[pygame.K_s] and left_paddle.bottom < height:
                left_paddle.y += paddle_speed

            if is_cpu_controlled:
                # Handle paddle movement for CPU
                if ball.centery < right_paddle.centery and right_paddle.top > 0:
                    right_paddle.y -= paddle_speed
                elif ball.centery > right_paddle.centery and right_paddle.top < height:
                    right_paddle.y += paddle_speed
            else:
                # Handle paddle movement for Player 2
                if keys[pygame.K_UP] and right_paddle.top > 0:
                    right_paddle.y -= paddle_speed
                if keys[pygame.K_DOWN] and right_paddle.bottom < height:
                    right_paddle.y += paddle_speed

            # Ball movement
            ball.x += ball_speed_x
            ball.y += ball_speed_y

            # Ball collision with walls
            if ball.top <= 0 or ball.bottom >= height:
                ball_speed_y *= -1
            if ball.left <= 0 or ball.right >= width:
                if is_cpu_controlled:
                    save_high_score(player_name, score)
                    pygame.mixer.music.stop()
                    game_over()
                else:
                    save_high_score(player_name, score)
                    save_high_score(player2_name, score_p2)
                    if score > score_p2:
                        player_wins(player_name, score)
                    else:
                        player_wins(player2_name, score_p2)

            # Ball collision with paddles
            if ball.colliderect(left_paddle):
                ball_speed_x *= -1.01
                score += 1
            elif ball.colliderect(right_paddle):
                ball_speed_x *= -1.01
                score_p2 += 1

        # Clear screen
        screen.blit(level_background, (0, 0))

        # Draw paddles and ball
        pygame.draw.rect(screen, white, left_paddle)
        pygame.draw.rect(screen, white, right_paddle)
        pygame.draw.ellipse(screen, ball_color, ball)

        # Display score
        if is_cpu_controlled:
            score_text = get_font(45).render(f"Score: {score}", True, white)
            screen.blit(score_text, (width // 2 - score_text.get_width() // 2, 20))
        else:
            score_text = get_font(25).render(f"{player_name}: {score}", True, white)
            screen.blit(score_text, (5, 20))
            score_p2_text = get_font(25).render(f"{player2_name}: {score_p2}", True, white)
            screen.blit(score_p2_text, (width - score_p2_text.get_width() - 5, 20))

        # Update display
        pygame.display.flip()

        # Cap the frame rate at 60 frames per second
        clock.tick(60)

    pygame.mixer.music.stop()

    # Quit game
    pygame.quit()


def options():
    global is_cpu_controlled, ball_color, volume_level

    slider_width = 300
    slider_height = 10
    slider_x = 640 - slider_width // 2
    slider_y = 500

    handle_width = 20
    handle_x = slider_x + volume_level * slider_width - handle_width // 2
    handle_y = slider_y - (handle_width // 2 - slider_height // 2)
    dragging = False

    while True:
        options_mouse_pos = pygame.mouse.get_pos()
        screen.fill("black")

        options_text = get_font(45).render("OPTIONS", True, "White")
        options_rect = options_text.get_rect(center=(width // 2, 100))
        screen.blit(options_text, options_rect)

        # Toggle CPU control for Player 2
        toggle_text = "CPU" if is_cpu_controlled else "Player 2"
        toggle_button = Button(image=None, pos=(width // 2, 260),
                               text_input=f"Right Paddle: {toggle_text}", font=get_font(45), base_color="White",
                               hovering_color="Green")

        options_back = Button(image=None, pos=(640, 575),
                              text_input="BACK", font=get_font(45), base_color="White", hovering_color="Green")

        # Ball color selection
        ball_color_text = get_font(45).render("Select ball color:", True, "White")
        ball_color_rect = options_text.get_rect(center=(width // 2 - 225, 325))

        screen.blit(ball_color_text, ball_color_rect)

        white_button = Button(image=None, pos=(width // 2 - 100, 375), text_input=".", font=get_font(45),
                              base_color="White", hovering_color="Green")
        red_button = Button(image=None, pos=(width // 2, 375), text_input=".", font=get_font(45),
                            base_color="Red", hovering_color="Green")
        blue_button = Button(image=None, pos=(width // 2 + 100, 375), text_input=".", font=get_font(45),
                             base_color="Blue", hovering_color="Green")

        volume_text = get_font(45).render("Adjust volume:", True, "White")
        volume_rect = volume_text.get_rect(center=(width // 2, 450))

        screen.blit(volume_text, volume_rect)

        pygame.draw.rect(screen, (100, 100, 100), (slider_x, slider_y, slider_width, slider_height))

        pygame.draw.rect(screen, (255, 0, 0), (handle_x, handle_y, handle_width, handle_width))

        # Update the buttons
        toggle_button.changeColor(options_mouse_pos)
        toggle_button.update(screen)
        white_button.changeColor(options_mouse_pos)
        white_button.update(screen)
        red_button.changeColor(options_mouse_pos)
        red_button.update(screen)
        blue_button.changeColor(options_mouse_pos)
        blue_button.update(screen)
        options_back.changeColor(options_mouse_pos)
        options_back.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if toggle_button.checkForInput(options_mouse_pos):
                    is_cpu_controlled = not is_cpu_controlled
                if white_button.checkForInput(options_mouse_pos):
                    ball_color = (255, 255, 255)
                if red_button.checkForInput(options_mouse_pos):
                    ball_color = (255, 0, 0)
                if blue_button.checkForInput(options_mouse_pos):
                    ball_color = (0, 0, 255)
                if options_back.checkForInput(options_mouse_pos):
                    return
                # Check if mouse pos is within the handle
                if ((handle_x <= options_mouse_pos[0] <= handle_x + handle_width) and
                        (handle_y <= options_mouse_pos[1] <= handle_y + handle_width)):
                    dragging = True
            if event.type == pygame.MOUSEBUTTONUP:
                dragging = False  # Stop dragging on mouse up

            if event.type == pygame.MOUSEMOTION:
                # Allow dragging volume if
                if dragging:
                    handle_x = max(slider_x, min(options_mouse_pos[0] - handle_width // 2,
                                                 slider_x + slider_width - handle_width))
                    volume_level = (handle_x - slider_x + handle_width // 2) / slider_width
                    volume_level = max(0.0, min(1.0, volume_level))
                    pygame.mixer.music.set_volume(volume_level)

        pygame.display.flip()


def get_player_name(player_num):
    player_name = ""
    input_active = True

    while input_active:
        screen.fill("black")

        # Display prompt
        prompt_text = get_font(45).render(f"Enter Player {player_num} name:", True, "White")
        screen.blit(prompt_text, (width // 2 - prompt_text.get_width() // 2, height // 2 - 100))

        # Display the current input text
        name_text = get_font(45).render(player_name, True, "White")
        pygame.draw.rect(screen, "White", (width // 2 - 200, height // 2, 400, 50), 2)
        screen.blit(name_text, (width // 2 - name_text.get_width() // 2, height // 2))

        # Display "Start" button
        start_button = Button(image=None, pos=(width // 2, height // 2 + 100),
                              text_input="START", font=get_font(45), base_color="White", hovering_color="Green")
        start_button.changeColor(pygame.mouse.get_pos())
        start_button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                print(f"Key pressed: {event.key}")
                if event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                elif event.key == pygame.K_RETURN:
                    input_active = False
                else:
                    if event.unicode.isprintable():
                        player_name += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.checkForInput(pygame.mouse.get_pos()):
                    input_active = False

        pygame.display.update()

    return player_name


def load_leaderboard():
    try:
        with open("assets/leaderboard.txt", "r") as file:
            return [(line.split(",")[0], int(line.split(",")[1].strip())) for line in file.readlines()]
    except FileNotFoundError:
        return []


def save_high_score(player_name, score):
    leaderboard = load_leaderboard()
    leaderboard.append((player_name, score))
    leaderboard = sorted(leaderboard, key=lambda x: x[1], reverse=True)[:10]

    with open("assets/leaderboard.txt", "w") as file:
        for name, score in leaderboard:
            file.write(f"{name},{score}\n")


def show_leaderboard():
    leaderboard = load_leaderboard()
    while True:
        screen.fill("black")
        leaderboard_text = get_font(45).render("Leaderboard", True, "White")
        leaderboard_rect = leaderboard_text.get_rect(center=(width // 2, 50))
        screen.blit(leaderboard_text, leaderboard_rect)

        # Display leaderboard scores
        for i, (name, score) in enumerate(leaderboard):
            score_text = get_font(45).render(f"{i + 1}. {name} - {score}", True, "White")
            screen.blit(score_text, (width // 2 - score_text.get_width() // 2, 100 + i * 50))

        # Back button
        back_button = Button(image=None, pos=(width // 2, 625), text_input="BACK", font=get_font(45),
                             base_color="White", hovering_color="Green")

        back_button.changeColor(pygame.mouse.get_pos())
        back_button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.checkForInput(pygame.mouse.get_pos()):
                    return  # Go back to main menu
        pygame.display.flip()


def game_over():
    while True:
        game_over_mouse_pos = pygame.mouse.get_pos()

        screen.fill("black")

        options_text = get_font(55).render("GAME OVER", True, "White")
        options_rect = options_text.get_rect(center=(640, 260))
        screen.blit(options_text, options_rect)

        play_again_button = Button(image=None, pos=(640, 430),
                                   text_input="PLAY AGAIN", font=get_font(45), base_color="White",
                                   hovering_color="Green")

        play_again_button.changeColor(game_over_mouse_pos)
        play_again_button.update(screen)

        menu_button = Button(image=None, pos=(640, 490),
                             text_input="MAIN MENU", font=get_font(45), base_color="White", hovering_color="Green")

        menu_button.changeColor(game_over_mouse_pos)
        menu_button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_button.checkForInput(game_over_mouse_pos):
                    play()
                if menu_button.checkForInput(game_over_mouse_pos):
                    main_menu()

        pygame.display.update()


def player_wins(player_name, player_score):
    while True:
        game_over_mouse_pos = pygame.mouse.get_pos()

        screen.fill("black")

        player_win_text = get_font(45).render(f"{player_name} wins with {player_score} points!", True, "White")
        player_win_rect = player_win_text.get_rect(center=(640, 260))
        screen.blit(player_win_text, player_win_rect)

        play_again_button = Button(image=None, pos=(640, 460),
                                   text_input="PLAY AGAIN", font=get_font(45), base_color="White",
                                   hovering_color="Green")

        play_again_button.changeColor(game_over_mouse_pos)
        play_again_button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_button.checkForInput(game_over_mouse_pos):
                    main_menu()

        pygame.display.update()


def main_menu():
    pygame.mixer.music.load(menu_music)
    pygame.mixer.music.set_volume(volume_level)
    pygame.mixer.music.play(-1)

    while True:
        screen.blit(background, (0, 0))

        menu_mouse_pos = pygame.mouse.get_pos()

        menu_text = get_font(100).render("PONG", True, "#b68f40")
        menu_rect = menu_text.get_rect(center=(640, 100))

        trophy_icon = pygame.image.load("assets/Trophy.png")
        scaled_trophy = pygame.transform.scale(trophy_icon, (50, 50))

        play_button = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250),
                             text_input="Play", font=get_font(75), base_color="#d7fcd4", hovering_color="Green")
        options_button = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400),
                                text_input="Options", font=get_font(75), base_color="#d7fcd4", hovering_color="Green")
        quit_button = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550),
                             text_input="Quit", font=get_font(75), base_color="#d7fcd4", hovering_color="Green")
        trophy_button = Button(image=scaled_trophy, pos=(50, 50),
                               text_input="", font=get_font(30), base_color="#d7fcd4", hovering_color="Green")

        screen.blit(menu_text, menu_rect)

        for button in [play_button, options_button, quit_button, trophy_button]:
            button.changeColor(menu_mouse_pos)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.checkForInput(menu_mouse_pos):
                    pygame.mixer.music.stop()
                    play()
                if options_button.checkForInput(menu_mouse_pos):
                    options()
                if quit_button.checkForInput(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()
                if trophy_button.checkForInput(menu_mouse_pos):
                    show_leaderboard()

        pygame.display.flip()


def pause():
    global paused
    while paused:
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        pause_text = get_font(75).render("PAUSED", True, "White")
        pause_rect = pause_text.get_rect(center=(640, 200))
        screen.blit(pause_text, pause_rect)

        # Resume Button
        resume_button = Button(image=None, pos=(640, 350), text_input="RESUME",
                               font=get_font(50), base_color="White", hovering_color="Green")

        # Main Menu Button
        menu_button = Button(image=None, pos=(640, 450), text_input="MAIN MENU",
                             font=get_font(50), base_color="White", hovering_color="Green")

        pause_mouse_pos = pygame.mouse.get_pos()

        resume_button.changeColor(pause_mouse_pos)
        resume_button.update(screen)

        menu_button.changeColor(pause_mouse_pos)
        menu_button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if resume_button.checkForInput(pause_mouse_pos):
                    paused = False
                if menu_button.checkForInput(pause_mouse_pos):
                    main_menu()
                    paused = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False

        pygame.display.update()
        clock.tick(30)


main_menu()

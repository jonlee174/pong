import pygame
import pygame.gfxdraw
import os
from item_class import Item
from history import record_history
import webbrowser

pygame.init()
pygame.mixer.init()

# Screen Setup
WIDTH, HEIGHT = 750, 400
SCREEN = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Pong")
LOGO = pygame.image.load(os.path.join("assets", "pong_logo.png"))
LEFT_ARROW = pygame.transform.scale(pygame.image.load(os.path.join("assets", "left_arrow.png")), (50, 30))
pygame.display.set_icon(LOGO)
FPS = 60
HIT_SOUND = pygame.mixer.Sound(os.path.join("assets", "pong_hit.mp3"))
THEME = pygame.mixer.music.load(os.path.join("assets", "pong_theme.mp3"))
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

player_1_score = 0
player_2_score = 0
WON = pygame.USEREVENT + 1

# Text Setup

FONT = pygame.font.Font(os.path.join("assets", "pixel.ttf"), 50)
text1 = FONT.render(str(player_1_score), True, WHITE)
text1_rect = text1.get_rect()
text1_rect.center = (WIDTH//2 - 100, 33)

text2 = FONT.render(str(player_2_score), True, WHITE)
text2_rect = text1.get_rect()
text2_rect.center = (WIDTH//2 + 100, 33)

MENU_FONT = pygame.font.Font(os.path.join("assets", "pixel.ttf"), 125)
menu_text = MENU_FONT.render("PONG", True, WHITE)
menu_text_rect = menu_text.get_rect()
menu_text_rect.center = (WIDTH//2, 60)

CREDITS_FONT = pygame.font.Font(os.path.join("assets", "pixel.ttf"), 20)
credits_text = CREDITS_FONT.render("BY JLEE", True, WHITE)
credits_text_rect = credits_text.get_rect()
credits_text_rect.center = (WIDTH//2, HEIGHT - 60)

PAUSE_FONT = pygame.font.Font(os.path.join("assets", "pixel.ttf"), 75)
pause_text = PAUSE_FONT.render("PAUSED", True, WHITE)
pause_text_rect = pause_text.get_rect()
pause_text_rect.center = (WIDTH//2, HEIGHT//2)

message_text = CREDITS_FONT.render("ARE YOU SURE YOU WANT TO QUIT?", True, WHITE)
message_text_rect = message_text.get_rect()
message_text_rect.center = (WIDTH//2, HEIGHT//2 - 25)

PADDLE_1 = Item("pong_paddle.png", 25, 150)
PADDLE_2 = Item("pong_paddle.png", 720, 150)
BALL = Item("pong_ball.png", WIDTH//2 - 4, 185)

mainloop = False
history_loop = False
open_link_count = 0

# Game Menu Presentation
def game_menu():
    global in_menu, running, mainloop, history_loop, presenting_exit, esc_key_count, open_link_count
    while in_menu:

        play_text = FONT.render("PLAY", True, WHITE)
        play_text_rect = play_text.get_rect()
        play_text_rect.center = (212, 225)

        hist_text = FONT.render("HISTORY", True, WHITE)
        hist_text_rect = play_text.get_rect()
        hist_text_rect.center = (512, 225)

        SCREEN.fill(BLACK)
        SCREEN.blit(menu_text, menu_text_rect)
        SCREEN.blit(credits_text, credits_text_rect)

        if credits_text_rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
            pygame.gfxdraw.line(SCREEN, WIDTH//2 - 5, HEIGHT - 53, WIDTH//2 + 25, HEIGHT - 53, WHITE)
            if pygame.mouse.get_pressed()[0]:
                while open_link_count == 0:
                    webbrowser.open("https://github.com/jonlee174")
                    open_link_count += 1

        if 125 < pygame.mouse.get_pos()[0] < 300 and 200 < pygame.mouse.get_pos()[1] < 250:
            pygame.gfxdraw.filled_polygon(SCREEN, [(125, 200), (300, 200), (300, 250), (125, 250)], WHITE)
            play_text = FONT.render("PLAY", True, BLACK)

        if WIDTH - 125 > pygame.mouse.get_pos()[0] > WIDTH - 300 and 200 < pygame.mouse.get_pos()[1] < 250:
            pygame.gfxdraw.filled_polygon(SCREEN, [(WIDTH - 125, 200), (WIDTH - 300, 200), (WIDTH - 300, 250), (WIDTH - 125, 250)], WHITE)
            hist_text = FONT.render("HISTORY", True, BLACK)

        pygame.gfxdraw.aapolygon(SCREEN, [(125, 200), (300, 200), (300, 250), (125, 250)], WHITE)
        pygame.gfxdraw.aapolygon(SCREEN, [(WIDTH - 125, 200), (WIDTH - 300, 200), (WIDTH - 300, 250), (WIDTH - 125, 250)], WHITE)
        SCREEN.blit(play_text, play_text_rect)
        SCREEN.blit(hist_text, hist_text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_menu = False
                running = False
                mainloop = False

        if pygame.mouse.get_pressed()[0] and 125 < pygame.mouse.get_pos()[0] < 300 and 200 < pygame.mouse.get_pos()[1] < 250:
            in_menu = False
            presenting_exit = False
            mainloop = True
            history_loop = False

        elif pygame.mouse.get_pressed()[0] and WIDTH - 125 > pygame.mouse.get_pos()[0] > WIDTH - 300 and 200 < pygame.mouse.get_pos()[1] < 250:
            in_menu = False
            presenting_exit = False
            mainloop = False
            history_loop = True

            
            while history_loop:
                line_y = 50
                SCREEN.fill(BLACK)

                line_list = []
                try:
                    with open(os.path.join("data", "history.txt"), "r") as f:
                        for line in f.readlines():
                            line_list.append(line.strip("\n"))

                    for line in line_list:
                        line_text = CREDITS_FONT.render(line, True, WHITE)
                        line_text_rect = line_text.get_rect()
                        line_text_rect.center = (200, line_y)
                        SCREEN.blit(line_text, line_text_rect)
                        line_y += 50
                    if len(line_list) == 0:
                        line_text = FONT.render("NO HISTORY", True, WHITE)
                        line_text_rect = line_text.get_rect()
                        line_text_rect.center = (WIDTH//2, 175)
                        SCREEN.blit(line_text, line_text_rect)
                except PermissionError or FileNotFoundError:
                    pass

                SCREEN.blit(LEFT_ARROW, (10, 10))
                if pygame.mouse.get_pressed()[0] and LEFT_ARROW.get_rect().collidepoint(pygame.mouse.get_pos()):
                    in_menu = True
                    presenting_exit = False
                    mainloop = False
                    history_loop = False

                '''clr_hist_text = CREDITS_FONT.render("CLEAR HISTORY", True, WHITE)
                clr_hist_text_rect = clr_hist_text.get_rect()
                clr_hist_text_rect.center = (WIDTH - 75, 23)

                pygame.gfxdraw.filled_polygon(SCREEN, [(WIDTH - 136, 10), (WIDTH - 136, 35), (WIDTH - 15, 35), (WIDTH - 15, 10)], BLACK)
                pygame.gfxdraw.aapolygon(SCREEN, [(WIDTH - 136, 10), (WIDTH - 136, 35), (WIDTH - 15, 35), (WIDTH - 15, 10)], WHITE)
                SCREEN.blit(clr_hist_text, clr_hist_text_rect)

                if WIDTH - 136 < pygame.mouse.get_pos()[0] < WIDTH - 15 and 10 < pygame.mouse.get_pos()[1] < 35:
                    pygame.gfxdraw.filled_polygon(SCREEN, [(WIDTH - 136, 10), (WIDTH - 136, 35), (WIDTH - 15, 35), (WIDTH - 15, 10)], WHITE)
                    clr_hist_text = CREDITS_FONT.render("CLEAR HISTORY", True, BLACK)
                    SCREEN.blit(clr_hist_text, clr_hist_text_rect)
                    if pygame.mouse.get_pressed()[0]:
                        with open(os.path.join("data", "history.txt"), "w+") as f:
                            f.truncate(0)'''

                present_exit()

                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        mainloop = False
                        history_loop = False
                        presenting_exit = False

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            esc_key_count += 1
                            if esc_key_count % 2 == 1:
                                presenting_exit = True
                            else:
                                presenting_exit = False

        pygame.display.update()

# Main Game Presentation
def draw_win():
    global mainloop, in_menu, history_loop

    SCREEN.fill(BLACK)
    SCREEN.blit(PADDLE_1.surface, (PADDLE_1.x, PADDLE_1.y))
    SCREEN.blit(PADDLE_2.surface, (PADDLE_2.x, PADDLE_2.y))
    SCREEN.blit(BALL.surface, (BALL.x, BALL.y))
    SCREEN.blit(FONT.render(str(player_1_score), True, WHITE), text1_rect)
    SCREEN.blit(FONT.render(str(player_2_score), True, WHITE), text2_rect)
    pygame.gfxdraw.line(SCREEN, WIDTH//2, 0, WIDTH//2, HEIGHT, WHITE)

    if paused:
        SCREEN.blit(pause_text, pause_text_rect)

    check_win("PLAYER 1", player_1_score)
    check_win("PLAYER 2", player_2_score)
        

    present_exit()

# Pop-up exit window
def present_exit():
    global running, presenting_exit, in_menu, esc_key_count

    yes_text = CREDITS_FONT.render("YES", True, WHITE)
    yes_text_rect = yes_text.get_rect()
    yes_text_rect.center = (WIDTH//2 - 63, HEIGHT//2 + 12)
    
    no_text = CREDITS_FONT.render("NO", True, WHITE)
    no_text_rect = no_text.get_rect()
    no_text_rect.center = (WIDTH//2 + 63, HEIGHT//2 + 12)

    esc_key_count = 0
    if presenting_exit:
        pygame.gfxdraw.filled_polygon(SCREEN, [(WIDTH//2 - 150, 150), (WIDTH//2 + 150, 150), (WIDTH//2 + 150, 250), (WIDTH//2 - 150, 250)], BLACK)
        pygame.gfxdraw.aapolygon(SCREEN, [(WIDTH//2 - 150, 150), (WIDTH//2 + 150, 150), (WIDTH//2 + 150, 250), (WIDTH//2 - 150, 250)], WHITE)
        SCREEN.blit(message_text, message_text_rect)
        pygame.gfxdraw.filled_polygon(SCREEN, [(WIDTH//2 - 100, HEIGHT//2), (WIDTH//2 - 25, HEIGHT//2), (WIDTH//2 - 25, HEIGHT//2 + 25), (WIDTH//2 - 100, HEIGHT//2 + 25)], BLACK)
        pygame.gfxdraw.aapolygon(SCREEN, [(WIDTH//2 - 100, HEIGHT//2), (WIDTH//2 - 25, HEIGHT//2), (WIDTH//2 - 25, HEIGHT//2 + 25), (WIDTH//2 - 100, HEIGHT//2 + 25)], WHITE)
        pygame.gfxdraw.filled_polygon(SCREEN, [(WIDTH//2 + 100, HEIGHT//2), (WIDTH//2 + 25, HEIGHT//2), (WIDTH//2 + 25, HEIGHT//2 + 25), (WIDTH//2 + 100, HEIGHT//2 + 25)], BLACK)
        pygame.gfxdraw.aapolygon(SCREEN, [(WIDTH//2 + 100, HEIGHT//2), (WIDTH//2 + 25, HEIGHT//2), (WIDTH//2 + 25, HEIGHT//2 + 25), (WIDTH//2 + 100, HEIGHT//2 + 25)], WHITE)

        if WIDTH//2 - 100 < pygame.mouse.get_pos()[0] < WIDTH//2 - 25 and HEIGHT//2 < pygame.mouse.get_pos()[1] < HEIGHT//2 + 25:
            pygame.gfxdraw.filled_polygon(SCREEN, [(WIDTH//2 - 100, HEIGHT//2), (WIDTH//2 - 25, HEIGHT//2), (WIDTH//2 - 25, HEIGHT//2 + 25), (WIDTH//2 - 100, HEIGHT//2 + 25)], WHITE)
            yes_text = CREDITS_FONT.render("YES", True, BLACK)

        if WIDTH//2 + 100 > pygame.mouse.get_pos()[0] > WIDTH//2 + 25 and HEIGHT//2 < pygame.mouse.get_pos()[1] < HEIGHT//2 + 25:
            pygame.gfxdraw.filled_polygon(SCREEN, [(WIDTH//2 + 100, HEIGHT//2), (WIDTH//2 + 25, HEIGHT//2), (WIDTH//2 + 25, HEIGHT//2 + 25), (WIDTH//2 + 100, HEIGHT//2 + 25)], WHITE)
            no_text = CREDITS_FONT.render("NO", True, BLACK)

        if pygame.mouse.get_pressed()[0] and WIDTH//2 + 100 > pygame.mouse.get_pos()[0] > WIDTH//2 + 25 and HEIGHT//2 < pygame.mouse.get_pos()[1] < HEIGHT//2 + 25:
            presenting_exit = False

        elif pygame.mouse.get_pressed()[0] and WIDTH//2 - 100 < pygame.mouse.get_pos()[0] < WIDTH//2 - 25 and HEIGHT//2 < pygame.mouse.get_pos()[1] < HEIGHT//2 + 25:
            presenting_exit = False
            in_menu = True
            reset_game()
            game_menu()

        SCREEN.blit(yes_text, yes_text_rect)
        SCREEN.blit(no_text, no_text_rect)

    pygame.display.update()

# Game Reset
def reset_game():
    global paused, player_1_score, player_2_score

    BALL.x, BALL.y = WIDTH//2 - 4, 185
    PADDLE_1.x, PADDLE_1.y = 25, 150
    PADDLE_2.x, PADDLE_2.y = 720, 150
    paused = True
    player_1_score = 0
    player_2_score = 0

# Checks for winner
def check_win(winner, winning_score):
    global mainloop, history_loop, in_menu, paused

    if winning_score >= 5:
        paused = True
        SCREEN.fill(BLACK)
        SCREEN.blit(MENU_FONT.render(str(f"{winner} WINS"), True, WHITE), (50, 50))
        pygame.gfxdraw.filled_polygon(SCREEN, [(WIDTH//2 - 150, 200), (WIDTH//2 + 150, 200), (WIDTH//2 + 150, 250), (WIDTH//2 - 150, 250)], BLACK)
        pygame.gfxdraw.aapolygon(SCREEN, [(WIDTH//2 - 150, 200), (WIDTH//2 + 150, 200), (WIDTH//2 + 150, 250), (WIDTH//2 - 150, 250)], WHITE)
        SCREEN.blit(FONT.render(str("BACK TO MENU"), True, WHITE), (WIDTH//2 - 135, 203))

        if WIDTH//2 - 150 < pygame.mouse.get_pos()[0] < WIDTH//2 + 150 and 200 < pygame.mouse.get_pos()[1] < 250:
            pygame.gfxdraw.filled_polygon(SCREEN, [(WIDTH//2 - 150, 200), (WIDTH//2 + 150, 200), (WIDTH//2 + 150, 250), (WIDTH//2 - 150, 250)], WHITE)
            SCREEN.blit(FONT.render(str("BACK TO MENU"), True, BLACK), (WIDTH//2 - 135, 203))

        if pygame.mouse.get_pressed()[0] and WIDTH//2 - 150 < pygame.mouse.get_pos()[0] < WIDTH//2 + 150 and 200 < pygame.mouse.get_pos()[1] < 250:
            mainloop = False
            history_loop = False
            in_menu = True
            reset_game()
            game_menu()


running = True
in_menu = True
clock = pygame.time.Clock()
x_vel = 6
y_vel = 2

pygame.mixer.music.play(-1)
game_menu()

pygame.mixer.music.stop()
paused = True
esc_key_count = 0
run_once = 0

# Main Loop
while running:
    while mainloop:
    
        keys = pygame.key.get_pressed()
        clock.tick(FPS)

        draw_win()

    # Game Logic
        if not paused:
            BALL.x += x_vel
            BALL.y += y_vel
        if BALL.x < PADDLE_1.x and PADDLE_1.y < BALL.y < PADDLE_1.y + 70:
            pygame.mixer.Sound.play(HIT_SOUND)
            x_vel *= -1

        elif BALL.x > PADDLE_2.x and PADDLE_2.y < BALL.y < PADDLE_2.y + 70:
            pygame.mixer.Sound.play(HIT_SOUND)
            x_vel *= -1

        if BALL.y <= 0 or BALL.y >= HEIGHT:
            y_vel *= -1
        
        if BALL.x > WIDTH:
            player_1_score += 1
            BALL.x, BALL.y = WIDTH//2 - 4, 185
            x_vel *= -1
            y_vel *= -1

        elif BALL.x < 0:
            player_2_score += 1
            BALL.x, BALL.y = WIDTH//2 - 4, 185
            x_vel *= -1
            y_vel *= -1


    # Game Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                history_loop = False
                mainloop = False
                presenting_exit = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if paused and not presenting_exit:
                        paused = False
                    else:
                        paused = True

                if event.key == pygame.K_ESCAPE:
                    paused = True
                    esc_key_count += 1
                    if esc_key_count % 2 == 1:
                        presenting_exit = True
                    else:
                        presenting_exit = False

            if event.type == WON:
                while run_once == 0:
                    record_history(player_1_score, player_2_score)
                    run_once += 1

                while run_once == 0:
                    record_history(player_2_score, player_1_score)
                    run_once += 1

        if player_1_score >= 5 or player_2_score >= 5:
            pygame.event.post(pygame.event.Event(WON))


    # Keypress Events
            
        if keys[pygame.K_w]:
            if 3 <= PADDLE_1.y and not paused:
                PADDLE_1.y -= 4

        elif keys[pygame.K_s] and not paused:
            if PADDLE_1.y <= HEIGHT - 70:
                PADDLE_1.y += 4

        if keys[pygame.K_UP] and not paused:
            if 3 <= PADDLE_2.y:
                PADDLE_2.y -= 4

        elif keys[pygame.K_DOWN] and not paused:
            if PADDLE_2.y <= HEIGHT - 70:
                PADDLE_2.y += 4
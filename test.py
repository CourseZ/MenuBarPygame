import pygame,sys
from button import Button
from random import randint
import random

pygame.init()

# load font
GAME_FONT = pygame.font.Font('font/04B_19.TTF',50)

# load tube image
TUBE_IMG = pygame.image.load('img/tube.png')
TUBE_OP_IMG = pygame.image.load('img/tube_op.png') # tube opposite

PLAY_BG_IMG = pygame.image.load('img/background-night.png')
PLAY_BG_IMG = pygame.transform.scale(PLAY_BG_IMG,(WIDTH,HEIGHT))
FLOOR = pygame.image.load('img/floor.png')
FLOOR = pygame.transform.scale(FLOOR,(WIDTH,100))

BIRD_WIDTH,BIRD_HEIGHT = 35,35
BIRD_IMG = pygame.image.load('img/yellowbird-midflap.png')
BIRD_IMG = pygame.transform.scale(BIRD_IMG,(BIRD_WIDTH,BIRD_HEIGHT))

BIRD_DOWN_YELLOW = pygame.image.load('img/yellowbird-downflap.png')
BIRD_DOWN_YELLOW = pygame.transform.scale(BIRD_DOWN_YELLOW,(BIRD_WIDTH,BIRD_HEIGHT))
BIRD_MID_YELLOW = pygame.image.load('img/yellowbird-midflap.png')
BIRD_MID_YELLOW = pygame.transform.scale(BIRD_MID_YELLOW,(BIRD_WIDTH,BIRD_HEIGHT))
BIRD_UP_YELLOW = pygame.image.load('img/yellowbird-upflap.png')
BIRD_UP_YELLOW = pygame.transform.scale(BIRD_UP_YELLOW,(BIRD_WIDTH,BIRD_HEIGHT))

BIRD_DOWN_BLUE = pygame.image.load('img/bluebird-downflap.png')
BIRD_DOWN_BLUE = pygame.transform.scale(BIRD_DOWN_BLUE,(BIRD_WIDTH,BIRD_HEIGHT))
BIRD_MID_BLUE = pygame.image.load('img/bluebird-midflap.png')
BIRD_MID_BLUE = pygame.transform.scale(BIRD_MID_BLUE,(BIRD_WIDTH,BIRD_HEIGHT))
BIRD_UP_BLUE = pygame.image.load('img/bluebird-upflap.png')
BIRD_UP_BLUE = pygame.transform.scale(BIRD_UP_BLUE,(BIRD_WIDTH,BIRD_HEIGHT))

BIRD_DOWN_RED = pygame.image.load('img/redbird-downflap.png')
BIRD_DOWN_RED = pygame.transform.scale(BIRD_DOWN_RED,(BIRD_WIDTH,BIRD_HEIGHT))
BIRD_MID_RED = pygame.image.load('img/redbird-midflap.png')
BIRD_MID_RED = pygame.transform.scale(BIRD_MID_RED,(BIRD_WIDTH,BIRD_HEIGHT))
BIRD_UP_RED = pygame.image.load('img/redbird-upflap.png')
BIRD_UP_RED = pygame.transform.scale(BIRD_UP_RED,(BIRD_WIDTH,BIRD_HEIGHT))

FLAP_SOUND = pygame.mixer.Sound('sounds/sfx_wing.wav')
HIT_SOUND = pygame.mixer.Sound('sounds/sfx_hit.wav')
SCORE_SOUND = pygame.mixer.Sound('sounds/sfx_point.wav')

GAME_LOSS = pygame.image.load('img/gameover.png') # 192x42
GAME_LOSS_RECT = GAME_LOSS.get_rect(center=(250,50))

GAME_OVER = pygame.image.load('img/message.png')
GAME_OVER = pygame.transform.scale2x(GAME_OVER) # (145x210) x2 = (290x420)
GAME_OVER_RECT = GAME_OVER.get_rect(center=(250,375))

# options
SQUARE_BTN_BG = pygame.image.load('img/square_btn_bg.png')
SQUARE_BTN_BG = pygame.transform.scale(SQUARE_BTN_BG,(130,130))

OPTION_BTN_BG = pygame.image.load('img/btn_options_bg.png')
OPTION_BTN_BG = pygame.transform.scale(OPTION_BTN_BG,(130,50))

OPTION_CONTROL_BG = pygame.image.load('img/options_back_btn_bg.png')
OPTION_CONTROL_BG = pygame.transform.scale(OPTION_CONTROL_BG,(130,70))

SNOW_MOUNTAIN_IMG = pygame.image.load('img/background.png')
SNOW_MOUNTAIN_IMG = pygame.transform.scale(SNOW_MOUNTAIN_IMG,(WIDTH,HEIGHT))

TUTOR_IMG = pygame.image.load('img/tutor_btn.png')
TUTOR_IMG = pygame.transform.scale(TUTOR_IMG,(50,50))

PYGAME_ICON = pygame.image.load('flappy.ico')



LEVEL = 1
WIDTH,HEIGHT = 500,700
# main
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Bird Game")
pygame.display.set_icon(PYGAME_ICON)
CLOCK = pygame.time.Clock()

birdflap = pygame.USEREVENT
pygame.time.set_timer(birdflap,200)

running = True

def play(LEVEL,bird_selected):
    LEVEL = LEVEL
    bird_selected = bird_selected

    GRAVITY = 0.5

    floor_x_pos = 0
    bg_x_pos = 0

    x_pos_play = 0
    
    tube1_x = 500
    tube2_x = 700
    tube3_x = 900
    
    tube1_height = randint(100,350)
    tube2_height = randint(100,350)
    tube3_height = randint(100,350)

    tube1_op_height = HEIGHT - (tube1_height + TUBE_GAP + 100) 
    tube2_op_height = HEIGHT - (tube2_height + TUBE_GAP + 100) 
    tube3_op_height = HEIGHT - (tube3_height + TUBE_GAP + 100) 

    x_bird = 50
    y_bird = 350
    bird_drop_velocity = 0
    if bird_selected == 0:
        bird_list = [BIRD_DOWN_YELLOW,BIRD_MID_YELLOW,BIRD_UP_YELLOW]
    elif bird_selected == 1:
        bird_list = [BIRD_DOWN_BLUE,BIRD_MID_BLUE,BIRD_UP_BLUE]
    else:
        bird_list = [BIRD_DOWN_RED,BIRD_MID_RED,BIRD_UP_RED]
    bird_index = 0
    choose_bird = bird_list[bird_index]

    score = 0
    your_score = 0

    tube1_pass = False
    tube2_pass = False
    tube3_pass = False

    TUBE_VELOCITY = 3
    game_active = False
    
    ISSNOWFALL = False
    point_level = [10,25,30,35,40]
    isStart = False
    isWin = False
    pausing = False
    # retry for RETRY button
    retry = False
    next_level = False

    pausing_bird_drop_velocity = 0

    def snow_fall_effect():
        global snowFall 
        snowFall = []
        for i in range(50): # from 0 to 49
            # x = random.randrange(0+500+180,500+500+180)
            # y = random.randrange(-880,-180)
            x = random.randrange(0,500)
            y = random.randrange(-50,-10)
            snowFall.append([x,y])
    def new_snow_effect():
        for i in range(len(snowFall)):
            pygame.draw.circle(SCREEN,'white',snowFall[i],5) # tham số cuối cùng là bán kính
            snowFall[i][0] -= 1
            snowFall[i][1] += 1
            if snowFall[i][1] > 700 or snowFall[i][0] < 0:
                y = random.randrange(-50,-10)
                snowFall[i][1] = y
                x = random.randrange(0,500)
                snowFall[i][0] = x
    
    while True: 
        # print(LEVEL)
        if x_pos_play <= -1000 and ISSNOWFALL == False:
            snow_fall_effect()
            ISSNOWFALL = True
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        
        SCREEN.fill('black')

        # background
        bg1 = SCREEN.blit(PLAY_BG_IMG,(bg_x_pos,0))
        bg2 = SCREEN.blit(PLAY_BG_IMG,(bg_x_pos+WIDTH,0))
        bg3 = SCREEN.blit(PLAY_BG_IMG,(bg_x_pos+(WIDTH*2),0))
        bg4 = SCREEN.blit(SNOW_MOUNTAIN_IMG,(bg_x_pos+(WIDTH*3),0))
        bg5 = SCREEN.blit(SNOW_MOUNTAIN_IMG,(bg_x_pos+(WIDTH*4),0))
        bg6 = SCREEN.blit(SNOW_MOUNTAIN_IMG,(bg_x_pos+(WIDTH*5),0))
        bg_x_pos -= 2

        # draw floor
        floor1 = SCREEN.blit(FLOOR,(floor_x_pos,600))
        floor2 = SCREEN.blit(FLOOR,(floor_x_pos+WIDTH,600)) 
        floor_x_pos -= 2
        if floor_x_pos <= -WIDTH:
            floor_x_pos = 0

        # draw sky
        SKY = pygame.draw.rect(SCREEN,'white',[0,-10,WIDTH,11])
        if ISSNOWFALL:
            new_snow_effect()
        if game_active:
            if retry:
                GRAVITY = 0.5
                retry = False
            x_pos_play -= 2

            # draw pipes
            tube1_img = pygame.transform.scale(TUBE_IMG,(TUBE_WIDTH,tube1_height))
            tube1 = SCREEN.blit(tube1_img,(tube1_x,0))
            tube2_img = pygame.transform.scale(TUBE_IMG,(TUBE_WIDTH,tube2_height))
            tube2 = SCREEN.blit(tube2_img,(tube2_x,0))
            tube3_img = pygame.transform.scale(TUBE_IMG,(TUBE_WIDTH,tube3_height))
            tube3 = SCREEN.blit(tube3_img,(tube3_x,0))

            tube1_op_img = pygame.transform.scale(TUBE_OP_IMG,(TUBE_WIDTH,tube1_op_height))
            tube1_op = SCREEN.blit(tube1_op_img,(tube1_x,tube1_height+TUBE_GAP))
            tube2_op_img = pygame.transform.scale(TUBE_OP_IMG,(TUBE_WIDTH,tube2_op_height))
            tube2_op = SCREEN.blit(tube2_op_img,(tube2_x,tube2_height+TUBE_GAP))
            tube3_op_img = pygame.transform.scale(TUBE_OP_IMG,(TUBE_WIDTH,tube3_op_height))
            tube3_op = SCREEN.blit(tube3_op_img,(tube3_x,tube3_height+TUBE_GAP))

            # move pipe to left
            tube1_x -= TUBE_VELOCITY
            tube2_x -= TUBE_VELOCITY
            tube3_x -= TUBE_VELOCITY

            # create new pipes
            if tube1_x < -TUBE_WIDTH:
                tube1_x = 550
                tube1_height = randint(100,350)
                tube1_op_height = HEIGHT - (tube1_height + TUBE_GAP + 100)
                tube1_pass = False
            if tube2_x < -TUBE_WIDTH:
                tube2_x = 550
                tube2_height = randint(100,350)
                tube2_op_height = HEIGHT - (tube2_height + TUBE_GAP + 100)
                tube2_pass = False
            if tube3_x < -TUBE_WIDTH:
                tube3_x = 550
                tube3_height = randint(100,350)
                tube3_op_height = HEIGHT - (tube3_height + TUBE_GAP + 100)
                tube3_pass = False
            
            # draw bird
            # bird = SCREEN.blit(BIRD_IMG,(x_bird,y_bird))
            # y_bird += bird_drop_velocity  # bird drop by gravity
            # bird_drop_velocity += GRAVITY

            bird_drop_velocity += GRAVITY
            rotate_bird = pygame.transform.rotozoom(choose_bird,-bird_drop_velocity*3,1)
            y_bird += bird_drop_velocity
            bird = SCREEN.blit(rotate_bird,(x_bird,y_bird))

            # score
            if tube1_x + TUBE_WIDTH <= x_bird and tube1_pass == False:
                score += 1
                tube1_pass = True
                SCORE_SOUND.play()
            if tube2_x + TUBE_WIDTH <= x_bird and tube2_pass == False:
                score += 1
                tube2_pass = True
                SCORE_SOUND.play()
            if tube3_x + TUBE_WIDTH <= x_bird and tube3_pass == False:
                score += 1
                tube3_pass = True
                SCORE_SOUND.play()

            # score text
            SCORE_TEXT = get_font(25).render("Score: " + str(score),True,'white')
            SCREEN.blit(SCORE_TEXT,(120,5))

            # check colitions
            tubes = [tube1,tube2,tube3,tube1_op,tube2_op,tube3_op,SKY,floor1,floor2]
            for tube in tubes:
                if bird.colliderect(tube):
                    HIT_SOUND.play()
                    TUBE_VELOCITY = 0
                    bird_drop_velocity = 0
                    your_score = score
                    pygame.time.delay(500)
                    game_active = False

            for i in range(1,6):
                if LEVEL == i and score == point_level[i-1]:
                    isWin = True
                    game_active = False
                    your_score = score
                    pygame.time.delay(500)
                    break

            if pausing:
                pausing_bird_drop_velocity = bird_drop_velocity
                bird_drop_velocity = 0
                TUBE_VELOCITY = 0
                GRAVITY = 0
        else:
            if isStart:
                if isWin:
                    if next_level:
                        LEVEL += 1
                        next_level = False
                        isWin = False
                        isStart = False
                        score = 0
                    else:
                        SCREEN.blit(PLAY_BG_IMG,(0,0))
                        you_win_txt = GAME_FONT.render("You win!!!",True,'green')
                        you_win_rect = you_win_txt.get_rect(center=(250,50))
                        SCREEN.blit(you_win_txt,you_win_rect)
                        your_score_txt = GAME_FONT.render("Your Score: "+str(your_score),True,'white')
                        your_score_rect = your_score_txt.get_rect(center=(250,125))
                        SCREEN.blit(your_score_txt,your_score_rect)
                        SCREEN.blit(GAME_OVER,GAME_OVER_RECT)
                        PLAY_BACK = Button(image=OPTION_CONTROL_BG,pos=(100,630),text_input='BACK',font=get_font(45),base_color='red',hovering_color='white')
                        RETRY_BTN = Button(image=OPTION_CONTROL_BG,pos=(250,630),text_input='RETRY',font=get_font(45),base_color='red',hovering_color='white')
                        global NEXT_LEVEL_BTN
                        NEXT_LEVEL_BTN = Button(image=OPTION_CONTROL_BG,pos=(395,630),text_input='NEXT',font=get_font(45),base_color='red',hovering_color='white')
                        for button in [PLAY_BACK,RETRY_BTN,NEXT_LEVEL_BTN]:
                            button.changeColor(PLAY_MOUSE_POS)
                            button.update(SCREEN)
                else:
                    SCREEN.blit(PLAY_BG_IMG,(0,0))
                    SCREEN.blit(GAME_LOSS,GAME_LOSS_RECT)
                    your_score_txt = GAME_FONT.render("Your Score: "+str(your_score),True,'white')
                    your_score_rect = your_score_txt.get_rect(center=(250,125))
                    SCREEN.blit(your_score_txt,your_score_rect)
                    SCREEN.blit(GAME_OVER,GAME_OVER_RECT)
                    PLAY_BACK = Button(image=OPTION_CONTROL_BG,pos=(100,630),text_input='BACK',font=get_font(45),base_color='red',hovering_color='white')
                    PLAY_BACK.changeColor(PLAY_MOUSE_POS)
                    PLAY_BACK.update(SCREEN)
                    RETRY_BTN = Button(image=OPTION_CONTROL_BG,pos=(250,630),text_input='RETRY',font=get_font(45),base_color='red',hovering_color='white')
                    RETRY_BTN.changeColor(PLAY_MOUSE_POS)
                    RETRY_BTN.update(SCREEN)

            else:
                SCREEN.blit(PLAY_BG_IMG,(0,0))
                your_score_txt = GAME_FONT.render("Your Score: "+str(your_score),True,'white')
                your_score_rect = your_score_txt.get_rect(center=(250,50))
                level_txt = GAME_FONT.render("Level "+str(LEVEL),True,'red')
                level_txt_rect = level_txt.get_rect(center=(250,125))
                SCREEN.blit(your_score_txt,your_score_rect)
                SCREEN.blit(level_txt,level_txt_rect)
                SCREEN.blit(GAME_OVER,GAME_OVER_RECT)
                PLAY_BACK = Button(image=OPTION_CONTROL_BG,pos=(100,630),text_input='BACK',font=get_font(45),base_color='red',hovering_color='white')
                PLAY_BACK.changeColor(PLAY_MOUSE_POS)
                PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()
                if RETRY_BTN.checkForInput(PLAY_MOUSE_POS):
                    pygame.time.delay(500)
                    game_active = True
                    retry = True
                    x_bird = 50 
                    y_bird = 300
                    tube1_x = 500
                    tube2_x = 700
                    tube3_x = 900
                    TUBE_VELOCITY = 3
                    score = 0
                    x_pos_play = 0
                    ISSNOWFALL = False
                    isStart = True
                    bg_x_pos = 0
                    bird_drop_velocity = 0
                    GRAVITY = 0
                if RETRY_BTN.checkForInput(PLAY_MOUSE_POS) and isWin:
                    isWin = False
                if isWin and NEXT_LEVEL_BTN.checkForInput(PLAY_MOUSE_POS):
                    next_level = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_drop_velocity = 0
                    bird_drop_velocity -= 7
                    FLAP_SOUND.play()
                    if game_active == False:
                        pygame.mixer.unpause()
                        game_active = True
                        x_bird = 50 
                        y_bird = 400
                        tube1_x = 500
                        tube2_x = 700
                        tube3_x = 900
                        TUBE_VELOCITY = 3
                        score = 0
                        x_pos_play = 0
                        ISSNOWFALL = False
                        isStart = True
                        bg_x_pos = 0
                if event.key == pygame.K_SPACE and isWin:
                    isWin = False
                if event.key == pygame.K_p and pausing == False:
                    pausing = True
                    
                if event.key == pygame.K_c and pausing:
                    pausing = False
                    bird_drop_velocity = pausing_bird_drop_velocity
                    TUBE_VELOCITY = 3
                    GRAVITY = 0.5
            if event.type == birdflap:
                if bird_index < 2:
                    bird_index += 1
                else:
                    bird_index = 0
                choose_bird = bird_list[bird_index]
                        
        pygame.display.update()
        CLOCK.tick(60)  

def main_menu(bird_selected = 0,level = LEVEL):
    menu_x_pos = 0
    while True:
        CLOCK.tick(60)
        SCREEN.blit(BG_IMG,(menu_x_pos,0))
        SCREEN.blit(BG_IMG,(menu_x_pos+WIDTH,0))
        menu_x_pos -= 2
        if menu_x_pos <= -WIDTH:
            menu_x_pos = 0
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # pygame.draw.rect(SCREEN,'#919191',(WIDTH-50,0,50,50))
        TUTOR_BTN = Button(image=TUTOR_IMG,pos=(WIDTH-25,25),text_input='',font=get_font(0),base_color='red',hovering_color='white')

        BIRD_HOME_RECT = BIRD_MID_YELLOW.get_rect(center=(250,50))
        SELECT_BIRD = BIRD_LIST[bird_selected]
        SCREEN.blit(SELECT_BIRD,BIRD_HOME_RECT)

        MENU_TEXT = get_font(30).render('Bird Game',True,'red')
        MENU_RECT = MENU_TEXT.get_rect(center=(250,100))  # tọa độ tâm và có chiều cao và chiều rộng bao trùm vật thể

        LEVEL_TEXT = get_font(30).render("LEVEL " + str(LEVEL),True,'white')
        LEVEL_RECT = LEVEL_TEXT.get_rect(center=(250,150))

        PLAY_BUTTON = Button(image=MENU_BTN_BG,pos=(250,250),text_input='PLAY',font=get_font(45),base_color='white',hovering_color='red')
        OPTIONS_BUTTON = Button(image=MENU_BTN_BG,pos=(250,400),text_input='OPTIONS',font=get_font(45),base_color='white',hovering_color='red')
        QUIT_BUTTON = Button(image=MENU_BTN_BG,pos=(250,550),text_input='QUIT',font=get_font(45),base_color='white',hovering_color='red')

        SCREEN.blit(MENU_TEXT,MENU_RECT)
        SCREEN.blit(LEVEL_TEXT,LEVEL_RECT)

        for button in [PLAY_BUTTON,OPTIONS_BUTTON,QUIT_BUTTON,TUTOR_BTN]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if TUTOR_BTN.checkForInput(MENU_MOUSE_POS):
                    tutor()
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play(LEVEL,bird_selected)
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()

main_menu()

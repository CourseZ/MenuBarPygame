import pygame,sys
from button import Button

# pygame.draw.rect(SCREEN,color,[x,y,width=,height],w,border-radius)

pygame.init()
SCREEN = pygame.display.set_mode((500,700))
pygame.display.set_caption("Game Bird")

BG_IMG = pygame.image.load('img/menu_game_bg.png')
BG_IMG = pygame.transform.scale(BG_IMG,(500,700))

BTN_BG = pygame.image.load('img/btn_bg.png')
BTN_BG = pygame.transform.scale(BTN_BG,(300,100))
running = True

def get_font(size):
    return pygame.font.SysFont('sans',size,True)

def play():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill('black')

        PLAY_TEXT = get_font(45).render('This is a PLAY screen',True,'white')
        PLAY_RECT = PLAY_TEXT.get_rect(center=(250,250))
        SCREEN.blit(PLAY_TEXT,PLAY_RECT)

        PLAY_BACK = Button(image=None,pos=(250,600),text_input='BACK',font=get_font(45),base_color='red',hovering_color='white')
        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()
        pygame.display.update()

def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill('white')

        OPTIONS_TEXT = get_font(45).render('This is the OPTIONS creen',True,'red')
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(250,250))
        SCREEN.blit(OPTIONS_TEXT,OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None,pos=(250,600),text_input='BACK',font=get_font(45),base_color='red',hovering_color='white')
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()
        pygame.display.update()

def main_menu():
    while True:
        SCREEN.blit(BG_IMG,(0,0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(30).render('Game Bird',True,'red')
        MENU_RECT = MENU_TEXT.get_rect(center=(250,100))

        PLAY_BUTTON = Button(image=None,pos=(250,250),text_input='PLAY',font=get_font(45),base_color='white',hovering_color='red')
        OPTIONS_BUTTON = Button(image=None,pos=(250,400),text_input='OPTIONS',font=get_font(45),base_color='white',hovering_color='red')
        QUIT_BUTTON = Button(image=None,pos=(250,550),text_input='QUIT',font=get_font(45),base_color='white',hovering_color='red')

        # 250,250 center
        # 250,400
        # 250,550

        btn1 = pygame.draw.rect(SCREEN,'#b68f40',[100,250-50,300,100],border_radius=50)
        btn11 = pygame.draw.rect(SCREEN,'#FFC10A',[110,250-50+10,300-20,80],border_radius=50)
        btn111 = pygame.draw.rect(SCREEN,'#919191',[120,250-50+20,300-40,60],border_radius=50)

        btn2 = pygame.draw.rect(SCREEN,'#b68f40',[100,400-50,300,100],border_radius=50)
        btn22 = pygame.draw.rect(SCREEN,'#FFC10A',[110,400-50+10,300-20,80],border_radius=50)
        btn222 = pygame.draw.rect(SCREEN,'#919191',[120,400-50+20,300-40,60],border_radius=50)

        btn3 = pygame.draw.rect(SCREEN,'#b68f40',[100,550-50,300,100],border_radius=50)
        btn33 = pygame.draw.rect(SCREEN,'#FFC10A',[110,550-50+10,300-20,80],border_radius=50)
        btn333 = pygame.draw.rect(SCREEN,'#919191',[120,550-50+20,300-40,60],border_radius=50)

        SCREEN.blit(MENU_TEXT,MENU_RECT)

        for button in [PLAY_BUTTON,OPTIONS_BUTTON,QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()

main_menu()
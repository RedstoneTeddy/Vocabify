import pygame
import sys
pygame.init()
display = pygame.display.set_mode([700, 600])
base_font = pygame.font.Font("images/calibri.ttf", 45)
usr_txt = ''
usr_inp_rect = pygame.Rect(400, 400, 320, 50)
color = pygame.Color('chartreuse4')
active = True
while True:
    for event in pygame.event.get():
	# if the user types QUIT then the screen will close
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()  
        if event.type == pygame.KEYDOWN:
			# Check for backspace
            if event.key == pygame.K_BACKSPACE:
                  usr_txt = usr_txt[:-1]
            else:
                usr_txt += event.unicode
                
    # draw rectangle and the argument passed which should be on-screen
    pygame.draw.rect(display, color, usr_inp_rect)
    txt_surface = base_font.render(str(usr_txt) , True, (255, 255, 255))
	# render at position stated in arguments
    print(usr_txt)
    display.blit(txt_surface, (usr_inp_rect.x+5, usr_inp_rect.y+5))
    # set the width of textfield so that text cannot get outside of user's text input
    usr_inp_rect.w = max(100, txt_surface.get_width()+10)
    # display.flip() will try to update only a portion of the screen to updated, not full area
    pygame.display.flip()
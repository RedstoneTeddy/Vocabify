from os import path as os_path
from os import chdir as os_chdir
from os import mkdir as os_mkdir
import pygame
import time
import easygui


pygame.init()

directory = os_path.dirname(os_path.abspath(__file__))
os_chdir(directory) #Small Bugfix, that in some situations, the code_path isn't correct



import functions
import logger

#Version
version = "0.3.2b"

debug = False
log = False
debug_clicked = False
fullscreen_pressed = False
data = functions.init_data(version)
logger.Add(data,"main","main",0,"This is the logger. Any logged Info will be in here...")


screen = pygame.display.set_mode(size=(1000,600),flags=pygame.RESIZABLE+pygame.SHOWN)
pygame.display.set_caption("Vocabify")


#Check for cards-folder and settings file
if os_path.exists("settings.dat"):
    functions.Load_settings(data)
else:
    functions.Save_settings(data)
if not(os_path.isdir("cards")):
    os_mkdir("cards")
    

#Object initialization
import menu
menu_obj = menu.Menu(data,screen)
import transmission
transmission_obj = transmission.Transmission(data,screen)
import tools.edit
edit_obj = tools.edit.Edit(data,screen)
import tools.learn
learn_obj = tools.learn.Learn(data,screen)
import tools.learn_cards
learn_cards_obj = tools.learn_cards.Learn(data,screen)
import tools.learn_multiple
learn_multiple_obj = tools.learn_multiple.Learn(data,screen)
import tools.learn_write
learn_write_obj = tools.learn_write.Learn(data,screen)



try:   
    while data.get("run") == True:
        start_time = time.time_ns()

        screen.fill(data.get("settings").get("color1"))
        
        if pygame.display.get_surface().get_size()[0] != data.get("width") or pygame.display.get_surface().get_size()[1] != data.get("height"):
            data["width"] = pygame.display.get_surface().get_size()[0]
            data["height"] = pygame.display.get_surface().get_size()[1]
            data["resize"] = True
        

        match data.get("mode"):
            case "menu":
                menu_obj.Main()
            case "edit":
                edit_obj.Main()
            case "learn":
                learn_obj.Main()
            case "learn_cards":
                learn_cards_obj.Main()
            case "learn_multiple":
                learn_multiple_obj.Main()
            case "learn_write":
                learn_write_obj.Main()
            case other:
                raise ValueError("Unknown mode!")


        transmission_obj.Main()
        #Debug & Logger
        if pygame.key.get_pressed()[pygame.K_q] == True:
            if pygame.key.get_pressed()[pygame.K_LCTRL] or pygame.key.get_pressed()[pygame.K_RCTRL]:
                if debug_clicked == False:
                    debug_clicked = True
                    debug = not(debug)
        else:
            if pygame.key.get_pressed()[pygame.K_l] == True:
                if pygame.key.get_pressed()[pygame.K_LCTRL] or pygame.key.get_pressed()[pygame.K_RCTRL]:
                    if debug_clicked == False:
                        debug_clicked = True
                        log = not(log)
            else:
                debug_clicked = False
        if debug == True:
            pygame.draw.rect(screen,(255,255,255),(0,0,200,66))
            functions.draw_text(f"AVG MSPF: {data.get('avg_mspf')}|{data.get('long_avg_mspf')}",data.get("font_data").get("20"),(0,0,0),(3,3),screen)
            functions.draw_text(f"Last Learn gen: {data.get('last_learn_generation_ms')}µs",data.get("font_data").get("20"),(0,0,0),(3,23),screen)
            functions.draw_text(f"Mouse Pos: {pygame.mouse.get_pos()}",data.get("font_data").get("20"),(0,0,0),(3,43),screen)
        if data.get("resize") == True:
            data["resize"] = False
        if log == True or data.get("log_timer") > 0:
            logger.Main(data,screen,log)
        
        if pygame.key.get_pressed()[pygame.K_LCTRL] or pygame.key.get_pressed()[pygame.K_RCTRL]:
            pygame.draw.rect(screen,(255,255,255),(data.get("width")-223,0,223,86))
            functions.draw_text("Debug-Keybindings",data.get("font_data").get("20"),(0,0,0),(data.get("width")-220,3),screen)
            functions.draw_text("Debug: CTRL+Q",data.get("font_data").get("20"),(0,0,0),(data.get("width")-220,23),screen)
            functions.draw_text("Logger: CTRL+L",data.get("font_data").get("20"),(0,0,0),(data.get("width")-220,43),screen)
            functions.draw_text("Learn-Algorithm: CTRL+P",data.get("font_data").get("20"),(0,0,0),(data.get("width")-220,63),screen)
        
        #Fullscreen
        if pygame.key.get_pressed()[pygame.K_F11] == True:
            if fullscreen_pressed == False:
                fullscreen_pressed = True
                if data.get("fullscreen") == True:
                    data["fullscreen"] = False
                    screen = pygame.display.set_mode(size=(1000,600),flags=pygame.RESIZABLE+pygame.SHOWN)
                    logger.Add(data,"main","Main",0,"Changed to Windowed Screen")
                else:
                    data["fullscreen"] = True
                    screen = pygame.display.set_mode(size=(0,0),flags=pygame.RESIZABLE+pygame.FULLSCREEN)
                    logger.Add(data,"main","Main",0,"Changed to Fullscreen")
        else:
            fullscreen_pressed = False
        

        if data.get("mouse_wheel") != None:
            data["mouse_wheel"] = None


        pygame.display.update()
        
        data["key_pressed"] = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                data["run"] = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    data["mouse_wheel"] = "up"
                if event.button == 5:
                    data["mouse_wheel"] = "down"
            if event.type == pygame.KEYDOWN:
                # Check for backspace
                if event.key == pygame.K_BACKSPACE:
                    data["key_pressed"] = "back"
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    data["key_pressed"] = "enter"
                elif event.key == pygame.K_TAB:
                    data["key_pressed"] = "tab"
                elif event.key == pygame.K_ESCAPE:
                    data["key_pressed"] = "esc"
                else:
                    if event.unicode not in ["^","¨","´","`","~"]:
                        data["key_pressed"] = event.unicode
        
        pygame.key.get_pressed()

        end_time = time.time_ns()
        data["mspf"] = round((end_time-start_time)/1000000,1)
        functions.calc_avg_mspf(data)

        # Wait until max mspf is reached
        if data.get("mspf") < 1000/60:
            time.sleep((1000/60-data.get("mspf"))/1000)
except:
    easygui.exceptionbox(f"A fatal Error occured in the Vocabify App and the program crashed! Log:\n{data.get('log_list')}","Vocabify-Error!")
    data["run"] = False
    raise


match data.get("mode"):
    case "edit":
        edit_obj.Save()
    case "learn":
        learn_obj.Save()


functions.Save_settings(data)
pygame.quit()







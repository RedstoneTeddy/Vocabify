from copy import deepcopy
import pygame
from pygame.locals import *
from pygame import mixer
from datetime import datetime
pygame.mixer.pre_init(44100,16,2,4096)
mixer.init()
pygame.init()


def Draw_text(text,font,text_color,x,y,SCREEN):
    img = font.render(text,True,text_color)
    SCREEN.blit(img, (x,y))

def Main(global_variables,SCREEN,is_shown):
    if is_shown == True:
        if global_variables.get("log_timer") >= 1000:
            SCREEN.fill((0,0,0))
            index = -1
            for msg in global_variables["log_list"]:
                index += 1
                match msg[2]:
                    case 0:
                        Draw_text(msg[0],global_variables.get("font_data").get("24"),(255,255,255),10,index*60+0,SCREEN)
                        Draw_text("-->  "+msg[1],global_variables.get("font_data").get("24"),(255,255,255),20,index*60+28,SCREEN)
                    case 1:
                        Draw_text(msg[0],global_variables.get("font_data").get("24"),(255,239,0),10,index*60+0,SCREEN)
                        Draw_text("-->  "+msg[1],global_variables.get("font_data").get("24"),(255,239,0),20,index*60+28,SCREEN)
                    case 2:
                        Draw_text(msg[0],global_variables.get("font_data").get("24"),(255,111,85),10,index*60+0,SCREEN)
                        Draw_text("-->  "+msg[1],global_variables.get("font_data").get("24"),(255,111,85),20,index*60+28,SCREEN)
                    case 3:
                        Draw_text(msg[0],global_variables.get("font_data").get("24"),(239,0,0),10,index*60+0,SCREEN)
                        Draw_text("-->  "+msg[1],global_variables.get("font_data").get("24"),(239,0,0),20,index*60+28,SCREEN)
                    case _:
                        Draw_text(msg[0],global_variables.get("font_data").get("24"),(239,0,0),10,index*60+0,SCREEN)
                        Draw_text("-->  "+msg[1],global_variables.get("font_data").get("24"),(239,0,0),20,index*60+28,SCREEN)
        else:
            global_variables["log_timer"] += (1000/60)*2
            if global_variables.get("log_timer") > 1000:
                global_variables["log_timer"] = 1000
            rect = (0,
                    global_variables.get("height")*(1000-global_variables.get("log_timer"))/1000,
                    global_variables.get("width"),
                    global_variables.get("height"))
            pygame.draw.rect(SCREEN,(0,0,0),rect)
    else:        
        global_variables["log_timer"] -= (1000/60)*2
        if global_variables.get("log_timer") <= 0:
            global_variables["log_timer"] = 0
        if global_variables.get("log_timer") > 0:
            pygame.draw.rect(SCREEN,(0,0,0),(0,global_variables.get("height")*(1000-global_variables.get("log_timer"))/1000,global_variables.get("width"),global_variables.get("height")))
        
 
     
    
     
     
        
#Message to the console:
# %SCRIPTNAME%.py/%FUNCTIONNAME%] - %MESSAGESTATUS% - %TEXT%
#MESSAGESTATUS: (0)Info, (1)Warning, (2)Small_Error, (3)Fatal
        
def Add(global_variables,scriptname,functionname,status,text):
    current_time = datetime.now()
    current_time = current_time.strftime("%H:%M:%S")
    if len(global_variables.get("log_list")) > 15:
        del global_variables["log_list"][-1]

    match status:
        case 0:
            output = scriptname + ".py  -  " + functionname + "  -  Info - " + current_time
        case 1:
            output = scriptname + ".py  -  " + functionname + "  -  Warning - " + current_time
        case 2:
            output = scriptname + ".py  -  " + functionname + "  -  Small Error - " + current_time
        case 3:
            output = scriptname + ".py  -  " + functionname + "  -  Fatal - " + current_time
        case _:
            output = "LOG ERROR"
            
    global_variables["log_list"].insert(0,[output,str(text),status])
    #[1line,2line,status]
    




import buttons
import pygame
import functions
pygame.init()

def Calculated_moving_pos(start:list,end:list,max_time:int,time:int):
    '''
    Calculates the position at a given time of a moving object

    Parameters:
    start -> A list of the starting position
    end -> A list of the ending position
    max_time -> How long it should take to move from start to end
    time -> The current time

    Returns:
    The current position
    '''
    vector_start_to_end = (end[0]-start[0], end[1]-start[1])
    current_pos = (
        start[0] + vector_start_to_end[0]/max_time*time,
        start[1] + vector_start_to_end[1]/max_time*time
    )
    return current_pos



class Menu():
    '''
    A class that handles the main menu.
    '''
    def __init__(self, data:dict,screen:object) -> object:
        '''
        Initializes the menu object.

        Parameters:
        data -> The main data dictionary
        screen -> The screen object

        Returns:
        Object
        '''
        self.data = data
        self.screen = screen
        self.animation_timer = 0
        self.current_selection = None
        self.animation_to = None

        self.button_obj = buttons.Button(screen,data)
        self.img_learn = pygame.transform.scale(pygame.image.load("images/menu/learn.png").convert_alpha(),(64,64))
        self.img_learn_custom = pygame.transform.scale(pygame.image.load("images/menu/learn_custom.png").convert_alpha(),(64,64))
        self.img_edit = pygame.transform.scale(pygame.image.load("images/menu/edit.png").convert_alpha(),(64,64))
        self.img_settings = pygame.transform.scale(pygame.image.load("images/menu/settings.png").convert_alpha(),(64,64))
        self.img_home = pygame.transform.scale(pygame.image.load("images/menu/home.png").convert_alpha(),(32,32))

    def Main(self):
        self.screen.fill(self.data.get("settings").get("color1"))
        functions.draw_text("Vocabify", self.data.get("font_data").get("title"),self.data["settings"]["color_text"],(self.data.get("width")//2-160,50),self.screen)



        match self.current_selection:
            case "settings":
                if self.animation_to == "settings":
                    if self.button_obj.Button((self.data.get("width")//2-220,self.data.get("height")//2-100,200,44),2,(255,255,255),(0,0,0),["Bright Mode",f"Activated: {self.data.get('settings').get('color1')==(255,255,255)}"],18):
                        self.data["settings"]["color1"] = (255,255,255)
                        self.data["settings"]["color2"] = (0,0,0)
                        self.data["settings"]["color3"] = (200,200,200)
                        self.data["settings"]["color_text"] = (0,0,0)
                        functions.Save_settings(self.data)
                    if self.button_obj.Button((self.data.get("width")//2-220,self.data.get("height")//2-50,200,44),2,(20,20,20),(255,255,255),["Dark Mode",f"Activated: {self.data.get('settings').get('color1')==(20,20,20)}"],18):
                        self.data["settings"]["color1"] = (20,20,20)
                        self.data["settings"]["color2"] = (255,255,255)
                        self.data["settings"]["color3"] = (80,80,80)
                        self.data["settings"]["color_text"] = (255,255,255)
                        functions.Save_settings(self.data)









        #Main Button menu
        match self.current_selection:
            case None:
                match self.animation_to:
                    case None:
                        if self.animation_timer == 0:
                            if self.button_obj.Button([self.data.get("width")//2-140,self.data.get("height")//2-140,130,130],3,(232,145,30),self.data.get("settings").get("color2"),["Learn"],20,self.img_learn):
                                self.animation_timer = 0
                                self.animation_to = "learn"
                            if self.button_obj.Button([self.data.get("width")//2-140,self.data.get("height")//2+10,130,130],3,(0,133,13),self.data.get("settings").get("color2"),["Custom","Learning"],20,self.img_learn_custom):
                                self.animation_timer = 0
                                self.animation_to = "learn_custom"
                            if self.button_obj.Button([self.data.get("width")//2+10,self.data.get("height")//2-140,130,130],3,(64,55,212),self.data.get("settings").get("color2"),["Cards"],20,self.img_edit):
                                self.animation_timer = 0
                                self.animation_to = "edit"
                            if self.button_obj.Button([self.data.get("width")//2+10,self.data.get("height")//2+10,130,130],3,(181,60,60),self.data.get("settings").get("color2"),["Settings"],20,self.img_settings):
                                self.animation_timer = 0
                                self.animation_to = "settings"
                        else:
                            self.animation_timer = 0

                    case "learn":
                        self.animation_timer += 1
                        if self.animation_timer < 16:
                            moving_pos = Calculated_moving_pos([self.data.get("width")//2-140,self.data.get("height")//2-140],[self.data.get("width")//2,self.data.get("height")//2-110],15,self.animation_timer)
                            self.button_obj.Button([*moving_pos,130,130],3,(232,145,30),self.data.get("settings").get("color2"),["Learn"],20,self.img_learn)
                        elif self.animation_timer < 31:                            
                            moving_pos = Calculated_moving_pos([self.data.get("width")//2+30,self.data.get("height")//2-90],[self.data.get("width")//2+30,self.data.get("height")//2+40],15,self.animation_timer-15)
                            self.button_obj.Button([*moving_pos,70,70],3,self.data.get("settings").get("color3"),self.data.get("settings").get("color2"),["Home"],20,self.img_home)
                            self.button_obj.Button([self.data.get("width")//2,self.data.get("height")//2-110,130,130],3,(232,145,30),self.data.get("settings").get("color2"),["Learn"],20,self.img_learn)
                        else:
                            self.button_obj.Button([self.data.get("width")//2,self.data.get("height")//2-110,130,130],3,(232,145,30),self.data.get("settings").get("color2"),["Learn"],20,self.img_learn)
                            self.button_obj.Button([self.data.get("width")//2+30,self.data.get("height")//2+40,70,70],3,self.data.get("settings").get("color3"),self.data.get("settings").get("color2"),["Home"],20,self.img_home)
                            self.animation_timer = 0
                            self.current_selection = "learn"

                    case "learn_custom":
                        self.animation_timer += 1
                        if self.animation_timer < 16:
                            moving_pos = Calculated_moving_pos([self.data.get("width")//2-140,self.data.get("height")//2+10],[self.data.get("width")//2,self.data.get("height")//2-110],15,self.animation_timer)
                            self.button_obj.Button([*moving_pos,130,130],3,(0,133,13),self.data.get("settings").get("color2"),["Custom","Learning"],20,self.img_learn_custom)
                        elif self.animation_timer < 31:                            
                            moving_pos = Calculated_moving_pos([self.data.get("width")//2+30,self.data.get("height")//2-90],[self.data.get("width")//2+30,self.data.get("height")//2+40],15,self.animation_timer-15)
                            self.button_obj.Button([*moving_pos,70,70],3,self.data.get("settings").get("color3"),self.data.get("settings").get("color2"),["Home"],20,self.img_home)
                            self.button_obj.Button([self.data.get("width")//2,self.data.get("height")//2-110,130,130],3,(0,133,13),self.data.get("settings").get("color2"),["Custom","Learning"],20,self.img_learn_custom)
                        else:
                            self.button_obj.Button([self.data.get("width")//2,self.data.get("height")//2-110,130,130],3,(0,133,13),self.data.get("settings").get("color2"),["Custom","Learning"],20,self.img_learn_custom)
                            self.button_obj.Button([self.data.get("width")//2+30,self.data.get("height")//2+40,70,70],3,self.data.get("settings").get("color3"),self.data.get("settings").get("color2"),["Home"],20,self.img_home)
                            self.animation_timer = 0
                            self.current_selection = "learn_custom"

                    case "edit":
                        self.animation_timer += 1
                        if self.animation_timer < 16:
                            moving_pos = Calculated_moving_pos([self.data.get("width")//2+10,self.data.get("height")//2-140],[self.data.get("width")//2,self.data.get("height")//2-110],15,self.animation_timer)
                            self.button_obj.Button([*moving_pos,130,130],3,(64,55,212),self.data.get("settings").get("color2"),["Cards"],20,self.img_edit)
                        elif self.animation_timer < 31:                            
                            moving_pos = Calculated_moving_pos([self.data.get("width")//2+30,self.data.get("height")//2-90],[self.data.get("width")//2+30,self.data.get("height")//2+40],15,self.animation_timer-15)
                            self.button_obj.Button([*moving_pos,70,70],3,self.data.get("settings").get("color3"),self.data.get("settings").get("color2"),["Home"],20,self.img_home)
                            self.button_obj.Button([self.data.get("width")//2,self.data.get("height")//2-110,130,130],3,(64,55,212),self.data.get("settings").get("color2"),["Cards"],20,self.img_edit)
                        else:
                            self.button_obj.Button([self.data.get("width")//2,self.data.get("height")//2-110,130,130],3,(64,55,212),self.data.get("settings").get("color2"),["Cards"],20,self.img_edit)
                            self.button_obj.Button([self.data.get("width")//2+30,self.data.get("height")//2+40,70,70],3,self.data.get("settings").get("color3"),self.data.get("settings").get("color2"),["Home"],20,self.img_home)
                            self.animation_timer = 0
                            self.current_selection = "edit"

                    case "settings":
                        self.animation_timer += 1
                        if self.animation_timer < 16:
                            moving_pos = Calculated_moving_pos([self.data.get("width")//2+10,self.data.get("height")//2+10],[self.data.get("width")//2,self.data.get("height")//2-110],15,self.animation_timer)
                            self.button_obj.Button([*moving_pos,130,130],3,(181,60,60),self.data.get("settings").get("color2"),["Settings"],20,self.img_settings)
                        elif self.animation_timer < 31:                            
                            moving_pos = Calculated_moving_pos([self.data.get("width")//2+30,self.data.get("height")//2-90],[self.data.get("width")//2+30,self.data.get("height")//2+40],15,self.animation_timer-15)
                            self.button_obj.Button([*moving_pos,70,70],3,self.data.get("settings").get("color3"),self.data.get("settings").get("color2"),["Home"],20,self.img_home)
                            self.button_obj.Button([self.data.get("width")//2,self.data.get("height")//2-110,130,130],3,(181,60,60),self.data.get("settings").get("color2"),["Settings"],20,self.img_settings)
                        else:
                            self.button_obj.Button([self.data.get("width")//2,self.data.get("height")//2-110,130,130],3,(181,60,60),self.data.get("settings").get("color2"),["Settings"],20,self.img_settings)
                            self.button_obj.Button([self.data.get("width")//2+30,self.data.get("height")//2+40,70,70],3,self.data.get("settings").get("color3"),self.data.get("settings").get("color2"),["Home"],20,self.img_home)
                            self.animation_timer = 0
                            self.current_selection = "settings"
            


            # Learn option
            case "learn":
                if self.animation_to == "learn":
                    self.button_obj.Button([self.data.get("width")//2,self.data.get("height")//2-110,130,130],3,(232,145,30),self.data.get("settings").get("color2"),["Learn"],20,self.img_learn)
                    if self.button_obj.Button([self.data.get("width")//2+30,self.data.get("height")//2+40,70,70],3,self.data.get("settings").get("color3"),self.data.get("settings").get("color2"),["Home"],20,self.img_home):
                        self.animation_to = None
                        self.animation_timer = 31
                else:
                    self.animation_timer -= 1
                    if self.animation_timer < 16:
                        moving_pos = Calculated_moving_pos([self.data.get("width")//2-140,self.data.get("height")//2-140],[self.data.get("width")//2,self.data.get("height")//2-110],15,self.animation_timer)
                        self.button_obj.Button([*moving_pos,130,130],3,(232,145,30),self.data.get("settings").get("color2"),["Learn"],20,self.img_learn)
                        if self.animation_timer == 0:
                            self.animation_to = None
                            self.current_selection = None
                    else:                            
                        moving_pos = Calculated_moving_pos([self.data.get("width")//2+30,self.data.get("height")//2-90],[self.data.get("width")//2+30,self.data.get("height")//2+40],15,self.animation_timer-15)
                        self.button_obj.Button([*moving_pos,70,70],3,self.data.get("settings").get("color3"),self.data.get("settings").get("color2"),["Home"],20,self.img_home)
                        self.button_obj.Button([self.data.get("width")//2,self.data.get("height")//2-110,130,130],3,(232,145,30),self.data.get("settings").get("color2"),["Learn"],20,self.img_learn)


                    
            # Learn custom option
            case "learn_custom":
                if self.animation_to == "learn_custom":
                    self.button_obj.Button([self.data.get("width")//2,self.data.get("height")//2-110,130,130],3,(0,133,13),self.data.get("settings").get("color2"),["Custom","Learning"],20,self.img_learn_custom)
                    if self.button_obj.Button([self.data.get("width")//2+30,self.data.get("height")//2+40,70,70],3,self.data.get("settings").get("color3"),self.data.get("settings").get("color2"),["Home"],20,self.img_home):
                        self.animation_to = None
                        self.animation_timer = 31
                else:
                    self.animation_timer -= 1
                    if self.animation_timer < 16:
                        moving_pos = Calculated_moving_pos([self.data.get("width")//2-140,self.data.get("height")//2+10],[self.data.get("width")//2,self.data.get("height")//2-110],15,self.animation_timer)
                        self.button_obj.Button([*moving_pos,130,130],3,(0,133,13),self.data.get("settings").get("color2"),["Custom","Learning"],20,self.img_learn_custom)
                        if self.animation_timer == 0:
                            self.animation_to = None
                            self.current_selection = None
                    else:                                    
                        moving_pos = Calculated_moving_pos([self.data.get("width")//2+30,self.data.get("height")//2-90],[self.data.get("width")//2+30,self.data.get("height")//2+40],15,self.animation_timer-15)
                        self.button_obj.Button([*moving_pos,70,70],3,self.data.get("settings").get("color3"),self.data.get("settings").get("color2"),["Home"],20,self.img_home)
                        self.button_obj.Button([self.data.get("width")//2,self.data.get("height")//2-110,130,130],3,(0,133,13),self.data.get("settings").get("color2"),["Custom","Learning"],20,self.img_learn_custom)


                    
            # Edit option
            case "edit":
                if self.animation_to == "edit":
                    self.button_obj.Button([self.data.get("width")//2,self.data.get("height")//2-110,130,130],3,(64,55,212),self.data.get("settings").get("color2"),["Cards"],20,self.img_edit)
                    if self.button_obj.Button([self.data.get("width")//2+30,self.data.get("height")//2+40,70,70],3,self.data.get("settings").get("color3"),self.data.get("settings").get("color2"),["Home"],20,self.img_home):
                        self.animation_to = None
                        self.animation_timer = 31
                else:
                    self.animation_timer -= 1
                    if self.animation_timer < 16:
                        moving_pos = Calculated_moving_pos([self.data.get("width")//2+10,self.data.get("height")//2-140],[self.data.get("width")//2,self.data.get("height")//2-110],15,self.animation_timer)
                        self.button_obj.Button([*moving_pos,130,130],3,(64,55,212),self.data.get("settings").get("color2"),["Cards"],20,self.img_edit)
                        if self.animation_timer == 0:
                            self.animation_to = None
                            self.current_selection = None
                    else:                               
                        moving_pos = Calculated_moving_pos([self.data.get("width")//2+30,self.data.get("height")//2-90],[self.data.get("width")//2+30,self.data.get("height")//2+40],15,self.animation_timer-15)
                        self.button_obj.Button([*moving_pos,70,70],3,self.data.get("settings").get("color3"),self.data.get("settings").get("color2"),["Home"],20,self.img_home)
                        self.button_obj.Button([self.data.get("width")//2,self.data.get("height")//2-110,130,130],3,(64,55,212),self.data.get("settings").get("color2"),["Cards"],20,self.img_edit)

                    

            # Settings option
            case "settings":
                if self.animation_to == "settings":
                    self.button_obj.Button([self.data.get("width")//2,self.data.get("height")//2-110,130,130],3,(181,60,60),self.data.get("settings").get("color2"),["Settings"],20,self.img_settings)
                    if self.button_obj.Button([self.data.get("width")//2+30,self.data.get("height")//2+40,70,70],3,self.data.get("settings").get("color3"),self.data.get("settings").get("color2"),["Home"],20,self.img_home):
                        self.animation_to = None
                        self.animation_timer = 31
                else:
                    self.animation_timer -= 1
                    if self.animation_timer < 16:
                        moving_pos = Calculated_moving_pos([self.data.get("width")//2+10,self.data.get("height")//2+10],[self.data.get("width")//2,self.data.get("height")//2-110],15,self.animation_timer)
                        self.button_obj.Button([*moving_pos,130,130],3,(181,60,60),self.data.get("settings").get("color2"),["Settings"],20,self.img_settings)
                        if self.animation_timer == 0:
                            self.animation_to = None
                            self.current_selection = None
                    else:                                     
                        moving_pos = Calculated_moving_pos([self.data.get("width")//2+30,self.data.get("height")//2-90],[self.data.get("width")//2+30,self.data.get("height")//2+40],15,self.animation_timer-15)
                        self.button_obj.Button([*moving_pos,70,70],3,self.data.get("settings").get("color3"),self.data.get("settings").get("color2"),["Home"],20,self.img_home)
                        self.button_obj.Button([self.data.get("width")//2,self.data.get("height")//2-110,130,130],3,(181,60,60),self.data.get("settings").get("color2"),["Settings"],20,self.img_settings)











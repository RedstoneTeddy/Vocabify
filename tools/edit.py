import buttons
import pygame
import functions
import easygui
import os
pygame.init()
from copy import deepcopy



class Edit():
    '''
    A class that handles the cards editing function of the programm.
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
        self.scroll_y = 0
        self.cards_data = []
        self.cards_front = []
        self.cards_back = []
        self.cards_phase = [] #In which phase the special-learn function should ask you, multiple-choice, write
        self.cards_last_wrong = [] #Penalty points
        self.all_right = [] #In total how many times you got it right
        self.all_wrong = [] #In total how many times you got it wrong

        self.button_obj = buttons.Button(screen,data)
        self.img_home = pygame.transform.scale(pygame.image.load("images/menu/home.png").convert_alpha(),(32,32))
        self.img_swap = pygame.transform.scale(pygame.image.load("images/menu/swap.png").convert_alpha(),(32,32))
        self.img_delete = pygame.transform.scale(pygame.image.load("images/menu/delete.png").convert_alpha(),(32,32))
        
        self.current_selection = -1
        self.tab_pressed = False
        self.auto_save_timer = 0


    def Main(self):
        self.screen.fill(self.data.get("settings").get("color1"))
        if self.cards_data == []:
            self.Load()
            if self.cards_data == []:
                self.cards_data = [None]
            self.scroll_y = 0
            self.current_selection = -1 #Nothing selected

        ###########################
        ###Show alternatives but separated with a semciolon, and also possibility to add alternative words with just a semicolon
        ###########################

        #Main Cards Front & Back
        functions.draw_text("Front",self.data["fonts"](22,self.data),self.data.get("settings").get("color2"),[self.data.get("width")//2-55,178+self.scroll_y],self.screen)
        functions.draw_text("Back",self.data["fonts"](22,self.data),self.data.get("settings").get("color2"),[self.data.get("width")//2+5,178+self.scroll_y],self.screen)
        for i in range(0,len(self.cards_front)*2+1):
            #Draw
            if i == len(self.cards_front)*2: #New Card
                new_card = False
                if self.button_obj.Button([90,(i//2)*50+200+self.scroll_y,self.data.get("width")-180,40],3,(64,55,212),self.data.get("settings").get("color2"),["+   New Card   +"],30):
                    new_card = True
                if i == self.current_selection or self.current_selection == -1:
                    if pygame.key.get_pressed()[pygame.K_SPACE] or pygame.key.get_pressed()[pygame.K_TAB] or pygame.key.get_pressed()[pygame.K_RETURN] or pygame.key.get_pressed()[pygame.K_KP_ENTER]:
                        new_card = True
                if new_card == True:
                    self.cards_front.append([""])
                    self.cards_back.append([""])
                    self.cards_phase.append(0)
                    self.cards_last_wrong.append(0)
                    self.all_right.append(0)
                    self.all_wrong.append(0)
                    self.current_selection = len(self.cards_front)*2-2

            else:
                #Delete word button
                if i%2==0: #Front
                    if self.button_obj.Button([self.data.get("width")-80,(i//2)*50+200+self.scroll_y,40,40],3,self.data.get("settings").get("color3"),self.data.get("settings").get("color2"),[],20,self.img_delete):
                        del self.cards_front[i//2]
                        del self.cards_back[i//2]
                        del self.cards_phase[i//2]
                        del self.cards_last_wrong[i//2]
                        del self.all_right[i//2]
                        del self.all_wrong[i//2]
                        self.current_selection -= 1
                        break
                        

                if self.current_selection == i:
                    if i%2==0: #Front
                        if self.button_obj.Button([90,(i//2)*50+200+self.scroll_y,self.data.get("width")//2-95,40],3,self.data.get("settings").get("color3"),self.data.get("settings").get("color2"),[self.cards_front[i//2][0]],20):
                            self.current_selection = i
                        if self.data.get("key_pressed") != None:
                            if self.data.get("key_pressed") == "back":
                                self.cards_front[i//2][0] = self.cards_front[i//2][0][:-1]
                            elif self.data.get("key_pressed") not in ["back","enter","tab","esc"]:
                                self.cards_front[i//2][0] += self.data.get("key_pressed")
                    else:
                        if self.button_obj.Button([self.data.get("width")//2+5,(i//2)*50+200+self.scroll_y,self.data.get("width")//2-95,40],3,self.data.get("settings").get("color3"),self.data.get("settings").get("color2"),[self.cards_back[i//2][0]],20):
                            self.current_selection = i
                        if self.data.get("key_pressed") != None:
                            if self.data.get("key_pressed") == "back":
                                self.cards_back[i//2][0] = self.cards_back[i//2][0][:-1]
                            elif self.data.get("key_pressed") not in ["back","enter","tab","esc"]:
                                self.cards_back[i//2][0] += self.data.get("key_pressed")
                else:
                    if i%2==0: #Front
                        if self.button_obj.Button([90,(i//2)*50+200+self.scroll_y,self.data.get("width")//2-95,40],3,self.data.get("settings").get("color1"),self.data.get("settings").get("color2"),[self.cards_front[i//2][0]],20):
                            self.current_selection = i
                    else:
                        if self.button_obj.Button([self.data.get("width")//2+5,(i//2)*50+200+self.scroll_y,self.data.get("width")//2-95,40],3,self.data.get("settings").get("color1"),self.data.get("settings").get("color2"),[self.cards_back[i//2][0]],20):
                            self.current_selection = i

            
            

        #Tab-Funciton
        if pygame.key.get_pressed()[pygame.K_TAB] or pygame.key.get_pressed()[pygame.K_RETURN]:
            if self.tab_pressed  == False:
                self.tab_pressed = True
                if self.current_selection < len(self.cards_front)*2:
                    self.current_selection += 1
        else:
            self.tab_pressed = False

        #Scroll Function
        if self.data.get("mouse_wheel") == "up" and self.scroll_y < 0:
            self.scroll_y += 50
        if self.data.get("mouse_wheel") == "down" and self.scroll_y > -len(self.cards_front)*50:
            self.scroll_y -= 50


        #Side Menu  
        pygame.draw.rect(self.screen,self.data.get("settings").get("color1"),(0,0,250,62))
        functions.draw_text("Active Cards:",self.data["fonts"](18,self.data),self.data.get("settings").get("color2"),(90,2),self.screen)
        functions.draw_text(self.data.get("cards"),self.data["fonts"](18,self.data),self.data.get("settings").get("color2"),(90,22),self.screen)
        functions.draw_text(f"{len(self.cards_front)} Cards",self.data["fonts"](18,self.data),self.data.get("settings").get("color2"),(90,42),self.screen)


        if self.button_obj.Button([10,90,70,70],3,self.data.get("settings").get("color3"),self.data.get("settings").get("color2"),["Swap"],20,self.img_swap):
            new_back = deepcopy(self.cards_front)
            self.cards_front = deepcopy(self.cards_back)
            self.cards_back = deepcopy(new_back)
        
    
        if self.button_obj.Button([10,10,70,70],3,self.data.get("settings").get("color3"),self.data.get("settings").get("color2"),["Home"],20,self.img_home):
            self.Save()
            self.data["change_mode"] = "menu"
            self.cards_data = []
        
        #Auto-Save
        self.auto_save_timer += 1
        if self.auto_save_timer > 60*60: #Every minute, 60frames per second, 60 seconds per minute
            self.auto_save_timer = 0
            self.Save()


        


    def Load(self) -> None:
        '''
        Loads the current card-set and writes it into the recent-cards list
        '''
        try:
            file_handler = open("cards/"+self.data.get("cards"),"r")
            self.cards_data = []
            self.cards_front = []
            self.cards_back = []
            self.cards_phase = []
            self.cards_last_wrong = []
            self.all_right = []
            self.all_wrong = []
            for line in file_handler.readlines():
                self.cards_data.append(eval(line))
            file_handler.close()

            for line in self.cards_data:
                self.cards_front.append(line[0])
                self.cards_back.append(line[1])
                self.cards_phase.append(line[2])
                self.cards_last_wrong.append(line[3])
                self.all_right.append(line[4])
                self.all_wrong.append(line[5])
        except FileNotFoundError:
            self.cards_data = []
            self.cards_front = []
            self.cards_back = []
            self.cards_phase = []
            self.cards_last_wrong = []
            self.all_right = []
            self.all_wrong = []


        if self.data["cards"] not in self.data["recent"]:
            if len(self.data.get("recent")) >= 5:
                del self.data["recent"][0]
            self.data["recent"].append(self.data["cards"])
        functions.Save_settings(self.data)


    def Save(self):
        '''
        Saves the current card-set and writes it into the recent-cards list
        '''
        file_handler = open("cards/"+self.data.get("cards"),"w")

        text = ""
        for i in range(0,len(self.cards_front)):
            if i == len(self.cards_front)-1:
                text += str([self.cards_front[i],self.cards_back[i],self.cards_phase[i],self.cards_last_wrong[i],self.all_right[i],self.all_wrong[i]])
            else:
                text += str([self.cards_front[i],self.cards_back[i],self.cards_phase[i],self.cards_last_wrong[i],self.all_right[i],self.all_wrong[i]]) +"\n"

        file_handler.write(text)
        file_handler.close()
        

        if self.data["cards"] not in self.data["recent"]:
            if len(self.data.get("recent")) >= 5:
                del self.data["recent"][0]
            self.data["recent"].append(self.data["cards"])










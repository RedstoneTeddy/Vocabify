import buttons
import pygame
import time
import functions
import random
import easygui
import os
pygame.init()
from copy import deepcopy



class Learn():
    '''
    A class that handles the possibility to learn the cards with an intelligent algorithm
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
        self.cards_last_wrong = [] #Penalty points, up to 6. 2=wrong,3=skipped,-1=right
        self.all_right = [] #In total how many times you got it right
        self.all_wrong = [] #In total how many times you got it wrong

        
        self.auto_save_timer = 0
        self.button_obj = buttons.Button(screen,data)
        self.img_home = pygame.transform.scale(pygame.image.load("images/menu/home.png").convert_alpha(),(32,32))
        self.learn_words = []
        self.learn_words_position = 0
        self.show_result = False
        
        self.other_words = [] #For multiple-choice only
        self.choices = [] #For multiple-choice only
        self.write_side = [] #For write_random only
        self.entered = "" #For write only

        self.current_right = True
        self.current_skipped = False
        self.last_weigths = []
        self.next_clicked = False 
        self.turn_card_click = False


    def Main(self):
        self.screen.fill(self.data.get("settings").get("color1"))
        if self.cards_data == []:
            self.Load()
            self.show_result = False
            self.learn_words = []
            self.learn_words_position = 0
            if self.cards_data == []:
                self.cards_data = [None]



        if self.learn_words == [] or len(self.learn_words) <= self.learn_words_position:
            self.New_words()
            self.learn_words_position = 0


        #Debug Funciton
        if pygame.key.get_pressed()[pygame.K_p] == True:
            if pygame.key.get_pressed()[pygame.K_LCTRL] or pygame.key.get_pressed()[pygame.K_RCTRL]:
                text = ""
                text += "Weights: " + str(self.last_weigths) + "\n\n"
                text += "Learn_words: " + str(self.learn_words) + "\n\n"
                text += "Learn_words_position: " + str(self.learn_words_position) + "\n\n\n"
                text += "-----------------------------------" + "\n\n\n"
                text += "Phases: " + str(self.cards_phase) + "\n\n"
                text += "Cards_last_wrong: " + str(self.cards_last_wrong) + "\n\n"
                text += "All_right: " + str(self.all_right) + "\n\n"
                text += "All_wrong: " + str(self.all_wrong) + "\n\n"
                easygui.textbox("Some important variables & List for debbuging purposes:","Vocabify Debugger",text,True)



        match self.cards_phase[self.learn_words[self.learn_words_position]]:
            case 0:
                self.Cards()
            case 1:
                self.Multiple()
            case 2:
                self.Multiple_reverse()
            case 3:
                self.Write()
            case 4:
                self.Write_reverse()
            case 5:
                if self.write_side[self.learn_words_position] == 0:
                    self.Write()
                else:
                    self.Write_reverse()





        if self.show_result == True:
            if self.button_obj.Button([self.data.get("width")-100,self.data.get("height")-5-50,100,50],4,(0,133,13),self.data.get("settings").get("color2"),["Next"],21) or (pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.KSCAN_RIGHT]) or pygame.key.get_pressed()[pygame.K_RETURN] or pygame.key.get_pressed()[pygame.K_KP_ENTER]:
                if self.next_clicked == False:
                    self.next_clicked = True
                    self.show_result = False
                    self.Next_word(self.learn_words[self.learn_words_position],self.current_right,self.current_skipped)
            else:
                self.next_clicked = False



        if self.button_obj.Button([self.data.get("width")//2-50,self.data.get("height")-5-50,100,50],4,(0,133,13),self.data.get("settings").get("color2"),["Home"],22) or pygame.key.get_pressed()[pygame.K_ESCAPE]:
            self.Save()
            self.data["change_mode"] = "menu"
            self.cards_data = []

        #Auto-Save
        self.auto_save_timer += 1
        if self.auto_save_timer > 60*60: #Every minute, 60frames per second, 60 seconds per minute
            self.auto_save_timer = 0
            self.Save()






    ###########################################
    ###############Learn Options###############
    ###########################################
    def Write_reverse(self):
        if self.show_result == False:
            if self.data.get("key_pressed") != None and self.data.get("key_pressed") != "":
                if self.data.get("key_pressed") == "back":
                    self.entered = self.entered[:-1]
                elif self.data.get("key_pressed") not in ["back","enter","tab","esc"]:
                    self.entered += self.data.get("key_pressed")
            self.button_obj.Button([20,20,self.data.get("width")-40,self.data.get("height")//2-20],5,self.data.get("settings").get("color3"),self.data.get("settings").get("color2"),[self.cards_back[self.learn_words[self.learn_words_position]][0]],25)
            if self.button_obj.Button([20,self.data.get("height")//2,self.data.get("width")-40,self.data.get("height")//2-60],5,self.data.get("settings").get("color3"),self.data.get("settings").get("color2"),[self.entered],25) or pygame.key.get_pressed()[pygame.K_RETURN] or pygame.key.get_pressed()[pygame.K_KP_ENTER]:
                if self.turn_card_click == False:
                    self.show_result = True
                    self.turn_card_click = True
            else:
                self.turn_card_click = False
            functions.draw_text("Your answer:",self.data["fonts"](20,self.data),self.data.get("settings").get("color2"),(self.data.get("width")//2-55,self.data.get("height")//2+15),self.screen)
        else:
            if self.entered in self.cards_front[self.learn_words[self.learn_words_position]]:
                self.button_obj.Button([20,self.data.get("height")//2,self.data.get("width")-40,self.data.get("height")//2-60],5,self.data.get("settings").get("color3"),(50,205,50),[self.entered],25)
                functions.draw_text("Correct!",self.data["fonts"](20,self.data),(50,205,50),(self.data.get("width")//2-35,self.data.get("height")//2+35),self.screen)
                self.current_right = True
                self.current_skipped = False
            else:
                self.button_obj.Button([20,self.data.get("height")//2,self.data.get("width")-40,self.data.get("height")//2-60],5,self.data.get("settings").get("color3"),(255,100,100),[self.entered],25)
                functions.draw_text("Wrong!",self.data["fonts"](20,self.data),(255,100,100),(self.data.get("width")//2-30,self.data.get("height")//2+35),self.screen)
                self.current_right = False
                self.current_skipped = False
                if self.entered in [""," ","\n"]:
                    self.current_skipped = True
            if self.button_obj.Button([20,20,self.data.get("width")-40,self.data.get("height")//2-20],5,self.data.get("settings").get("color3"),self.data.get("settings").get("color2"),[self.cards_back[self.learn_words[self.learn_words_position]][0],"==>",self.cards_front[self.learn_words[self.learn_words_position]][0]],25) or pygame.key.get_pressed()[pygame.K_RETURN] or pygame.key.get_pressed()[pygame.K_KP_ENTER]:
                if self.turn_card_click == False:
                    self.show_result = False
                    self.turn_card_click = True
                    self.entered = ""
                    self.Next_word(self.learn_words[self.learn_words_position],self.current_right,self.current_skipped)
            else:
                self.turn_card_click = False
            functions.draw_text("Your answer:",self.data["fonts"](20,self.data),self.data.get("settings").get("color2"),(self.data.get("width")//2-55,self.data.get("height")//2+15),self.screen)
            
        functions.draw_text(f"{self.learn_words_position}/{len(self.learn_words)}",self.data["fonts"](18,self.data),self.data.get("settings").get("color2"),[25,25],self.screen)    



    def Write(self):
        if self.show_result == False:
            if self.data.get("key_pressed") != None and self.data.get("key_pressed") != "":
                if self.data.get("key_pressed") == "back":
                    self.entered = self.entered[:-1]
                elif self.data.get("key_pressed") not in ["back","enter","tab","esc"]:
                    self.entered += self.data.get("key_pressed")
            self.button_obj.Button([20,20,self.data.get("width")-40,self.data.get("height")//2-20],5,self.data.get("settings").get("color3"),self.data.get("settings").get("color2"),[self.cards_front[self.learn_words[self.learn_words_position]][0]],25)
            if self.button_obj.Button([20,self.data.get("height")//2,self.data.get("width")-40,self.data.get("height")//2-60],5,self.data.get("settings").get("color3"),self.data.get("settings").get("color2"),[self.entered],25) or pygame.key.get_pressed()[pygame.K_RETURN] or pygame.key.get_pressed()[pygame.K_KP_ENTER]:
                if self.turn_card_click == False and self.next_clicked == False:
                    self.show_result = True
                    self.next_clicked = True
                    self.turn_card_click = True
            else:
                self.turn_card_click = False
            functions.draw_text("Your answer:",self.data["fonts"](20,self.data),self.data.get("settings").get("color2"),(self.data.get("width")//2-55,self.data.get("height")//2+15),self.screen)
        else:
            if self.entered in self.cards_back[self.learn_words[self.learn_words_position]]:
                self.button_obj.Button([20,self.data.get("height")//2,self.data.get("width")-40,self.data.get("height")//2-60],5,self.data.get("settings").get("color3"),(50,205,50),[self.entered],25)
                functions.draw_text("Correct!",self.data["fonts"](20,self.data),(50,205,50),(self.data.get("width")//2-35,self.data.get("height")//2+35),self.screen)
                self.current_right = True
                self.current_skipped = False
            else:
                self.button_obj.Button([20,self.data.get("height")//2,self.data.get("width")-40,self.data.get("height")//2-60],5,self.data.get("settings").get("color3"),(255,100,100),[self.entered],25)
                functions.draw_text("Wrong!",self.data["fonts"](20,self.data),(255,100,100),(self.data.get("width")//2-30,self.data.get("height")//2+35),self.screen)
                self.current_right = False
                self.current_skipped = False
                if self.entered in [""," ","\n"]:
                    self.current_skipped = True
            if self.button_obj.Button([20,20,self.data.get("width")-40,self.data.get("height")//2-20],5,self.data.get("settings").get("color3"),self.data.get("settings").get("color2"),[self.cards_front[self.learn_words[self.learn_words_position]][0],"==>",self.cards_back[self.learn_words[self.learn_words_position]][0]],25) or pygame.key.get_pressed()[pygame.K_RETURN] or pygame.key.get_pressed()[pygame.K_KP_ENTER]:
                if self.turn_card_click == False:
                    self.show_result = False
                    self.turn_card_click = True
                    self.entered = ""
                    self.Next_word(self.learn_words[self.learn_words_position],self.current_right,self.current_skipped)
            else:
                self.turn_card_click = False
            functions.draw_text("Your answer:",self.data["fonts"](20,self.data),self.data.get("settings").get("color2"),(self.data.get("width")//2-55,self.data.get("height")//2+15),self.screen)
            
        functions.draw_text(f"{self.learn_words_position}/{len(self.learn_words)}",self.data["fonts"](18,self.data),self.data.get("settings").get("color2"),[25,25],self.screen)    




    def Multiple_reverse(self):
        if self.show_result == False:
            self.selected = -1
            self.button_obj.Button([20,20,self.data.get("width")-40,self.data.get("height")//2-20],5,self.data.get("settings").get("color3"),self.data.get("settings").get("color2"),[self.cards_back[self.learn_words[self.learn_words_position]][0]],25)
            if self.button_obj.Button([20,self.data.get("height")//2,self.data.get("width")//2-20,self.data.get("height")//4-30],5,self.data.get("settings").get("color3"),self.data.get("settings").get("color2"),[self.cards_front[self.choices[self.learn_words_position][0]][0]],20) or pygame.key.get_pressed()[pygame.K_1] or pygame.key.get_pressed()[pygame.K_KP1]:
                self.show_result = True
                self.selected = self.choices[self.learn_words_position][0]
            if self.button_obj.Button([self.data.get("width")//2,self.data.get("height")//2,self.data.get("width")//2-20,self.data.get("height")//4-30],5,self.data.get("settings").get("color3"),self.data.get("settings").get("color2"),[self.cards_front[self.choices[self.learn_words_position][1]][0]],20) or pygame.key.get_pressed()[pygame.K_2] or pygame.key.get_pressed()[pygame.K_KP2]:
                self.show_result = True
                self.selected = self.choices[self.learn_words_position][1]
            if self.button_obj.Button([20,self.data.get("height")//4*3-30,self.data.get("width")//2-20,self.data.get("height")//4-30],5,self.data.get("settings").get("color3"),self.data.get("settings").get("color2"),[self.cards_front[self.choices[self.learn_words_position][2]][0]],20) or pygame.key.get_pressed()[pygame.K_3] or pygame.key.get_pressed()[pygame.K_KP3]:
                self.show_result = True
                self.selected = self.choices[self.learn_words_position][2]
            if self.button_obj.Button([self.data.get("width")//2,self.data.get("height")//4*3-30,self.data.get("width")//2-20,self.data.get("height")//4-30],5,self.data.get("settings").get("color3"),self.data.get("settings").get("color2"),[self.cards_front[self.choices[self.learn_words_position][3]][0]],20) or pygame.key.get_pressed()[pygame.K_4] or pygame.key.get_pressed()[pygame.K_KP4]:
                self.show_result = True
                self.selected = self.choices[self.learn_words_position][3]
        else:
            self.button_obj.Button([20,20,self.data.get("width")-40,self.data.get("height")//2-20],5,self.data.get("settings").get("color3"),self.data.get("settings").get("color2"),[self.cards_back[self.learn_words[self.learn_words_position]][0]],25)
            self.current_skipped = False

            if self.selected == self.choices[self.learn_words_position][0]:
                if self.selected == self.learn_words[self.learn_words_position]:
                    self.current_right = True
                    self.button_obj.Button([20,self.data.get("height")//2,self.data.get("width")//2-20,self.data.get("height")//4-30],5,self.data.get("settings").get("color3"),(50,205,50),[self.cards_front[self.choices[self.learn_words_position][0]][0]],20)
                else:
                    self.current_right = False
                    self.button_obj.Button([20,self.data.get("height")//2,self.data.get("width")//2-20,self.data.get("height")//4-30],5,self.data.get("settings").get("color3"),(255,100,100),[self.cards_front[self.choices[self.learn_words_position][0]][0]],20)
            elif self.choices[self.learn_words_position][0] == self.learn_words[self.learn_words_position]:
                self.button_obj.Button([20,self.data.get("height")//2,self.data.get("width")//2-20,self.data.get("height")//4-30],5,self.data.get("settings").get("color3"),(0,200,0),[self.cards_front[self.choices[self.learn_words_position][0]][0]],20)
            else:
                self.button_obj.Button([20,self.data.get("height")//2,self.data.get("width")//2-20,self.data.get("height")//4-30],5,self.data.get("settings").get("color3"),self.data.get("settings").get("color2"),[self.cards_front[self.choices[self.learn_words_position][0]][0]],20)

            if self.selected == self.choices[self.learn_words_position][1]:
                if self.selected == self.learn_words[self.learn_words_position]:
                    self.current_right = True
                    self.button_obj.Button([self.data.get("width")//2,self.data.get("height")//2,self.data.get("width")//2-20,self.data.get("height")//4-30],5,self.data.get("settings").get("color3"),(50,205,50),[self.cards_front[self.choices[self.learn_words_position][1]][0]],20)
                else:
                    self.current_right = False
                    self.button_obj.Button([self.data.get("width")//2,self.data.get("height")//2,self.data.get("width")//2-20,self.data.get("height")//4-30],5,self.data.get("settings").get("color3"),(255,100,100),[self.cards_front[self.choices[self.learn_words_position][1]][0]],20)
            elif self.choices[self.learn_words_position][1] == self.learn_words[self.learn_words_position]:
                self.button_obj.Button([self.data.get("width")//2,self.data.get("height")//2,self.data.get("width")//2-20,self.data.get("height")//4-30],5,self.data.get("settings").get("color3"),(0,200,0),[self.cards_front[self.choices[self.learn_words_position][1]][0]],20)
            else:
                self.button_obj.Button([self.data.get("width")//2,self.data.get("height")//2,self.data.get("width")//2-20,self.data.get("height")//4-30],5,self.data.get("settings").get("color3"),self.data.get("settings").get("color2"),[self.cards_front[self.choices[self.learn_words_position][1]][0]],20)

            if self.selected == self.choices[self.learn_words_position][2]:
                if self.selected == self.learn_words[self.learn_words_position]:
                    self.current_right = True
                    self.button_obj.Button([20,self.data.get("height")//4*3-30,self.data.get("width")//2-20,self.data.get("height")//4-30],5,self.data.get("settings").get("color3"),(50,205,50),[self.cards_front[self.choices[self.learn_words_position][2]][0]],20)
                else:
                    self.current_right = False
                    self.button_obj.Button([20,self.data.get("height")//4*3-30,self.data.get("width")//2-20,self.data.get("height")//4-30],5,self.data.get("settings").get("color3"),(255,100,100),[self.cards_front[self.choices[self.learn_words_position][2]][0]],20)
            elif self.choices[self.learn_words_position][2] == self.learn_words[self.learn_words_position]:
                self.button_obj.Button([20,self.data.get("height")//4*3-30,self.data.get("width")//2-20,self.data.get("height")//4-30],5,self.data.get("settings").get("color3"),(0,200,0),[self.cards_front[self.choices[self.learn_words_position][2]][0]],20)
            else:
                self.button_obj.Button([20,self.data.get("height")//4*3-30,self.data.get("width")//2-20,self.data.get("height")//4-30],5,self.data.get("settings").get("color3"),self.data.get("settings").get("color2"),[self.cards_front[self.choices[self.learn_words_position][2]][0]],20)

            if self.selected == self.choices[self.learn_words_position][3]:
                if self.selected == self.learn_words[self.learn_words_position]:
                    self.current_right = True
                    self.button_obj.Button([self.data.get("width")//2,self.data.get("height")//4*3-30,self.data.get("width")//2-20,self.data.get("height")//4-30],5,self.data.get("settings").get("color3"),(50,205,50),[self.cards_front[self.choices[self.learn_words_position][3]][0]],20)
                else:
                    self.current_right = False
                    self.button_obj.Button([self.data.get("width")//2,self.data.get("height")//4*3-30,self.data.get("width")//2-20,self.data.get("height")//4-30],5,self.data.get("settings").get("color3"),(255,100,100),[self.cards_front[self.choices[self.learn_words_position][3]][0]],20)
            elif self.choices[self.learn_words_position][3] == self.learn_words[self.learn_words_position]:
                    self.button_obj.Button([self.data.get("width")//2,self.data.get("height")//4*3-30,self.data.get("width")//2-20,self.data.get("height")//4-30],5,self.data.get("settings").get("color3"),(0,200,0),[self.cards_front[self.choices[self.learn_words_position][3]][0]],20)
            else:
                self.button_obj.Button([self.data.get("width")//2,self.data.get("height")//4*3-30,self.data.get("width")//2-20,self.data.get("height")//4-30],5,self.data.get("settings").get("color3"),self.data.get("settings").get("color2"),[self.cards_front[self.choices[self.learn_words_position][3]][0]],20)

        functions.draw_text(f"{self.learn_words_position}/{len(self.learn_words)}",self.data["fonts"](18,self.data),self.data.get("settings").get("color2"),[25,25],self.screen)    



    def Multiple(self):
        if self.show_result == False:
            self.selected = -1
            self.button_obj.Button([20,20,self.data.get("width")-40,self.data.get("height")//2-20],5,self.data.get("settings").get("color3"),self.data.get("settings").get("color2"),[self.cards_front[self.learn_words[self.learn_words_position]][0]],25)
            if self.button_obj.Button([20,self.data.get("height")//2,self.data.get("width")//2-20,self.data.get("height")//4-30],5,self.data.get("settings").get("color3"),self.data.get("settings").get("color2"),[self.cards_back[self.choices[self.learn_words_position][0]][0]],20) or pygame.key.get_pressed()[pygame.K_1] or pygame.key.get_pressed()[pygame.K_KP1]:
                self.show_result = True
                self.selected = self.choices[self.learn_words_position][0]
            if self.button_obj.Button([self.data.get("width")//2,self.data.get("height")//2,self.data.get("width")//2-20,self.data.get("height")//4-30],5,self.data.get("settings").get("color3"),self.data.get("settings").get("color2"),[self.cards_back[self.choices[self.learn_words_position][1]][0]],20) or pygame.key.get_pressed()[pygame.K_2] or pygame.key.get_pressed()[pygame.K_KP2]:
                self.show_result = True
                self.selected = self.choices[self.learn_words_position][1]
            if self.button_obj.Button([20,self.data.get("height")//4*3-30,self.data.get("width")//2-20,self.data.get("height")//4-30],5,self.data.get("settings").get("color3"),self.data.get("settings").get("color2"),[self.cards_back[self.choices[self.learn_words_position][2]][0]],20) or pygame.key.get_pressed()[pygame.K_3] or pygame.key.get_pressed()[pygame.K_KP3]:
                self.show_result = True
                self.selected = self.choices[self.learn_words_position][2]
            if self.button_obj.Button([self.data.get("width")//2,self.data.get("height")//4*3-30,self.data.get("width")//2-20,self.data.get("height")//4-30],5,self.data.get("settings").get("color3"),self.data.get("settings").get("color2"),[self.cards_back[self.choices[self.learn_words_position][3]][0]],20) or pygame.key.get_pressed()[pygame.K_4] or pygame.key.get_pressed()[pygame.K_KP4]:
                self.show_result = True
                self.selected = self.choices[self.learn_words_position][3]
        else:
            self.button_obj.Button([20,20,self.data.get("width")-40,self.data.get("height")//2-20],5,self.data.get("settings").get("color3"),self.data.get("settings").get("color2"),[self.cards_front[self.learn_words[self.learn_words_position]][0]],25)
            
            if self.selected == self.choices[self.learn_words_position][0]:
                if self.selected == self.learn_words[self.learn_words_position]:
                    self.current_right = True
                    self.button_obj.Button([20,self.data.get("height")//2,self.data.get("width")//2-20,self.data.get("height")//4-30],5,self.data.get("settings").get("color3"),(50,205,50),[self.cards_back[self.choices[self.learn_words_position][0]][0]],20)
                else:
                    self.current_right = False
                    self.button_obj.Button([20,self.data.get("height")//2,self.data.get("width")//2-20,self.data.get("height")//4-30],5,self.data.get("settings").get("color3"),(255,100,100),[self.cards_back[self.choices[self.learn_words_position][0]][0]],20)
            elif self.choices[self.learn_words_position][0] == self.learn_words[self.learn_words_position]:
                self.button_obj.Button([20,self.data.get("height")//2,self.data.get("width")//2-20,self.data.get("height")//4-30],5,self.data.get("settings").get("color3"),(0,200,0),[self.cards_back[self.choices[self.learn_words_position][0]][0]],20)
            else:
                self.button_obj.Button([20,self.data.get("height")//2,self.data.get("width")//2-20,self.data.get("height")//4-30],5,self.data.get("settings").get("color3"),self.data.get("settings").get("color2"),[self.cards_back[self.choices[self.learn_words_position][0]][0]],20)

            if self.selected == self.choices[self.learn_words_position][1]:
                if self.selected == self.learn_words[self.learn_words_position]:
                    self.current_right = True
                    self.button_obj.Button([self.data.get("width")//2,self.data.get("height")//2,self.data.get("width")//2-20,self.data.get("height")//4-30],5,self.data.get("settings").get("color3"),(50,205,50),[self.cards_back[self.choices[self.learn_words_position][1]][0]],20)
                else:
                    self.current_right = False
                    self.button_obj.Button([self.data.get("width")//2,self.data.get("height")//2,self.data.get("width")//2-20,self.data.get("height")//4-30],5,self.data.get("settings").get("color3"),(255,100,100),[self.cards_back[self.choices[self.learn_words_position][1]][0]],20)
            elif self.choices[self.learn_words_position][1] == self.learn_words[self.learn_words_position]:
                self.button_obj.Button([self.data.get("width")//2,self.data.get("height")//2,self.data.get("width")//2-20,self.data.get("height")//4-30],5,self.data.get("settings").get("color3"),(0,200,0),[self.cards_back[self.choices[self.learn_words_position][1]][0]],20)
            else:
                self.button_obj.Button([self.data.get("width")//2,self.data.get("height")//2,self.data.get("width")//2-20,self.data.get("height")//4-30],5,self.data.get("settings").get("color3"),self.data.get("settings").get("color2"),[self.cards_back[self.choices[self.learn_words_position][1]][0]],20)

            if self.selected == self.choices[self.learn_words_position][2]:
                if self.selected == self.learn_words[self.learn_words_position]:
                    self.current_right = True
                    self.button_obj.Button([20,self.data.get("height")//4*3-30,self.data.get("width")//2-20,self.data.get("height")//4-30],5,self.data.get("settings").get("color3"),(50,205,50),[self.cards_back[self.choices[self.learn_words_position][2]][0]],20)
                else:
                    self.current_right = False
                    self.button_obj.Button([20,self.data.get("height")//4*3-30,self.data.get("width")//2-20,self.data.get("height")//4-30],5,self.data.get("settings").get("color3"),(255,100,100),[self.cards_back[self.choices[self.learn_words_position][2]][0]],20)
            elif self.choices[self.learn_words_position][2] == self.learn_words[self.learn_words_position]:
                self.button_obj.Button([20,self.data.get("height")//4*3-30,self.data.get("width")//2-20,self.data.get("height")//4-30],5,self.data.get("settings").get("color3"),(0,200,0),[self.cards_back[self.choices[self.learn_words_position][2]][0]],20)
            else:
                self.button_obj.Button([20,self.data.get("height")//4*3-30,self.data.get("width")//2-20,self.data.get("height")//4-30],5,self.data.get("settings").get("color3"),self.data.get("settings").get("color2"),[self.cards_back[self.choices[self.learn_words_position][2]][0]],20)

            if self.selected == self.choices[self.learn_words_position][3]:
                if self.selected == self.learn_words[self.learn_words_position]:
                    self.current_right = True
                    self.button_obj.Button([self.data.get("width")//2,self.data.get("height")//4*3-30,self.data.get("width")//2-20,self.data.get("height")//4-30],5,self.data.get("settings").get("color3"),(50,205,50),[self.cards_back[self.choices[self.learn_words_position][3]][0]],20)
                else:
                    self.current_right = False
                    self.button_obj.Button([self.data.get("width")//2,self.data.get("height")//4*3-30,self.data.get("width")//2-20,self.data.get("height")//4-30],5,self.data.get("settings").get("color3"),(255,100,100),[self.cards_back[self.choices[self.learn_words_position][3]][0]],20)
            elif self.choices[self.learn_words_position][3] == self.learn_words[self.learn_words_position]:
                    self.button_obj.Button([self.data.get("width")//2,self.data.get("height")//4*3-30,self.data.get("width")//2-20,self.data.get("height")//4-30],5,self.data.get("settings").get("color3"),(0,200,0),[self.cards_back[self.choices[self.learn_words_position][3]][0]],20)
            else:
                self.button_obj.Button([self.data.get("width")//2,self.data.get("height")//4*3-30,self.data.get("width")//2-20,self.data.get("height")//4-30],5,self.data.get("settings").get("color3"),self.data.get("settings").get("color2"),[self.cards_back[self.choices[self.learn_words_position][3]][0]],20)

        functions.draw_text(f"{self.learn_words_position}/{len(self.learn_words)}",self.data["fonts"](18,self.data),self.data.get("settings").get("color2"),[25,25],self.screen)    



    def Cards(self):
        if self.show_result == False:
            if self.button_obj.Button([20,20,self.data.get("width")-40,self.data.get("height")-40-50],5,self.data.get("settings").get("color3"),self.data.get("settings").get("color2"),[self.cards_front[self.learn_words[self.learn_words_position]][0]],25) or (pygame.key.get_pressed()[pygame.K_SPACE]):
                if self.turn_card_click == False:
                    self.show_result = True
                    self.turn_card_click = True
                    self.current_right = True
                    self.current_skipped = False
            else:
                self.turn_card_click = False
        else:
            if self.button_obj.Button([20,20,self.data.get("width")-40,self.data.get("height")-40-50],5,self.data.get("settings").get("color3"),self.data.get("settings").get("color2"),[self.cards_back[self.learn_words[self.learn_words_position]][0]],25) or (pygame.key.get_pressed()[pygame.K_SPACE]):
               if self.turn_card_click == False:
                    self.show_result = False
                    self.turn_card_click = True
            else:
                self.turn_card_click = False
            functions.draw_text("Back",self.data["fonts"](18,self.data),self.data.get("settings").get("color2"),[25,self.data.get("height")-20-70],self.screen)
        functions.draw_text(f"{self.learn_words_position}/{len(self.learn_words)}",self.data["fonts"](18,self.data),self.data.get("settings").get("color2"),[25,25],self.screen)    









    
    def Next_word(self,i,right=True,skipped=False):
        self.show_result = False
        self.learn_words_position += 1
        self.entered = ""

        if right == True:
            self.all_right[i] += 1
            if self.cards_last_wrong[i] > 0:
                self.cards_last_wrong[i] -= 1
            if self.cards_phase[i] < 4:
                self.cards_phase[i] += 1
        else:
            self.all_wrong[i] += 1
            self.cards_last_wrong[i] += 2

        if skipped == True:
            self.cards_last_wrong[i] += 1

        if self.cards_last_wrong[i] >= 6:
            self.cards_last_wrong[i] -= 6
            if self.cards_phase[i] >= 1:
                self.cards_phase[i] -= 1

        



    def New_words(self):
        start_time = time.time_ns()
        self.other_words = []
        self.choices = []
        self.write_side = []

        self.learn_words = []
        self.learn_words_position = 0

        highest_phase = max(self.cards_phase)
        ratio = []
        for i in range(0,len(self.cards_front)):
            if self.all_right[i] == 0:
                if self.all_wrong[i] == 0:
                    ratio.append(1)
                else:
                    ratio.append(10)
            else:
                ratio.append(round(self.all_wrong[i]/self.all_right[i],2))
        highest_ratio = max(ratio)
        highest_all_right = max(self.all_right)

        weights = []
        for i in range(0,len(self.cards_front)):
            #Base
            weights.append(10)
            #Boost lower phases
            weights[i] *= 3**(highest_phase-self.cards_phase[i])
            #Boost higher wrong-ratios
            if ratio[i] == highest_ratio:
                weights[i] *= 1.5
            elif ratio[i] > 1:
                weights[i] *= 1.2
            elif ratio[i] > 0.3:
                weights[i] *= 1
            else:
                weights[i] *= 0.8
            #Boost last wrong cards
            if self.cards_last_wrong[i] == 0:
                weights[i] -= 4
            elif self.cards_last_wrong[i] <= 3:
                weights[i] += 5
            else:
                weights[i] += 7
            #Boost cards with less right
            if self.all_right[i] < highest_all_right*0.75:
                weights[i] += 1
            if self.all_right[i] < highest_all_right*0.5:
                weights[i] += 2
            if self.all_right[i] < highest_all_right*0.25:
                weights[i] += 3
        
        self.last_weigths = deepcopy(weights)

        for _ in range(0,10): #Get 10 random cards
            random_chance_range = []
            random_chance_counter = 0
            for chance in weights:
                if chance != 0:
                    random_chance_range.append([random_chance_counter,random_chance_counter+chance-1])
                    random_chance_counter += chance
                else:
                    random_chance_range.append([-1,-1])
            random_number = random.randrange(0,random_chance_counter)

            for i in range(len(random_chance_range)):
                if random_number >= random_chance_range[i][0] and random_number <= random_chance_range[i][1]:
                    self.learn_words.append(i)
                    weights[i] = 0
        
        #Setup all words
        for i in range(0,10):
            self.other_words.append([])
            self.choices.append([])
            run = True
            while run:
                other = random.randrange(0,len(self.cards_front))
                if other != self.learn_words[i]:
                    self.other_words[-1].append(other)
                if len(self.other_words[-1]) >= 3:
                    run = False
            self.choices[-1].append(self.learn_words[i])
            self.choices[-1].extend(self.other_words[-1])
            random.shuffle(self.choices[-1])
            self.write_side.append(random.randint(0,1))
        end_time = time.time_ns()
        self.data["last_learn_generation_ms"] = round((end_time-start_time)/1000,1)


        




        
    def Load(self) -> None:
        '''
        Loads the current card-set and writes it into the recent-cards list
        '''
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


        if self.data["cards"] not in self.data["recent"]:
            if len(self.data.get("recent")) >= 5:
                del self.data["recent"][0]
            self.data["recent"].append(self.data["cards"])
        
        if len(self.cards_front) < 10:
            self.Save()
            self.data["change_mode"] = "menu"
            self.cards_data = []
            easygui.msgbox("You need at least 10 words\nfor this mode to function correctly!\nTry the 'Custom Learn' instead","Vocabify")
            

        functions.Save_settings(self.data)


    def Save(self):
        '''
        Saves the current card-set and writes it into the recent-cards list
        '''
        file_handler = open("cards/"+self.data.get("cards"),"w")
        print(len(self.cards_front))
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




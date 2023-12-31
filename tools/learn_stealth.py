import buttons
import pygame
import functions
import random
import easygui
import os
pygame.init()
from copy import deepcopy



class Learn():
    '''
    A class that handles the possibility to learn the cards by a writing them in a stealth mode
    '''
    def __init__(self, data:dict,screen:object) -> object:
        '''
        Initializes the Learn_stealth object.

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
        self.turn_card_click = False
        self.next_clicked = False
        self.previous_clicked = False
        self.entered = ""


    def Main(self):
        self.screen.fill((0,0,0))
        if self.cards_data == []:
            self.Load()
            self.learn_words = []
            self.show_result = False
            self.learn_words_position = 0
            if self.cards_data == []:
                self.cards_data = [None]

        if self.learn_words == [] or len(self.learn_words) <= self.learn_words_position:
            if len(self.learn_words)-1 <= self.learn_words_position and self.learn_words != []:
                easygui.msgbox("Perfect!\nYou mastered all cards.\nThe cards will be reshuffled.","Vocabify")
            self.New_words()

        if pygame.key.get_pressed()[pygame.K_LALT] == True:
            show_text = True
        else:
            show_text = False
        
        if self.data.get("key_pressed") != None and self.data.get("key_pressed") != "":
            if self.data.get("key_pressed") == "back":
                self.entered = self.entered[:-1]
            elif self.data.get("key_pressed") not in ["back","enter","tab","esc"]:
                self.entered += self.data.get("key_pressed")
        if self.show_result == False:
            if show_text == True:
                functions.draw_text(self.cards_front[self.learn_words[self.learn_words_position]][0],self.data["fonts"](14,self.data),(255,255,255),(20,10),self.screen)
                functions.draw_text(self.entered,self.data["fonts"](14,self.data),(255,255,255),(20,40),self.screen)
                if self.button_obj.Button([20,self.data.get("height")//2,self.data.get("width")-40,self.data.get("height")//2-60],5,(0,0,0),(255,255,255),[""],25,no_outline=True):
                    if self.turn_card_click == False:
                        self.show_result = True
                        self.turn_card_click = True
                else:
                    self.turn_card_click = False
            else:
                if pygame.key.get_pressed()[pygame.K_RETURN] or pygame.key.get_pressed()[pygame.K_KP_ENTER]:
                    if self.turn_card_click == False:
                        self.show_result = True
                        self.turn_card_click = True
                else:
                    self.turn_card_click = False
        else:
            if self.entered in self.cards_back[self.learn_words[self.learn_words_position]]:
                pygame.draw.rect(self.screen,(255,255,255),(10,10,5,5))
            else:
                pygame.draw.rect(self.screen,(255,255,255),(self.data.get("width")-15,10,5,5))
            if show_text == True:
                
                functions.draw_text(self.cards_front[self.learn_words[self.learn_words_position]][0],self.data["fonts"](14,self.data),(255,255,255),(20,10),self.screen)
                functions.draw_text(self.cards_back[self.learn_words[self.learn_words_position]][0],self.data["fonts"](14,self.data),(255,255,255),(20,25),self.screen)
                functions.draw_text(self.entered,self.data["fonts"](14,self.data),(255,255,255),(20,40),self.screen)

                if self.button_obj.Button([20,55,self.data.get("width")-40,self.data.get("height")//2-20],5,(0,0,0),(255,255,255),[""],25,no_outline=True):
                    if self.turn_card_click == False:
                        self.show_result = False
                        self.learn_words_position += 1
                        self.turn_card_click = True
                        self.entered = ""
                else:
                    self.turn_card_click = False
            else:
                if pygame.key.get_pressed()[pygame.K_RETURN] or pygame.key.get_pressed()[pygame.K_KP_ENTER]:
                    if self.turn_card_click == False:
                        self.show_result = False
                        self.learn_words_position += 1
                        self.turn_card_click = True
                        self.entered = ""
                else:
                    self.turn_card_click = False

        if self.button_obj.Button([self.data.get("width")-100,self.data.get("height")-5-50,100,50],4,(0,0,0),(0,0,0),["Next"],21) or (pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.KSCAN_RIGHT]):
            if self.next_clicked == False:
                self.next_clicked = True
                self.learn_words_position += 1
                self.show_result = False
                self.entered = ""
        else:
            self.next_clicked = False





        #Auto-Save
        self.auto_save_timer += 1
        if self.auto_save_timer > 60*60: #Every minute, 60frames per second, 60 seconds per minute
            self.auto_save_timer = 0
            self.Save()





    def New_words(self):
        self.learn_words_position = 0
        self.learn_words = list(range(len(self.cards_front)))
        random.shuffle(self.learn_words)

        
        
    def Load(self) -> None:
        '''
        Loads the current card-set and writes it into the recent-cards list
        '''
        file_handler = open("cards/"+self.data.get("cards"),"r")
        self.cards_data = []
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




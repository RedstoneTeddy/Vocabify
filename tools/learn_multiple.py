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
    A class that handles the possibility to learn the cards by multiple choice
    '''
    def __init__(self, data:dict,screen:object) -> object:
        '''
        Initializes the Learn_multiple object.

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
        self.other_words = []
        self.choices = []
        self.learn_words_position = 0
        self.show_result = False
        self.selected = -1


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
            if len(self.learn_words)-1 <= self.learn_words_position and self.learn_words != []:
                easygui.msgbox("Perfect!\nYou mastered all cards.\nThe cards will be reshuffled.","Vocabify")
            self.New_words()


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
                    self.button_obj.Button([20,self.data.get("height")//2,self.data.get("width")//2-20,self.data.get("height")//4-30],5,self.data.get("settings").get("color3"),(50,205,50),[self.cards_back[self.choices[self.learn_words_position][0]][0]],20)
                else:
                    self.button_obj.Button([20,self.data.get("height")//2,self.data.get("width")//2-20,self.data.get("height")//4-30],5,self.data.get("settings").get("color3"),(255,100,100),[self.cards_back[self.choices[self.learn_words_position][0]][0]],20)
            elif self.choices[self.learn_words_position][0] == self.learn_words[self.learn_words_position]:
                self.button_obj.Button([20,self.data.get("height")//2,self.data.get("width")//2-20,self.data.get("height")//4-30],5,self.data.get("settings").get("color3"),(0,200,0),[self.cards_back[self.choices[self.learn_words_position][0]][0]],20)
            else:
                self.button_obj.Button([20,self.data.get("height")//2,self.data.get("width")//2-20,self.data.get("height")//4-30],5,self.data.get("settings").get("color3"),self.data.get("settings").get("color2"),[self.cards_back[self.choices[self.learn_words_position][0]][0]],20)

            if self.selected == self.choices[self.learn_words_position][1]:
                if self.selected == self.learn_words[self.learn_words_position]:
                    self.button_obj.Button([self.data.get("width")//2,self.data.get("height")//2,self.data.get("width")//2-20,self.data.get("height")//4-30],5,self.data.get("settings").get("color3"),(50,205,50),[self.cards_back[self.choices[self.learn_words_position][1]][0]],20)
                else:
                    self.button_obj.Button([self.data.get("width")//2,self.data.get("height")//2,self.data.get("width")//2-20,self.data.get("height")//4-30],5,self.data.get("settings").get("color3"),(255,100,100),[self.cards_back[self.choices[self.learn_words_position][1]][0]],20)
            elif self.choices[self.learn_words_position][1] == self.learn_words[self.learn_words_position]:
                self.button_obj.Button([self.data.get("width")//2,self.data.get("height")//2,self.data.get("width")//2-20,self.data.get("height")//4-30],5,self.data.get("settings").get("color3"),(0,200,0),[self.cards_back[self.choices[self.learn_words_position][1]][0]],20)
            else:
                self.button_obj.Button([self.data.get("width")//2,self.data.get("height")//2,self.data.get("width")//2-20,self.data.get("height")//4-30],5,self.data.get("settings").get("color3"),self.data.get("settings").get("color2"),[self.cards_back[self.choices[self.learn_words_position][1]][0]],20)

            if self.selected == self.choices[self.learn_words_position][2]:
                if self.selected == self.learn_words[self.learn_words_position]:
                    self.button_obj.Button([20,self.data.get("height")//4*3-30,self.data.get("width")//2-20,self.data.get("height")//4-30],5,self.data.get("settings").get("color3"),(50,205,50),[self.cards_back[self.choices[self.learn_words_position][2]][0]],20)
                else:
                    self.button_obj.Button([20,self.data.get("height")//4*3-30,self.data.get("width")//2-20,self.data.get("height")//4-30],5,self.data.get("settings").get("color3"),(255,100,100),[self.cards_back[self.choices[self.learn_words_position][2]][0]],20)
            elif self.choices[self.learn_words_position][2] == self.learn_words[self.learn_words_position]:
                self.button_obj.Button([20,self.data.get("height")//4*3-30,self.data.get("width")//2-20,self.data.get("height")//4-30],5,self.data.get("settings").get("color3"),(0,200,0),[self.cards_back[self.choices[self.learn_words_position][2]][0]],20)
            else:
                self.button_obj.Button([20,self.data.get("height")//4*3-30,self.data.get("width")//2-20,self.data.get("height")//4-30],5,self.data.get("settings").get("color3"),self.data.get("settings").get("color2"),[self.cards_back[self.choices[self.learn_words_position][2]][0]],20)

            if self.selected == self.choices[self.learn_words_position][3]:
                if self.selected == self.learn_words[self.learn_words_position]:
                    self.button_obj.Button([self.data.get("width")//2,self.data.get("height")//4*3-30,self.data.get("width")//2-20,self.data.get("height")//4-30],5,self.data.get("settings").get("color3"),(50,205,50),[self.cards_back[self.choices[self.learn_words_position][3]][0]],20)
                else:
                    self.button_obj.Button([self.data.get("width")//2,self.data.get("height")//4*3-30,self.data.get("width")//2-20,self.data.get("height")//4-30],5,self.data.get("settings").get("color3"),(255,100,100),[self.cards_back[self.choices[self.learn_words_position][3]][0]],20)
            elif self.choices[self.learn_words_position][3] == self.learn_words[self.learn_words_position]:
                    self.button_obj.Button([self.data.get("width")//2,self.data.get("height")//4*3-30,self.data.get("width")//2-20,self.data.get("height")//4-30],5,self.data.get("settings").get("color3"),(0,200,0),[self.cards_back[self.choices[self.learn_words_position][3]][0]],20)
            else:
                self.button_obj.Button([self.data.get("width")//2,self.data.get("height")//4*3-30,self.data.get("width")//2-20,self.data.get("height")//4-30],5,self.data.get("settings").get("color3"),self.data.get("settings").get("color2"),[self.cards_back[self.choices[self.learn_words_position][3]][0]],20)

                 

        functions.draw_text(f"{self.learn_words_position}/{len(self.learn_words)}",self.data["fonts"](18,self.data),self.data.get("settings").get("color2"),[25,25],self.screen)    
        if self.learn_words_position >= 1:
            if self.button_obj.Button([0,self.data.get("height")-5-50,100,50],4,(0,133,13),self.data.get("settings").get("color2"),["Previous"],21) or (pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.KSCAN_LEFT]):
                if self.previous_clicked == False:
                    self.previous_clicked = True
                    self.learn_words_position -= 1
                    self.show_result = False
            else:
                self.previous_clicked = False
        if self.button_obj.Button([self.data.get("width")-100,self.data.get("height")-5-50,100,50],4,(0,133,13),self.data.get("settings").get("color2"),["Next"],21) or (pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.KSCAN_RIGHT] or pygame.key.get_pressed()[pygame.K_RETURN] or pygame.key.get_pressed()[pygame.K_KP_ENTER]):
            if self.next_clicked == False:
                self.next_clicked = True
                self.learn_words_position += 1
                self.show_result = False
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





    def New_words(self):
        self.other_words = []
        self.choices = []
        self.learn_words_position = 0
        self.learn_words = list(range(len(self.cards_front)))
        random.shuffle(self.learn_words)
        for word in self.learn_words:
            self.other_words.append([])
            self.choices.append([])
            run = True
            while run:
                other = random.randrange(0,len(self.learn_words))
                if other != word:
                    self.other_words[-1].append(other)
                if len(self.other_words[-1]) >= 3:
                    run = False
            self.choices[-1].append(word)
            self.choices[-1].extend(self.other_words[-1])
            random.shuffle(self.choices[-1])


        
        
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




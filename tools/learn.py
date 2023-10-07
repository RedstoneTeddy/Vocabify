import buttons
import pygame
import functions
import easygui
import os
pygame.init()
from copy import deepcopy



class Learn():
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
        self.cards_last_wrong = [] #Penalty points, up to 6. 2=wrong,3=skipped,-1=right
        self.all_right = [] #In total how many times you got it right
        self.all_wrong = [] #In total how many times you got it wrong

        
        self.auto_save_timer = 0
        self.button_obj = buttons.Button(screen,data)
        self.img_home = pygame.transform.scale(pygame.image.load("images/menu/home.png").convert_alpha(),(32,32))
        self.learn_words = []
        self.learn_words_position = 0


    def Main(self):
        self.screen.fill(self.data.get("settings").get("color1"))
        if self.cards_data == []:
            self.Load()
            self.learn_words = []
            self.learn_words_position = 0
            if self.cards_data == []:
                self.cards_data = [None]



        if self.learn_words == [] or len(self.learn_words)-1 >= self.learn_words_position:
            self.New_words()








        if self.button_obj.Button([10,10,70,70],3,self.data.get("settings").get("color3"),self.data.get("settings").get("color2"),["Home"],20,self.img_home):
            self.Save()
            self.data["change_mode"] = "menu"
            self.cards_data = []

        #Auto-Save
        self.auto_save_timer += 1
        if self.auto_save_timer > 60*60: #Every minute, 60frames per second, 60 seconds per minute
            self.auto_save_timer = 0
            self.Save()





    def New_words(self):
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
            if ratio == highest_ratio:
                weights[i] *= 2
            elif ratio[i] > 1:
                weights[i] *= 1.5
            elif ratio[i] > 0.3:
                weights[i] *= 1
            else:
                weights[i] *= 0.8
            #Boost last wrong cards
            if self.cards_last_wrong[i] == 0:
                weights[i] -= 2
            elif self.cards_last_wrong[i] <= 3:
                weights[i] += 2
            else:
                weights[i] += 5
            #Boost cards with less right
            if self.all_right[i] < highest_all_right*0.75:
                weights[i] += 2
            if self.all_right[i] < highest_all_right*0.5:
                weights[i] += 3
            if self.all_right[i] < highest_all_right*0.25:
                weights[i] += 5
        
        for _ in range(0,10): #Get 10 random cards
            pass


        
    def Load(self) -> None:
        '''
        Loads the current card-set and writes it into the recent-cards list
        '''
        file_handler = open("cards/"+self.data.get("cards"),"r")
        self.cards_data = []
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
            text += str([self.cards_front[i],self.cards_back[i],self.cards_phase[i],self.cards_last_wrong[i],self.all_right[i],self.all_wrong[i]]) +"\n"

        file_handler.write(text)
        file_handler.close()
        

        if self.data["cards"] not in self.data["recent"]:
            if len(self.data.get("recent")) >= 5:
                del self.data["recent"][0]
            self.data["recent"].append(self.data["cards"])




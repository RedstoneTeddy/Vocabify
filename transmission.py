
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



class Transmission():
    '''
    Automatically makes a black transmission between two different modes.
    '''
    def __init__(self,data,screen):
        self.data = data
        self.screen = screen
        self.animation_timer = 0

    def Main(self):
        if self.data.get("change_mode") != None:
            if self.animation_timer == 0:
                self.animation_timer = 90

        if self.animation_timer > 0:
            rect = (
                *Calculated_moving_pos([0,-self.data.get("height")*2],[0,self.data.get("height")],90,(90-self.animation_timer)),
                self.data.get("width"),
                self.data.get("height")*2
            )
            pygame.draw.rect(self.screen,(0,0,0),rect)
            self.animation_timer -= 1
        if self.animation_timer == 45:
            self.data["mode"] = self.data.get("change_mode")
            self.data["change_mode"] = None











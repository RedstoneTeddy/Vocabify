import pygame
pygame.init()

def in_range_1d(pos,size):
    if pos >= size[0] and pos <= size[1]:
        return True
    else:
        return False
    
def in_range_2d(pos,rect):
    if in_range_1d(pos[0],[rect[0],rect[2]+rect[0]]) and in_range_1d(pos[1],[rect[1],rect[3]+rect[1]]):
        return True
    else:
        return False


def Draw_text(text,font,text_color,x,y,screen):
    img = font.render(text,True,text_color)
    screen.blit(img, (x,y))
    
def Center_draw_text(text,font,text_color,pos,size,screen):
    img = font.render(text,True,text_color)
    size_img = img.get_size()
    x = ((pos[0]+size[0]/2)-size_img[0]/2)
    y = ((pos[1]+size[1]/2)-size_img[1]/2)
    screen.blit(img, (x,y))


class Button():
    '''
    Main button class
    '''
    def __init__(self,screen:object,data:dict) -> object:
        '''
        Initializes the button object, with which you can create many buttons.

        Parameters:
        screen --> The screen object
        data --> The main data dictionary

        Returns:
        Button object
        '''
        self.screen = screen
        self.clicked = False
        self.data = data

    def Button(self,rect:list,round_corner:int,background_color:list,line_color:list,text:list[str],font_size:int,img:pygame.image=None,middle_text=True,no_outline=False) -> None:
        '''
        Displays a button

        Parameters:
        rect -> A list [pos_x,pos_y,size_x,size_y]
        round_corner -> An integer how much the corners should be rounded
        background_color -> The background color
        line_color -> The line color
        text -> What text should be displayed. Every element in the list is a line.
        font_size -> How big the font should be
        img -> An optional image to display before the text, needs to already be a pygame.image object
        middle_text -> Default: True. If False, the text won't be middled.
        no_outline -> Default: False. If True, no outline on the box will be rendered

        Returns:
        A boolean, if the button got clicked
        '''
        output = None
        pygame.draw.rect(self.screen,background_color,rect,0,round_corner)
        if no_outline == False:
            pygame.draw.rect(self.screen,line_color,rect,2,round_corner)

        if img != None:
            img_size = img.get_size()
            img_pos = (
                (rect[2]-img_size[0])//2+rect[0],
                (rect[3]-(img_size[1]+len(text)*(font_size+2)+10))//2+rect[1]
            )
            self.screen.blit(img,img_pos)

        if img != None:
            i = -1
        else:
            i = -1-len(text)/2
        for text_line in text:
            i += 1
            if img != None:
                if middle_text == True:
                    Center_draw_text(str(text_line),self.data["fonts"](font_size,self.data),line_color,(rect[0],((rect[3]-(img_size[1]+len(text)*(font_size+2)+10))//2+rect[1])+img_size[1]+10+i*(font_size+2)),(rect[2],font_size+2),self.screen)
                else:
                    Draw_text(str(text_line),self.data["fonts"](font_size,self.data),line_color,rect[0]+4,((rect[3]-(img_size[1]+len(text)*(font_size+2)+10))//2+rect[1])+img_size[1]+10+i*(font_size+2),self.screen)
            else:
                if middle_text == True:
                    Center_draw_text(str(text_line),self.data["fonts"](font_size,self.data),line_color,(rect[0],rect[1]+rect[3]//2+i*(font_size+2)),(rect[2],font_size+2),self.screen)
                else:
                    Draw_text(str(text_line),self.data["fonts"](font_size,self.data),line_color,rect[0]+4,rect[1]+rect[3]//2+i*(font_size+2),self.screen)

        if pygame.mouse.get_pressed()[0] == True:
            if self.clicked == False:
                if in_range_2d(pygame.mouse.get_pos(),rect) == True:
                    self.clicked = True
                    output = True
        else:
            self.clicked = False
        
        return output
    






















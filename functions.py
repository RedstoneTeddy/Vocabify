import pygame
pygame.init()

def draw_text(text,font,text_color,pos,screen):
    img = font.render(text,True,text_color)
    screen.blit(img, pos)



def calc_avg_mspf(data):
    while len(data.get("avg_mspf_calc")) >= 60*5:
        del data["avg_mspf_calc"][0]
    data["avg_mspf_calc"].append(data.get("mspf"))
    data["long_avg_mspf"] = round(sum(data["avg_mspf_calc"])/len(data.get("avg_mspf_calc")),1)
    
    short_sum = 0
    for mspf_calc_counter in range(int(len(data.get("avg_mspf_calc"))/5*4),len(data.get("avg_mspf_calc"))):
        short_sum += data["avg_mspf_calc"][mspf_calc_counter]
    data["avg_mspf"] = round(short_sum/(len(data.get("avg_mspf_calc"))/5),1)


def Font(size,data):
    data = data["font_data"]
    needed_size = str(int(round(size*data.get("slide_zoom"),0)))
    if data.get(needed_size) == None:
        data[needed_size] = pygame.font.Font('images/calibri.TTF',int(needed_size))
    return data.get(needed_size)

def init_data():
    font12 = pygame.font.Font('images/calibri.TTF',12)
    font13 = pygame.font.Font('images/calibri.TTF',13)
    font14 = pygame.font.Font('images/calibri.TTF',14)
    font15 = pygame.font.Font('images/calibri.TTF',15)
    font16 = pygame.font.Font('images/calibri.TTF',16)
    font20 = pygame.font.Font('images/calibri.TTF',20)
    font24 = pygame.font.Font('images/calibri.TTF',24)
    font30 = pygame.font.Font('images/calibri.TTF',30)
    font40 = pygame.font.Font('images/calibri.TTF',40)


    data = {
        "resize":False,     #True, when the window got resized
        "width":1000,
        "height":600,
        "run":True,
        "last_mspf":0,      #mspf = miliseconds per frame
        "avg_mspf":0,       #Average mspf (over 1 second)
        "long_avg_mspf":0,  #Average mspf over a long time (over 5 seconds)
        "avg_mspf_calc":[],
        "settings":{
            "color1":(255,255,255), #Background color
            "color2": (0,0,0), #Color for lines for example
            "color3": (200,200,200), #For example other background color, for fields
            "color_text": (0,0,0)
        },
        "fonts":Font,
        "font_data":{
            "12":font12,
            "13":font13,
            "14":font14,
            "15":font15,
            "16":font16,
            "20":font20,
            "24":font24,
            "30":font30,
            "40":font40
            },
        "log_list":[],
        "log_timer":0,
        "fullscreen":False
    }
    return data
















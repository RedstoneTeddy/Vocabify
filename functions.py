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
    needed_size = str(int(size))
    if data.get(needed_size) == None:
        data[needed_size] = pygame.font.Font('images/calibri.TTF',int(needed_size))
    return data.get(needed_size)

def init_data(version):
    font12 = pygame.font.Font('images/calibri.TTF',12)
    font13 = pygame.font.Font('images/calibri.TTF',13)
    font14 = pygame.font.Font('images/calibri.TTF',14)
    font15 = pygame.font.Font('images/calibri.TTF',15)
    font16 = pygame.font.Font('images/calibri.TTF',16)
    font20 = pygame.font.Font('images/calibri.TTF',20)
    font24 = pygame.font.Font('images/calibri.TTF',24)
    font30 = pygame.font.Font('images/calibri.TTF',30)
    font40 = pygame.font.Font('images/calibri.TTF',40)
    font_title = pygame.font.Font('images/title.TTF',80)


    data = {
        "version":version,
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
        "last_learn_generation_ms":-1,
        "font_data":{
            "12":font12,
            "13":font13,
            "14":font14,
            "15":font15,
            "16":font16,
            "20":font20,
            "24":font24,
            "30":font30,
            "40":font40,
            "title":font_title
            },
        "log_list":[],
        "log_timer":0,
        "fullscreen":False,
        "mode":"menu",
        "change_mode":None,
        "cards":"",
        "recent":[],
        "key_pressed": None,
        "mouse_wheel":None
    }
    return data



def Save_settings(data):
    file = open("settings.dat","w")
    settings_text = ""
    settings_text += f"{data.get('settings').get('color1')}\n"
    settings_text += f"{data.get('settings').get('color2')}\n"
    settings_text += f"{data.get('settings').get('color3')}\n"
    settings_text += f"{data.get('settings').get('color_text')}\n"
    settings_text += f"{data.get('recent')}\n"
    file.write(settings_text)
    file.close()


def Load_settings(data):
    file = open("settings.dat","r")
    lines = file.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].replace("\n","")
    data["settings"]["color1"] = eval(lines[0])
    data["settings"]["color2"] = eval(lines[1])
    data["settings"]["color3"] = eval(lines[2])
    data["settings"]["color_text"] = eval(lines[3])
    data["recent"] = eval(lines[4])
    file.close()











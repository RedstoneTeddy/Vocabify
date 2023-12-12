import easygui


def Main() -> None:
    '''
    Loads the current card-set and writes it into the recent-cards list
    '''
    file_handler = open(easygui.fileopenbox(),"r")
    cards_data = []
    cards_data = []
    cards_front = []
    cards_back = []
    cards_phase = []
    cards_last_wrong = []
    all_right = []
    all_wrong = []
    for line in file_handler.readlines():
        cards_data.append(eval(line))
    file_handler.close()

    for line in cards_data:
        cards_front.append(line[0])
        cards_back.append(line[1])
        cards_phase.append(line[2])
        cards_last_wrong.append(line[3])
        all_right.append(line[4])
        all_wrong.append(line[5])

    file_handler = open(easygui.filesavebox(),"w")
    text = ""
    for i in range(0,len(cards_front)):
        text += cards_front[i][0] + ";" + cards_back[i][0] + "\n"
    file_handler.write(text)
    file_handler.close()

if __name__ == "__main__":
    Main()

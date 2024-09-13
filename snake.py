# snake
import os
import random
import time
import keyboard

import colorama
RED_COLOR = colorama.Fore.RED
GREEN_COLOR = colorama.Fore.GREEN
EMPTY_COLOR = colorama.Fore.RESET


def is_collided(x: int, y: int, dont_check_head=False) -> bool:
    for i in range(int(dont_check_head), len(players_x)):
        if (x == players_x[i]) and (y == players_y[i]):
            return True
    else:
        return False


def berry_spawn():
    global berryX, berryY
    while True:
        ber_x = random.randint(0, MAP_X - 1)
        ber_y = random.randint(0, MAP_Y - 1)
        if is_collided(ber_x, ber_y):
            continue
        else:
            berryX = ber_x
            berryY = ber_y
            return


def print_screen():
    print('-' * (MAP_X*2 + 2))

    for y in range(MAP_Y):
        print('|', end='')

        for x in range(MAP_X):
            if (x == head_x) and (y == head_y):
                print(f"{GREEN_COLOR}@", end=f"{EMPTY_COLOR} ")
            elif (x == berryX) and (y == berryY):
                print(f"{RED_COLOR}$", end=f"{EMPTY_COLOR} ")
            else:
                for i in range(len(players_x)):
                    if (x == players_x[i]) and (y == players_y[i]):
                        print(f"{GREEN_COLOR}#", end=f"{EMPTY_COLOR} ")
                        break
                else:
                    print("*", end=' ')
        print('|')
    print('-' * (MAP_X*2 + 2))

    if clear_mode == 1:
        print(clear_screen_char)
    else:
        os.system(clear_screen_char)


def init_rules():
    file_name = "sneak_options.txt"
    global CAN_GO_AFTER_SCREEN
    global TIME_TO_UPDATE
    global CONSOLE_CONTROL
    global MAP_X, MAP_Y
    if file_name not in os.listdir():
        with open(file_name, "a+") as file:
            print("Вы впервые запускаете мою змейку, так-что установим правила:")
            button = input("Змейка может выходить за пределы экрана? (y/n) [default - n] [")
            if button.lower() == 'y':
                CAN_GO_AFTER_SCREEN = True
            else:
                CAN_GO_AFTER_SCREEN = False

            button = input("Управление через консоль? (y/n) [default - n] [")
            if button.lower() == 'y':
                CONSOLE_CONTROL = True
                TIME_TO_UPDATE = 0.5
            else:
                CONSOLE_CONTROL = False
                while not isinstance(button, float):
                    try:
                        button = float(input("Через сколько секунд экран будет обновляться? Можно ввести дробь"))
                    except ValueError:
                        print("Введите дробь")
                TIME_TO_UPDATE = button

            while True:
                button = input("Какой размер поля? (x y) через пробел [").split()
                if (button[0].isdigit()) and (button[1].isdigit()):
                    button[0] = int(button[0])
                    button[1] = int(button[1])
                    break
                else:
                    print("Введите нормально! (Пример:5 8)")

            MAP_X = button[0]
            MAP_Y = button[1]
            file.write(f"{CAN_GO_AFTER_SCREEN}\n")
            file.write(f"{CONSOLE_CONTROL}")
            file.write(f"{TIME_TO_UPDATE}")
            file.write(f"{MAP_X} {MAP_Y}")

    else:
        with open(file_name, "r+") as file:
            if file.readline() == "True":
                CAN_GO_AFTER_SCREEN = True
            else:
                CAN_GO_AFTER_SCREEN = False

            if file.readline() == "True":
                CONSOLE_CONTROL = True
            else:
                CONSOLE_CONTROL = False

            TIME_TO_UPDATE = float(file.readline())

            MAP_X, MAP_Y = [int(i) for i in file.readline().split()]
    print("init complete")
    print(CAN_GO_AFTER_SCREEN)
    print(MAP_X, MAP_Y)


def game_over():
    print("GAME OVER!!!")
    print(f"you're score is {len(players_x) - 1}")
    exit()


def player_move(player_input=None):
    global button
    if player_input is None:
        button = input()[0]

    elif isinstance(player_input, str):
        button = player_input[0]
    else:
        raise TypeError(f"{player_input} wtf?")


clear_mode = 0
clear_screen_char = "clear"
if os.system(clear_screen_char) != 0:
    clear_screen_char = "cls"
    if os.system(clear_screen_char) != 0:
        print("wtf!? what is you're OS?")
        clear_mode = 1
        clear_screen_char = "\n" * os.get_terminal_size()[0]


MAP_X = 0
MAP_Y = 0
TIME_TO_UPDATE = 0.5
CAN_GO_AFTER_SCREEN = False
CONSOLE_CONTROL = True
init_rules()

players_x = [MAP_X // 2]
players_y = [MAP_Y // 2]
head_x = players_x[0]
head_y = players_y[0]

berryX = 0
berryY = 0
berry_spawn()

button = ''
if not CONSOLE_CONTROL:
    button = 'w'
    keyboard.add_hotkey('w', player_move, ('w',))
    keyboard.add_hotkey('a', player_move, ('a',))
    keyboard.add_hotkey('s', player_move, ('s',))
    keyboard.add_hotkey('d', player_move, ('d',))

while True:
    print_screen()

    head_x = players_x[0]
    head_y = players_y[0]

    if is_collided(head_x, head_y, dont_check_head=True):
        game_over()
        break

    # where to move head
    if CONSOLE_CONTROL:
        player_move()
    else:
        time.sleep(TIME_TO_UPDATE)

    if button in "wц":
        head_y -= 1
    elif button in "aф":
        head_x -= 1
    elif button in "sы":
        head_y += 1
    elif button in "dв":
        head_x += 1

    # if moved over screen
    if head_x < 0:
        if CAN_GO_AFTER_SCREEN:
            head_x = MAP_X - 1
        else:
            game_over()
    elif head_x >= MAP_X:
        if CAN_GO_AFTER_SCREEN:
            head_x = 0
        else:
            game_over()
    elif head_y < 0:
        if CAN_GO_AFTER_SCREEN:
            head_y = MAP_Y - 1
        else:
            game_over()
    elif head_y >= MAP_Y:
        if CAN_GO_AFTER_SCREEN:
            head_y = 0
        else:
            game_over()

    # if eat berry
    if (head_x == berryX) and (head_y == berryY):
        players_x.insert(0, head_x)
        players_y.insert(0, head_y)
        berry_spawn()
    else:
        # move tail
        for i in range(len(players_x) - 1, 0, -1):
            players_x[i] = players_x[i - 1]
            players_y[i] = players_y[i - 1]
        players_x[0] = head_x
        players_y[0] = head_y

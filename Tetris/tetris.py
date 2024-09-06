import time
import os
import keyboard
import random


# will load from data_file
GAME_SIZE_X = 10
GAME_SIZE_Y = 20
falling_speed = 1.5
FPS = 10
HARDMODE = False
ALL_FALLING_TYPE = ["L->", "L<-", "I", "T", "Z->", "Z<-", "#"]
# will load from data_file


def load_data_file():
    global GAME_SIZE_X, GAME_SIZE_Y, falling_speed, FPS, HARDMODE, ALL_FALLING_TYPE
    options_file_name = "tetris_options.txt"
    try:
        with open(options_file_name, "r+") as file:
            GAME_SIZE_X = int(file.readline().replace("SIZE_X:", "").replace(" ", ""))
            GAME_SIZE_Y = int(file.readline().replace("SIZE_Y:", "").replace(" ", ""))
            falling_speed = float(file.readline().replace("falling_speed:", "").replace(" ", ""))
            FPS = int(file.readline().replace("FPS:", "").replace(" ", ""))
            HARDMODE = bool(file.readline().replace("HARDMODE:", "").replace(" ", "").replace("false", "").replace("true", "True").replace("False", "").replace("\n", ""))
            ALL_FALLING_TYPE = file.readline().replace("ALL_FALLING_TYPE:", "").replace(" ", "").split(",")
            ALL_FALLING_TYPE[-1] = ALL_FALLING_TYPE[-1].replace("\n", "")
    except FileNotFoundError:
        with open(options_file_name, "w+") as file:
            file.write(f"SIZE_X: {str(GAME_SIZE_X)}\n")
            file.write(f"SIZE_Y: {str(GAME_SIZE_Y)}\n")
            file.write(f"falling_speed: {str(falling_speed)}\n")
            file.write(f"FPS: {str(FPS)}\n")
            file.write(f"HARDMODE: {HARDMODE}\n")
            file.write(f"ALL_FALLING_TYPE: {','.join(str(i) for i in ALL_FALLING_TYPE)}\n")
            file.write('\n\n# Все возможные - ["L->", "L<-", "I", "T", "Z->", "Z<-", "#"] ')


class MyGameExcept(Exception):
    def __init__(self, text_error="It just works"):
        super().__init__(text_error)


class Falling:
    def __init__(self, shape: str, mod_x=GAME_SIZE_X // 2, mod_y=GAME_SIZE_Y):
        if (mod_y in level_map) and (mod_x in level_map[mod_y]):
            raise MyGameExcept("Game Over")
        self.mod_x = mod_x
        self.mod_y = mod_y
        self.type = shape
        self.stop_falling = False
        self.coordinates = {}  # of every cell

        match shape:
            case "L->":
                self.shape = ["# ",
                              "# ",
                              "##"
                              ]
            case "L<-":
                self.shape = [" #",
                              " #",
                              "##"
                              ]
            case "I":
                self.shape = ["#",
                              "#",
                              "#",
                              "#"
                              ]
            case "T":
                self.shape = [" # ",
                              "###"
                              ]
            case "Z->":
                self.shape = [" ##",
                              "## "
                              ]
            case "Z<-":
                self.shape = ["## ",
                              " ##"
                              ]
            case "#":
                self.shape = ["##",
                              "##"
                              ]
            case _:
                if shape in ALL_FALLING_TYPE:
                    raise MyGameExcept(f"Ты забыл добавить тип '{shape}' в класс")
                else:
                    raise MyGameExcept(f"создан объект '{shape}', которого нет в ALL_FALLING_TYPE")

        self.shape = self.shape[-1::-1]
        self.update_coordinates("falling")

    def rotate(self):  # Поменять на right
        if self.stop_falling is False:
            old_shape_copy = self.shape
            new_shape = [''] * len(self.shape[0])
            for x in range(len(self.shape[0])):
                line = ''
                for y in range(len(self.shape)):
                    line += self.shape[y][x]
                new_shape[x] = line

            self.shape = new_shape[-1::-1]
            if self.update_coordinates("moving") is True:
                pass
            else:
                self.shape = old_shape_copy

    def update_coordinates(self, mode: str) -> bool:
        coordinates_copy = self.coordinates

        self.coordinates = {}
        try:
            for y in range(len(self.shape)):
                y += self.mod_y
                for x in range(len(self.shape[0])):
                    if self.shape[y - self.mod_y][x] != " ":

                        x += self.mod_x
                        if (x < 0) or (x > GAME_SIZE_X-1):
                            raise MyGameExcept
                        elif (y < 0) or (y in level_map and x in level_map[y]):
                            if mode == "falling":
                                self.stop_falling = True
                            raise MyGameExcept

                        else:
                            if y in self.coordinates:
                                self.coordinates[y].append(x)
                            else:
                                self.coordinates[y] = [x, ]

            return True

        except MyGameExcept:
            self.coordinates = coordinates_copy

            if self.stop_falling is True:
                for y in self.coordinates:
                    for x in self.coordinates[y]:
                        if y in level_map:
                            level_map[y][x] = "#"
                        else:
                            level_map[y] = {}
                            level_map[y][x] = "#"

                new_falling_now()
            return False

    def move(self, add_x=0, add_y=0, key_pressed=""):
        if self.stop_falling is False:
            global score
            key_pressed = key_pressed.lower()
            if key_pressed == "s":
                score += 10 / GAME_SIZE_Y
            elif key_pressed == "space":
                score += 3 * 10 / GAME_SIZE_Y

            self.mod_y += add_y
            self.mod_x += add_x

            mode = "falling"
            if add_y == 0:
                mode = "moving"
            if self.update_coordinates(mode) is True:
                pass
            else:
                self.mod_y -= add_y
                self.mod_x -= add_x


def draw_screen():
    print_screen = f'score: {score}   | now falling: {falling_now.type} | next will fall: {next_type}\n'
    if HARDMODE is True:
        title = "THE HARDMODE!!!"
        print_screen += " "*( (GAME_SIZE_X*2 - len(title) + 2) // 2) + title + "\n"
    print_screen += " " + "__" * GAME_SIZE_X + " \n"
    for y in range(GAME_SIZE_Y, 0 - 1, -1):
        line = '|'
        for x in range(GAME_SIZE_X):
            if (y in level_map and x in level_map[y]) or (
                    y in falling_now.coordinates and x in falling_now.coordinates[y]):
                line += "[]"
            else:
                line += " *"

        print_screen += line + "|\n"

    print(print_screen)


def update_hotkeys():
    try:
        keyboard.clear_all_hotkeys()
    except AttributeError as error:
        if error.__str__() == "'_KeyboardListener' object has no attribute 'blocking_hotkeys'":
            pass
        else:
            raise error

    keyboard.add_hotkey("a", falling_now.move, (-1, ))
    keyboard.add_hotkey("d", falling_now.move, (1, ))
    keyboard.add_hotkey("s", falling_now.move, (0, -1, "s"))
    keyboard.add_hotkey("space", falling_now.move, (0, -GAME_SIZE_Y, "space"))
    keyboard.add_hotkey("w", falling_now.rotate)


def new_falling_now(mode=None):
    global all_falling_type
    global next_type
    global falling_now
    global level_map
    global score

    # Очистка линий
    if mode is None:
        cleared_lines_cnt = 0
        first_y = 0
        for y in falling_now.coordinates:
            if (y in level_map) and (len(level_map[y]) == GAME_SIZE_X):
                cleared_lines_cnt += 1
                first_y = min(y, first_y)
                del level_map[y]

        if cleared_lines_cnt > 0:
            score += 100 * (2 ** (cleared_lines_cnt - 1))

            if HARDMODE is False:
                all_lines = []
                for y in range(GAME_SIZE_Y):
                    if y in level_map:
                        if len(level_map[y]) == GAME_SIZE_X:
                            print("not cleared")
                        all_lines.append(level_map[y])

                level_map = {}
                for y in range(len(all_lines)):
                    level_map[y] = all_lines[y]

    if len(all_falling_type) == 0:
        all_falling_type = [i for i in ALL_FALLING_TYPE]
    if next_type is None:
        next_type = random.choice(all_falling_type)
        all_falling_type.remove(next_type)

    falling_now = Falling(next_type)
    next_type = random.choice(all_falling_type)
    all_falling_type.remove(next_type)


load_data_file()

falling_now = Falling
all_falling_type = []
level_map = {}

next_type = None
new_falling_now("First upload")
score = 0


# interface + game logic


last_fall_down = time.time()
while True:
    os.system("cls")
    draw_screen()

    time.sleep(1 / FPS)
    if time.time() - last_fall_down >= falling_speed:
        update_hotkeys()
        last_fall_down = time.time()
        falling_now.move(0, -1)

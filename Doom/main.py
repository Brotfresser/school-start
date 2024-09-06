"""import math



import arcade
import math


SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 920

PLAYER_SPEED = 5
PLAYER_TURN_SPEED = 0.04

TILE_SIZE = 100
FOV = math.pi / 3
NUM_RAYS = 10
MAX_REY_LEN = 5 * TILE_SIZE


WORLD = ["########################",
         "#*     ##    #    #    #",
         "#    #    #  # #  #    #",
         "#   #     #   #  #     #",
         "#       #     #  #     #",
         "########################"
         ]


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("player.png")
        self.W_is_pressed = False
        self.A_is_pressed = False
        self.D_is_pressed = False
        self.S_is_pressed = False
        self.math_angle = 0

    def moving(self):
        if self.W_is_pressed:
            self.center_x += PLAYER_SPEED * math.cos(self.math_angle)
            self.center_y += PLAYER_SPEED * math.sin(self.math_angle)
        if self.S_is_pressed:
            self.center_x += -PLAYER_SPEED * math.cos(self.math_angle)
            self.center_y += -PLAYER_SPEED * math.sin(self.math_angle)
        if self.A_is_pressed:
            self.center_x += -PLAYER_SPEED * math.sin(self.math_angle)
            self.center_y += PLAYER_SPEED * math.cos(self.math_angle)
        if self.D_is_pressed:
            self.center_x += PLAYER_SPEED * math.sin(self.math_angle)
            self.center_y += -PLAYER_SPEED * math.cos(self.math_angle)

    def update(self):
        self.math_angle += self.change_angle
        self.moving()


class Game(arcade.Window):
    def __init__(self):
        super().__init__(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
        self.all_sprite_draw_list = arcade.SpriteList()
        self.player = Player()
        self.camera = arcade.Camera()
        self.world_map = {}

        for z in range(len(WORLD)):
            for x in range(len(WORLD[z])):
                if WORLD[z][x] != " " and WORLD[z][x] != "*":
                    if WORLD[z][x] == "#":  # стена
                        object = arcade.Sprite("wall.png", scale=2)
                        object.position = x * TILE_SIZE, z * TILE_SIZE
                        if object.center_x in self.world_map:
                            self.world_map[object.center_x][object.center_y] = object
                        else:
                            self.world_map[object.center_x] = {object.center_y: object}
                    self.all_sprite_draw_list.append(object)

                else:
                    if WORLD[z][x] == "*":
                        self.player.position = x * TILE_SIZE, z * TILE_SIZE

        self.all_sprite_draw_list.append(self.player)

    def on_draw(self):
        self.clear()
        self.player.draw()
        #self.all_sprite_draw_list.draw()

        angle = self.player.math_angle - FOV / 2
        for ray in range(NUM_RAYS):
            sin_a = math.sin(angle)
            cos_a = math.cos(angle)
            chk = True
            for depth in range(MAX_REY_LEN+1, TILE_SIZE, -TILE_SIZE*2):
                x = (self.player.center_x + depth * cos_a)
                y = (self.player.center_y + depth * sin_a)

                x = (self.player.center_x + depth * cos_a) // TILE_SIZE * TILE_SIZE
                y = (self.player.center_y + depth * sin_a) // TILE_SIZE * TILE_SIZE
                if x in self.world_map and y in self.world_map[x]:
                    self.world_map[x][y].draw()
                    chk = False
                if ray % 2 == 0:
                    clr = 255
                else:
                    clr = 50
                arcade.draw_line(self.player.center_x, self.player.center_y, x, y, (0, clr, ray*10), line_width=4)
                if chk is not True:
                    break
            angle += FOV / NUM_RAYS

        arcade.draw_line(self.player.center_x, self.player.center_y,
                         self.player.center_x + MAX_REY_LEN * math.cos(self.player.math_angle),
                         self.player.center_y + MAX_REY_LEN * math.sin(self.player.math_angle),
                         (255, 0, 0))

    def update(self, delta_time: float):
        self.camera.move_to((self.player.center_x - SCREEN_WIDTH//2, self.player.center_y - SCREEN_HEIGHT//2), 1)
        self.camera.use()
        self.player.update()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.W:
            self.player.W_is_pressed = True
        if symbol == arcade.key.S:
            self.player.S_is_pressed = True
        if symbol == arcade.key.A:
            self.player.A_is_pressed = True
        if symbol == arcade.key.D:
            self.player.D_is_pressed = True

        if symbol == arcade.key.RIGHT:
            self.player.change_angle = -PLAYER_TURN_SPEED
        if symbol == arcade.key.LEFT:
            self.player.change_angle = PLAYER_TURN_SPEED
        if symbol == arcade.key.ESCAPE:
            arcade.exit()

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.W:
            self.player.W_is_pressed = False
        if symbol == arcade.key.S:
            self.player.S_is_pressed = False
        if symbol == arcade.key.A:
            self.player.A_is_pressed = False
        if symbol == arcade.key.D:
            self.player.D_is_pressed = False

        if (symbol == arcade.key.LEFT) or (symbol == arcade.key.RIGHT):
            self.player.change_angle = 0


if __name__ == "__main__":
    THE_GAME = Game()
    arcade.run()"""

from pynput.keyboard import Listener
import time
import colorama
import threading
import math
import os
colorama.init()


start_map = [
    "########################",
    "###............D.......#",
    "DC##..#..#.....D.......#",
    "#CC###C##C#########....#",
    "#.............#........#",
    "#.............#.....#DD#",
    "##C##..##..*..##..###..#",
    "#......##.....#........#",
    "#..###............#....#",
    "#....#..####...####....#",
    "#...C#.........#C......#",
    "########################",
       ]
start_map = start_map[::-1]


class Object:
    def __init__(self, x=0, y=0, type="wall", char="#"):
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        add_to_map(self.x, self.y, self)
        all_objects.append(self)
        self.type = type
        self.static = False
        self.char = char
        self.color = (255, 255, 255)

        self.type_init(type)

    def type_init(self, type):
        if type == "wall":
            self.color = 255, 255, 255
            self.static = True
            self.char = "#"
        elif type == "door":
            self.color = 150, 110, 30
            self.static = True
            self.char = "D"
        elif type == "coin":
            self.color = 255, 240, 50
            self.char = "C"

    def move(self, add_x=0, add_y=0):
        object = return_object_in(int((self.x + add_x) // TILE_SIZE * TILE_SIZE), int((self.y + add_y) // TILE_SIZE * TILE_SIZE))
        if (object is False) or (object.static is False):
            global_map[int(self.y)][int(self.x)].remove(self)
            self.x += add_x
            self.y += add_y
            add_to_map(int(self.x), int(self.y), self)
            if (self.type == "player") and (isinstance(object, Object)):
                if object.type == "coin":
                    global coins
                    coins += 1
                    object.del_obj()
                    if coins == all_coins_cnt:
                        for obj in all_objects:
                            if obj.type == "door":
                                obj.del_obj()

    def del_obj(self):
        all_objects.remove(self)
        global_map[int(self.y)][int(self.x)].remove(self)


class Player(Object):
    def __init__(self, x=0, y=0):
        super().__init__(x, y, "player", "*")
        self.angle = 0
        self.speed = TILE_SIZE / 4
        global CAMERA_X, CAMERA_Y
        CAMERA_X = x
        CAMERA_Y = y


def add_to_map(x, y, object):
    if (y in global_map) and (x in global_map[y]):
        global_map[y][x].append(object)
    else:
        if y in global_map:
            global_map[y][x] = [object,]
        else:
            global_map[y] = {x: [object, ]}


def keyboard_listen():
    def key_pressed(key):
        global CONSOLE_SWITCH

        if CONSOLE_SWITCH is False:
            key = str(key)
            if key[1] in "wasd":
                if key[1] == "w":
                    add_x = player.speed * math.cos(player.angle)
                    add_y = player.speed * math.sin(player.angle)
                elif key[1] == "s":
                    add_x = -player.speed * math.cos(player.angle)
                    add_y = -player.speed * math.sin(player.angle)
                elif key[1] == "d":
                    add_x = player.speed * math.sin(player.angle)
                    add_y = -player.speed * math.cos(player.angle)
                else:  # key[1] == "a":
                    add_x = -player.speed * math.sin(player.angle)
                    add_y = player.speed * math.cos(player.angle)

                player.move(add_x, add_y)
            elif key == "Key.left":
                player.angle += 0.2
            elif key == "Key.right":
                player.angle -= 0.2
            elif key[1] == "/":
                if CONSOLE_SWITCH is True:
                    CONSOLE_SWITCH = False
                else:
                    CONSOLE_SWITCH = True

    with Listener(on_press=key_pressed) as lst:
        lst.join()


def return_object_in(x, y):
    if (y in global_map) and (x in global_map[y]):

        objects_list = global_map[y][x]
        for obj in objects_list:
            if isinstance(obj, Object):
                return obj

        return False

    else:
        return False


def on_draw():
    os.system("cls")

    if TOP_DOWN_MODE:
        screen = {}  # Создание пустого экрана
        for y in range(CAMERA_SIZE_Y//2 * TILE_SIZE, -CAMERA_SIZE_Y//2 * TILE_SIZE, -TILE_SIZE):
            for x in range(-CAMERA_SIZE_X//2 * TILE_SIZE, CAMERA_SIZE_X//2 * TILE_SIZE, TILE_SIZE):
                if y in screen:
                    screen[y][x] = " "
                else:
                    screen[y] = {x: " "}
    else:
        screen = {}  # Создание пустого экрана
        for y in range(TERMINAL_HEIGTH):
            for x in range(TERMINAL_WIDTH):
                if y in screen:
                    screen[y][x] = " "
                else:
                    screen[y] = {x: " "}

    ray_angle = player.angle - (FOV/2)  # Заполнение тем, что видит игрок
    for ray_id in range(RAYS_CNT):
        cos_a = math.cos(ray_angle)
        sin_a = math.sin(ray_angle)
        for depth in range(1, MAX_RAY_LEN):
            x = int(CAMERA_X + depth * cos_a) // TILE_SIZE * TILE_SIZE
            y = int(CAMERA_Y + depth * sin_a) // TILE_SIZE * TILE_SIZE

            if TOP_DOWN_MODE:
                screen_x = x - int(CAMERA_X)
                screen_y = y - int(CAMERA_Y)
                try:
                    if (y in global_map) and (x in global_map[y]):
                        lst = global_map[y][x]

                        if len(lst) > 1:
                            if return_object_in(x, y, player):
                                screen[screen_y][screen_x] = player.char
                            else:
                                screen[screen_y][screen_x] = lst[-1].char
                                break

                        elif len(lst) == 1:
                            screen[screen_y][screen_x] = lst[-1].char
                            if return_object_in(x, y, player) is False:
                                break

                        else:
                            screen[screen_y][screen_x] = "."
                    else:
                        screen[screen_y][screen_x] = "."
                except (KeyError, IndexError):
                    pass
            else:
                if (y in global_map) and (x in global_map[y]):
                    lst = global_map[y][x]

                    if len(lst) > 0:
                        for i in range(-len(lst), -1 + 1):
                            if lst[i].type != "player":
                                depth *= math.cos(player.angle - ray_angle)
                                proj_coef = int(PROJ_COEF / depth)

                                for screen_x in range(1, int(SCALE) + 1):
                                    for screen_y in range(int(TERMINAL_HEIGTH//2 - proj_coef//2), int(proj_coef)):
                                        try:
                                            color1 = int(lst[i].color[0] - ( (depth / TILE_SIZE) * (lst[i].color[0] / MAX_DEPTH_CELLS) ) )
                                            color2 = int(lst[i].color[1] - ((depth / TILE_SIZE) * (lst[i].color[1] / MAX_DEPTH_CELLS)))
                                            color3 = int(lst[i].color[2] - ((depth / TILE_SIZE) * (lst[i].color[2] / MAX_DEPTH_CELLS)))

                                            #color = int(255 - ((depth / TILE_SIZE) * (255 / MAX_DEPTH_CELLS)))
                                            char = "█"

                                            if (screen[screen_y][screen_x * ray_id] == " ") and (color1 > 10) and (color2 > 10) and (color3 > 10):
                                                screen[screen_y][screen_x * ray_id] = f"\033[38;2;{color1};{color2};{color3}m" + char + colorama.Style.RESET_ALL
                                        except KeyError:
                                            pass

                                break
                        else:
                            pass
                    else:
                        pass
                else:
                    pass

        ray_angle += FOV / RAYS_CNT

    to_draw = ""
    print(f"coins: {coins}/{all_coins_cnt}")
    print("-"*TERMINAL_WIDTH)
    if TOP_DOWN_MODE:
        print(" " + "_" * CAMERA_SIZE_X)
        for y in range((CAMERA_SIZE_Y // 2) * TILE_SIZE, (-CAMERA_SIZE_Y // 2) * TILE_SIZE, -TILE_SIZE):
            to_draw += "|"
            for x in range((-CAMERA_SIZE_X // 2) * TILE_SIZE, (CAMERA_SIZE_X // 2) * TILE_SIZE, TILE_SIZE):
                to_draw += screen[y][x]
            to_draw += "|\n"
    else:
        for y in range(TERMINAL_HEIGTH-3):
            to_draw += "|"
            for x in range(TERMINAL_WIDTH-1, 0, -1):
                to_draw += screen[y][x]
            #to_draw += "|"
    print(to_draw)


# Top down mode
CAMERA_SIZE_X = 40
CAMERA_SIZE_Y = 20
#

CAMERA_X = 0
CAMERA_Y = 0

TOP_DOWN_MODE = False
TILE_SIZE = 5

FOV = math.pi / 3
MAX_DEPTH_CELLS = 7
MAX_RAY_LEN = MAX_DEPTH_CELLS * TILE_SIZE
RAYS_CNT = 120

# 3D mode
PROJ_COEF = (RAYS_CNT / (2 * math.tan(FOV / 2))) * TILE_SIZE
TERMINAL_WIDTH, TERMINAL_HEIGTH = os.get_terminal_size()
SCALE = TERMINAL_WIDTH // RAYS_CNT
#

CONSOLE_SWITCH = False
TIME_TO_SLEEP = 0.2

global_map = {}
all_objects = []
all_coins_cnt = 0
coins = 0

# Загружаем карту
for y in range(len(start_map)):
    for x in range(len(start_map[y])):
        obj_type = start_map[y][x]

        if obj_type == "#":
            Object(x, y, "wall")
        elif obj_type == "D":
            Object(x, y, "door")
        elif obj_type == "C":
            all_coins_cnt += 1
            Object(x, y, "coin")
        elif obj_type == "*":
            player = Player(x, y)

threading.Thread(target=keyboard_listen).start()


last_com = ""
while True:
    CAMERA_X = int(player.x)
    CAMERA_Y = int(player.y)
    TERMINAL_WIDTH, TERMINAL_HEIGTH = os.get_terminal_size()
    SCALE = TERMINAL_WIDTH // RAYS_CNT
    on_draw()
    if CONSOLE_SWITCH:
        try:
            exec(last_com)
        except NameError:
            pass
        except Exception as error:
            print(error)

        com = input()
        last_com = com
        if com == "/":
            CONSOLE_SWITCH = False
    else:
        time.sleep(TIME_TO_SLEEP)

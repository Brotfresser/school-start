# https://api.arcade.academy/en/latest/resources.html
# C:\Users\Brotfresser\PycharmProjects\Manchkin\venv\Lib\site-packages\arcade\examples
"""***"""

"""
# Деление
ZeroDivision = Exception("Делить на ноль нельзя")
import sys
import math


def delimost(x, y, check=False, ans=None):
    if y == 0:
        raise ZeroDivision

    if x - y <= 0:

        if ans is None:
            return 0

        if x - y == 0:
            return ans + 1

        else:
            if check:
                return False

            for i in range(1, math.ceil(math.log(sys.getrecursionlimit(), 10)) + 1):
                i = 10**i
                ost = delimost(i, y, check=True, ans=0)
                if ost:
                    return float(ans) + float( "0." + str(x * ost) )
            else:
                return f"{ans} + {x}/{y}"

    if ans is None:
        ans = 0

    return delimost(x - y, y, check, ans + 1)
"""

"""***"""

"""
# Жизнь
import time
import random

world = {}
alive = 0
MAP_X = 60
MAP_Y = 30
char = "#"
GAME_SPEED = 1


def check_outside(sx, sy):
    cnt = 0
    for mod_x in range(-1, 2):
        for mod_y in range(-1, 2):
            x = sx + mod_x
            y = sy + mod_y
            if (x in world) and (y in world[x]):
                cnt += 1
    if (sx in world) and (sy in world[sx]):
        cnt -= 1
    return cnt


def check_all_cells():
    global world
    global alive

    screen = ""
    del_list = []
    add_list = []
    for y in range(MAP_Y):
        for x in range(MAP_X):

            if (x in world) and (y in world[x]):

                if check_outside(x, y) in [2, 3]:
                    screen += char
                else:
                    del_list.append((x, y))
                    screen += char

            else:

                if check_outside(x, y) == 3:
                    add_list.append((x, y))
                    screen += " "
                else:
                    screen += " "
        screen += "\n"

    print(screen)
    for cell in del_list:
        del world[cell[0]][cell[1]]
        alive -= 1

    for cell in add_list:
        create(*cell)


def create(x, y):
    global alive
    alive += 1

    if x >= MAP_X:
        x -= MAP_X
    if y >= MAP_Y:
        y -= MAP_Y
    if x in world:
        world[x][y] = 1
    else:
        world[x] = {y: 1}


def create_many(*add):
    for i in range(0, len(add), 2):
        create(add[i], add[i+1])


def create_struct(sx, sy, *add):
    new_add = []

    for i in range(len(add)):
        if i % 2 == 0:
            new = sx + add[i]
        else:
            new = sy + add[i]

        new_add.append(new)
    create_many(*new_add)


def random_generate():
    for _ in range(random.randint(int(MAP_X * MAP_Y * 0.5), int(MAP_X * MAP_Y * 0.8) + 1)):
        x = random.randint(0, MAP_X - 1)
        y = random.randint(0, MAP_Y - 1)
        create(x, y)

        while random.randint(1, 100) in range(1, 70 + 1):
            x += random.randint(-1, 1)
            y += random.randint(-1, 1)
            create(x, y)


glyder = 1,0, 2,1, 0,2, 1,2, 2,2
create_struct(10, 9, *glyder)
#create(1, 1)

iter_cycle = 0
while True:
    print("\n" * 1)
    print(f"Население: {alive}{' ' * 20}Поколение: {iter_cycle}")
    print("_" * MAP_X)

    check_all_cells()

    print("‾" * MAP_X)
    iter_cycle += 1
    time.sleep(GAME_SPEED)
    print("\033[J")
"""

"""***"""
"""
# пинг-понг (не закончен)
from random import randint
from random import choice
import os

map = {}
auto = True
max_x = 15
min_x = -max_x
max_y = 3
min_y = -max_y

for x in range(min_x, max_x + 1):
    map[x]={}
    for y in range(min_y, max_y + 1):
        map[x][y] = " "

        if x == max_x or x == min_x or y == max_y or y == min_y:
            map[x][y] = "0"


class Ball:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.direction = choice([-1,1])
        self.start_angle = randint(20, 70)
        self.angle = self.start_angle

    def update(self):
        if self.angle >= 0:
            angle_mod = 1
            angle = self.angle
        else:
            angle_mod = -1
            angle = -self.angle

        if angle >= 45:
            angle -= 45
            self.angle -= 45 * angle_mod
            self.y += 1 * angle_mod
        if angle < 45:
            self.x += self.direction
            self.angle += self.start_angle * angle_mod
            angle += self.start_angle

        if map[self.x][self.y] == "0":
            if self.x == max_x:
                self.direction = -1
                self.x -= 1
            if self.x == min_x:
                self.direction = 1
                self.x += 1
            if self.y == max_y:
                self.angle *= -1
                self.y -= 1
            if self.y == min_y:
                self.angle *= -1
                self.y += 1


ball = Ball()
balls_list = [ball]
fps = 0
time_to_spawn = randint(6, 20)
remain = 99

while True:
    fps += 1
    if fps // 1000000 == 1 or not auto:
        os.system('cls')
        for y in range(max_y, min_y - 1, -1):
            line = ""
            for x in range(min_x, max_x + 1):
                line += map[x][y]

            for ball in balls_list:
                if y == ball.y:
                    line = line[:ball.x + max_x] + "p" + line[ball.x + max_x + 1:]
            print(line)

        for ball in balls_list:
            ball.update()

        fps = 0
        if remain == time_to_spawn:
            remain = 0
            time_to_spawn = randint(6, 20)
            ball = Ball()
            balls_list.append(ball)
        else:
            remain += 1

        if not auto:
            input()
"""







"""***"""

""" # Первая анимация
import arcade
from random import randint

CHARACTER_SPEED = 5
RIGHT_DIRECTION = 0
LEFT_DIRECTION = 1


def person_load(path):
    return [arcade.load_texture(path), arcade.load_texture(path, flipped_horizontally=True)]


class NPC(arcade.AnimatedTimeBasedSprite):
    def __init__(self):
        super().__init__()
        self.center_x = 400
        self.center_y = 37
        self.time = 0
        self.tired = False
        self.tired_animation1 = False
        self.direction = LEFT_DIRECTION
        self.tired_count = 0
        self.tired_texture_list = []
        for i in range(1, 9):  # Список анимации уставшего
            tired_texture = person_load(f"database/resources/person/oldman-idle/oldman-idle-{i}.png")
            self.tired_texture_list.append(tired_texture)

    def on_update(self, delta_time: float = 1 / 60):
        if self.time > 0 and not self.tired:  # Если его коснутся, запуститься таймер (в Game.on_update())
            self.time += 1
            if self.time == 20:  # Когда пройдёт 2 секунды, начнёт проигрываться анимация
                self.tired = True
                self.time = 0
        elif not self.tired:  # Если таймер не запущен и анимация не играет
            if self.direction == RIGHT_DIRECTION:
                self.change_x = CHARACTER_SPEED
            if self.direction == LEFT_DIRECTION:
                self.change_x = -CHARACTER_SPEED

        if self.center_x <= 10:  # Если в левом краю карты
            self.direction = RIGHT_DIRECTION
        elif self.center_x >= 690:
            self.direction = LEFT_DIRECTION

    def update_animation(self, delta_time: float = 1 / 60):
        if self.tired:  # Анимация
            self.change_x = 0
            if self.tired_count >= 8:  # Если дед передохнул (проигралась половина анимации)
                self.tired_animation1 = True
                self.tired_count -= 1
            else:
                self.texture = self.tired_texture_list[self.tired_count][self.direction]
                if not self.tired_animation1:  # Если дед не передохнул
                    self.tired_count += 1  # Анимация идёт вправо
                else:
                    self.tired_count -= 1  # Анимация идёт в обратном направлении
                if self.tired_count < 0:  # Если анимация закончилась
                    self.tired_animation1 = False
                    self.tired = False
                    self.tired_count += 1
        else:
            self.texture = person_load("database/resources/person/oldman-idle/oldman-idle-1.png")[self.direction]


class Player(arcade.AnimatedTimeBasedSprite):
    def __init__(self):
        super().__init__()
        self.center_x = 100
        self.center_y = 8
        self.direction = RIGHT_DIRECTION
        self.stay = False
        self.texture_walk_count = 0
        self.texture_idle_count = 0
        self.player_texture = person_load("database/resources/person/bearded-idle/bearded-idle-1.png")
        self.walk_texture_list = []
        self.stay_texture_list = []
        self.texture = self.player_texture[self.direction]
        for i in range(1, 7):  # Список анимации ходьбы
            walk_texture = person_load(f"database/resources/person/bearded-walk/bearded-walk-{i}.png")
            self.walk_texture_list.append(walk_texture)
        for i in range(1, 6):  # Список анимации стояния
            stay_texture = person_load(f"database/resources/person/bearded-idle/bearded-idle-{i}.png")
            self.stay_texture_list.append(stay_texture)

    def moving(self, symbol):  # Вызывается в on_key_pressed
        if symbol == arcade.key.D:
            self.change_x = CHARACTER_SPEED
        elif symbol == arcade.key.A:
            self.change_x = -CHARACTER_SPEED
        elif symbol == arcade.key.W or symbol == arcade.key.SPACE or symbol == arcade.key.UP:
            if window.physic_engine.can_jump():
                self.change_y = CHARACTER_SPEED * 15

    def stop_moving(self, symbol):  # Вызывается в on_ley_release
        if symbol == arcade.key.D:
            self.change_x = 0
        elif symbol == arcade.key.A:
            self.change_x = 0

    def update_animation(self, delta_time: float = 1 / 60):
        if self.change_x == 0:  # Если стоит на мечте
            if not self.stay:  # И если анимация не проиграна
                if self.texture_idle_count >= 5:
                    self.stay = True
                    self.texture_idle_count = 0
                else:
                    self.texture = self.stay_texture_list[self.texture_idle_count][self.direction]
                    self.texture_idle_count += 1
        else:  # Иначе (если двигается)
            self.stay = False
            # Проверка направления игрока
            if self.change_x > 0 and self.direction == LEFT_DIRECTION:
                self.direction = RIGHT_DIRECTION
            elif self.change_x < 0 and self.direction == RIGHT_DIRECTION:
                self.direction = LEFT_DIRECTION
            # Анимация ходьбы
            if self.texture_walk_count >= 6:
                self.texture_walk_count = 0
            self.texture = self.walk_texture_list[self.texture_walk_count][self.direction]
            self.texture_walk_count += 1


class Game(arcade.Window):
    def __init__(self):
        super().__init__(width=700, height=500, title="animation test", update_rate=1/8)
        arcade.set_background_color((55, 55, 80))
        self.background_town = arcade.load_texture("database/resources/bg/middleground.png")
        self.house_sprite = None
        self.house_sprite_list = arcade.SpriteList()
        self.platform_sprite = None
        self.platform_list = arcade.SpriteList()
        self.physic_engine = None
        self.player = Player()
        self.villager = NPC()
        self.debugging_mode = False

    def setup(self):
        for x in range(0, self.width+16, 16):  # Генерация платформ
            # Пол
            random_type = randint(1, 2)
            self.platform_sprite = arcade.Sprite(f"database/resources/enviroments/wall-{random_type}.png")
            self.platform_sprite.center_x = x
            self.platform_sprite.bottom = 0
            self.platform_list.append(self.platform_sprite)
            # Потолок
            random_type = randint(1, 2)
            self.platform_sprite = arcade.Sprite(f"database/resources/enviroments/wall-{random_type}.png")
            self.platform_sprite.center_x = x
            self.platform_sprite.bottom = self.height-16
            self.platform_list.append(self.platform_sprite)
        for x in range(40, self.width + 100, 200 + randint(100, 400)):  # Генерация домов
            random_type = randint(0, 2)
            self.house_sprite = arcade.Sprite(f"database/resources/enviroments/house-{random_type}.png")
            self.house_sprite.center_x = x
            self.house_sprite.bottom = 16
            self.house_sprite_list.append(self.house_sprite)
        self.physic_engine = arcade.PhysicsEnginePlatformer(self.player, self.platform_list)

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.TAB:
            if self.debugging_mode:
                self.debugging_mode = False
            else:
                self.debugging_mode = True
        else:
            self.player.moving(symbol)

    def on_key_release(self, symbol: int, modifiers: int):
        self.player.stop_moving(symbol)

    def on_update(self, delta_time: float):
        self.physic_engine.update()
        self.player.update()
        self.player.update_animation()
        if arcade.check_for_collision(self.player, self.villager) and not self.villager.tired:
            self.villager.time += 1
        self.villager.update_animation()
        self.villager.update()
        self.villager.on_update()
        if self.debugging_mode:
            print(self.player.center_x, self.player.center_y)

    def on_draw(self):
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0, self.width, self.height, self.background_town)
        self.house_sprite_list.draw()
        self.platform_list.draw()
        self.villager.draw()
        self.player.draw()


if __name__ == "__main__":
    window = Game()
    window.setup()
    arcade.run()
"""


"""***"""


""" # Таджик в пустоте https://api.arcade.academy/en/latest/resources.html
import arcade


class Game(arcade.Window):
    def __init__(self):
        super().__init__(width=500, height=500, title="Падший")
        self.floor = arcade.Sprite(":resources:images/isometric_dungeon/stoneSideUneven_N.png",
                                   center_x=250, center_y=400)
        self.player = arcade.Sprite(":resources:images/animated_characters/male_person/malePerson_walk6.png",
                                    center_x=200, center_y=250)

    def setup(self):
        pass

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.D or symbol == arcade.key.RIGHT:
            self.player.change_x = 1
        elif symbol == arcade.key.A or symbol == arcade.key.LEFT:
            self.player.change_x = -1
        elif symbol == arcade.key.D or symbol == arcade.key.RIGHT:
            self.player.change_x = 1

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.D or symbol == arcade.key.RIGHT or symbol == arcade.key.A or symbol == arcade.key.LEFT:
            self.player.change_x = 0

    def on_draw(self):
        self.clear()
        self.floor.draw()
        self.player.draw()
        self.player.update()
        if self.player.center_x >= 305:
            self.player.angle = -10
            self.player.change_y = -15
        elif self.player.center_x <= 190:
            self.player.angle = 10
            self.player.change_y = -15
        if self.player.center_y <= 100:
            arcade.draw_text("Аааа", self.player.center_x+10, self.player.center_y+10, color=arcade.color.BONE,
                             rotation=-10, font_size=50)
        if self.player.center_y <= -1000:
            arcade.draw_text("Упал", 100, 100, color=arcade.color.BONE, rotation=10, font_size=100)


if __name__ == "__main__":
    program = Game()
    program.setup()
    arcade.run()

"""


"""***"""


""" #первый arcade
import arcade
class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(width=500, height=500, title='Looking Head')
        arcade.set_background_color(arcade.color.BONE)
    def setup(self, func):
        def character():
            arcade.draw_circle_filled(250, 200, 100, color=(255, 255, 255, 185))
            arcade.draw_circle_filled(200, 210, 30, color=(0, 0, 0, 200))
            arcade.draw_circle_filled(300, 210, 30, color=(0, 0, 0, 200))
            arcade.draw_line(200, 150, 300, 151, color=(0,0,0,170), line_width=8)
        def halo():
            width = 150
            height = 80
            start_angle = 180
            end_angle = 360
            line_width = 10
            arcade.draw_arc_outline(250, 300, width, height, arcade.color.BLACK, start_angle, end_angle, line_width)
        match func:
            case 1:
                character()
            case 2:
                halo()
    def on_draw(self):
        self.clear()
        self.setup(1)
        self.setup(2)
window = MyGame()
window.setup(0)
arcade.run()
"""


"""***"""


""" # Сапёр
from random import choice
from random import randint
from os import system

debug_mode = False


class Cell:
    def __init__(self, cell_x: int, cell_y: int, cell_type: str, cell_pos: str):
        self.type = cell_type  # Бомба, Пусто
        self.cell_pos = cell_pos  # Слева, Справа, Сверху, Снизу, Не на краю, СлеваСверху, СлеваСнизу...

        self.is_open = False
        self.checked_around = False
        self.is_flagged = False

        self.bombs_around = 0

        self.x = cell_x
        self.y = cell_y

    def open(self):  # Когда игрок открывает клетку
        if not self.bombs_around and not self.checked_around and not self.type == "Бомба":
            cell_x_in_list = self.x - 1
            cell_y_in_list = self.y - 1

            self.checked_around = True

            code_left = 'cell_list[cell_x_in_list - 1][cell_y_in_list].open()'
            code_right = 'cell_list[cell_x_in_list + 1][cell_y_in_list].open()'
            code_down = 'cell_list[cell_x_in_list + mod_x][cell_y_in_list + 1].open()'
            code_up = 'cell_list[cell_x_in_list + mod_x][cell_y_in_list - 1].open()'

            index = (MAP_RANGE_X * cell_y_in_list) + cell_x_in_list
            log_list[index] = check_cell_around_with_code(self, cell_x_in_list, cell_y_in_list,
                                                          code_left, code_right, code_down, code_up)

        if not self.is_open:
            self.is_open = True
            if self.type == "Бомба":
                global attempts

                attempts -= 1

        else:
            print("Эта ячейка уже открыта")
        print(self.type)
        print(f"x: {self.x} y: {self.y} бомб: {self.bombs_around}")

    def show(self):  # Когда консоли нужно отрисовать клетку
        if self.is_flagged:
            return " / "

        elif self.is_open:
            if self.type == "Бомба":
                return " # "
            else:
                if self.bombs_around == 0:
                    return "   "
                else:
                    return f" {self.bombs_around} "

        else:
            return " * "


def clear_console():  # Очистка консоли (не работает в IDLE)
    clear = lambda: system('cls')
    clear()


def check_cell_position(cell_x, cell_y):
    cell_position = ""

    # Проверка по х
    if cell_x == 1:
        cell_position += "Слева"
    elif cell_x == MAP_RANGE_X:
        cell_position += "Справа"

    # Проверка по у
    if cell_y == 1:
        cell_position += "Сверху"
    elif cell_y == MAP_RANGE_Y:
        cell_position += "Снизу"

    if not cell_position:
        cell_position = "Не на краю"

    return cell_position


def check_cell_around_with_code(cell, cell_x_in_list, cell_y_in_list, code_left: str, code_right: str, code_down: str, code_up: str):
    a1 = False
    a2 = False
    b1 = False
    b11 = 0
    b2 = False
    b21 = 0

    if "Слева" not in cell.cell_pos:
        min_operation = -1
    else:
        min_operation = 0
    if "Справа" not in cell.cell_pos:
        max_operation = 1
    else:
        max_operation = 0

    # Проверка слева и справа
    if min_operation:
        a1 = True
        exec(code_left)
    if max_operation:
        a2 = True
        exec(code_right)

    # Проверка ниже клетки
    if "Снизу" not in cell.cell_pos:
        b1 = True
        for mod_x in range(min_operation, max_operation + 1):
            exec(code_down)
            b11 += 1

    # Проверка выше клетки
    if "Сверху" not in cell.cell_pos:
        b2 = True
        for mod_x in range(min_operation, max_operation + 1):
            exec(code_up)
            b21 += 1

    return (cell.x, cell.y, cell.bombs_around, cell.cell_pos, min_operation, max_operation, a1, a2, b1, b11, b2, b21)


def player_control():
    global bombs_count
    global all_flags_correct_count
    # Если игрок написал координаты клетки
    open_position = operation.split()
    open_position = [int(pos) - 1 for pos in open_position]

    open_cell_x = open_position[0]
    open_cell_y = open_position[1]
    if fl_check:
        if cell_list[open_cell_x][open_cell_y].is_open and cell_list[open_cell_x][open_cell_y].type == "Пусто":
            print("Эта клетка пустая")

        else:
            if cell_list[open_cell_x][open_cell_y].is_flagged:
                cell_list[open_cell_x][open_cell_y].is_flagged = False
                bombs_count += 1
                all_flags_correct_count -= 1

            else:
                cell_list[open_cell_x][open_cell_y].is_flagged = True
                bombs_count -= 1
                if cell_list[open_cell_x][open_cell_y].type == "Бомба": all_flags_correct_count += 1

    elif ck_check:
        index = (MAP_RANGE_X * open_cell_y) + open_cell_x
        print(f"(x, y, b, '{log_list[index][3]}', n, x,    a1,       a2,      b1, b11, b2,    b21)")
        print(log_list[index])

    else:  # Когда просто вводятся координаты
        cell_list[open_cell_x][open_cell_y].open()

while True:

    bombs_count = 0
    attempts = 20

    print("    Добро пожаловать в Сапёра!!")
    print("  1 - начать игру")
    print("  0 - выйти")
    operation = input()
    if operation == "1":
        print("  Введите через пробел размер поля по x и по y, или выберите сложность:")
        print("1 - Легко (9 9) (10 мин)")
        print("2 - Средняя (16 16) (40 мин)")
        print("3 - Жёсткая (16 30) (99 мин)")
        print("4 - Крайность (24 30) (160 мин)")
        operation = input()

        if operation.isdigit():
            if operation == "1":
                difficulty = [9, 9]
                bombs_count = 10
            elif operation == "2":
                difficulty = [16, 16]
                bombs_count = 40
            elif operation == "3":
                difficulty = [16, 30]
                bombs_count = 99
            elif operation == "4":
                difficulty = [24, 30]
                bombs_count = 160

        else:
            bombs_count = int(input("Введите кол-во бомб: "))

            difficulty = operation.split()
            difficulty = [int(size) for size in difficulty]

        MAP_RANGE_X = difficulty[0]
        MAP_RANGE_Y = difficulty[1]

    else:  # выход
        break

    # Генерация клеток
    cell_list = []
    for x in range(1, MAP_RANGE_X + 1):
        cell_list.append([])

        for y in range(1, MAP_RANGE_Y + 1):
            cell_position = check_cell_position(x, y)
            cell = Cell(x, y, "Пусто", cell_position)

            list_index = x - 1
            cell_list[list_index].append(cell)

    # Случайная генерация бомб
    for _ in range(bombs_count):
        rand_cell = choice(cell_list[randint(0, MAP_RANGE_X - 1)])
        while rand_cell.type == "Бомба":  # Если в случайной клетке уже есть бомба, выбирается другая
            rand_cell = choice(cell_list[randint(0, MAP_RANGE_X - 1)])

        rand_cell.type = "Бомба"

    log_list = []
    # Проверка кол-ва бомб вокруг каждой клетки
    for y in range(1, MAP_RANGE_Y + 1):
        for x in range(1, MAP_RANGE_X + 1):
            cell = cell_list[x - 1][y - 1]
            cell_x_in_list = x - 1
            cell_y_in_list = y - 1

            code_left = 'if cell_list[cell_x_in_list - 1][cell_y_in_list].type == "Бомба": cell.bombs_around += 1'
            code_right = 'if cell_list[cell_x_in_list + 1][cell_y_in_list].type == "Бомба": cell.bombs_around += 1'
            code_down = 'if cell_list[cell_x_in_list + mod_x][cell_y_in_list + 1].type == "Бомба": cell.bombs_around += 1'
            code_up = 'if cell_list[cell_x_in_list + mod_x][cell_y_in_list - 1].type == "Бомба": cell.bombs_around += 1'

            log_list.append(check_cell_around_with_code(cell, cell_x_in_list, cell_y_in_list, code_left, code_right, code_down, code_up))


    # Здесь происходит запуск игры (для игрока)


    separator = "  |  "
    all_bombs_count = bombs_count
    all_flags_correct_count = 0

    while True:  # Игра
        clear_console()
        ck_check = False
        fl_check = False

        print(f"Всего бомб: {all_bombs_count}{separator}Неизвестных бомб: {bombs_count}"
              f"{separator}Попыток осталось: {attempts}")

        print("Чтобы поставить флаг, добавьте перед координатами fl ")
        print("Чтобы начать новую игру, введите exit")

        # Отрисовка верхнего ограничителя
        for i in range(MAP_RANGE_X):
            print("___", end="")
        print()

        # Отрисовка строки координат по х
        for x in range(1, MAP_RANGE_X + 1):
            if x > 9:  # Если координата по х - двухзначное (иначе они выходят за сетку)
                print(f" {x}", end="")
            else:
                print(f" {x} ", end="")
        print()

        # Отрисовка поля + координаты по у
        y = 1
        for cell_by_y_id in range(MAP_RANGE_Y):
            for cell_by_x in cell_list:
                print(cell_by_x[cell_by_y_id].show(), end="")

            # Когда прошлись по всем клеткам этой строки, пишется координата у и новая строка
            print(y)
            y += 1

        # Отрисовка нижнего ограничителя
        for i in range(MAP_RANGE_X):
            print("‾‾‾", end="")
        print()

        if all_flags_correct_count == all_bombs_count:
            print("Вы победили!")
        else:
            print("Введите координаты клетки, которую хотите открыть:")
        operation = input()

        if "fl" in operation:
            fl_check = True
            operation = operation[3:]
        elif "ck" in operation:
            ck_check = True
            operation = operation[3:]
        elif operation == "exit":
            break



        if debug_mode:
            player_control()

        else:
            try:
                player_control()

            except:
                print("Ошибка")
                input()


    # Очистка консоли (не работает в IDLE)
    clear_console()
"""


"""***"""


"""  # Смена дня и ночи в arcade
import arcade
from arcade.experimental.lights import LightLayer, Light

NIGHT_LIGHT = [10, 10, 10]
EVENING_LIGHT = [150, 120, 110]
DAY_LIGHT = [255, 245, 235]


class Game(arcade.Window):
    def __init__(self):
        super().__init__()
        self.play_music = arcade.load_sound("C:/Users/Brotfresser/PycharmProjects/Manchkin/venv/Lib/site-packages/pygame/examples/data/house_lo.wav")
        self.bg_texture = "projects/database/DS_parody/floor.png"
        self.bg_list = arcade.SpriteList()

        self.light_layer = LightLayer(self.width, self.height)
        self.light_layer.light_now = DAY_LIGHT.copy()

        self.camera = arcade.Camera()

        self.mouse_light = Light(50, 50, mode="soft")
        self.light_layer.add(self.mouse_light)

        self.play_music.play(loop=True, volume=0.4)

        self.change_light_to = None
        self.is_change_light = False

        for x in range(0, 1000, 256):
            for y in range(0, 1000, 256):
                floor = arcade.Sprite(self.bg_texture, scale=0.5)
                floor.position = x, y
                self.bg_list.append(floor)

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            arcade.exit()

        elif symbol == arcade.key.KEY_1:
            self.change_light_to = DAY_LIGHT
            if self.light_layer.light_now > self.change_light_to:
                self.change_light_operation = "-"
            else:
                self.change_light_operation = "+"

            self.is_change_light = True

        elif symbol == arcade.key.KEY_2:
            self.change_light_to = EVENING_LIGHT
            if self.light_layer.light_now > self.change_light_to:
                self.change_light_operation = "-"
            else:
                self.change_light_operation = "+"

            self.is_change_light = True

        elif symbol == arcade.key.KEY_3:
            self.change_light_to = NIGHT_LIGHT
            if self.light_layer.light_now > self.change_light_to:
                self.change_light_operation = "-"
            else:
                self.change_light_operation = "+"

            self.is_change_light = True

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        self.mouse_light.position = x, y
        self.camera.move((x * 1.5 - 160, y * 1.5 - 160))

    def change_light(self):
        if self.change_light_operation == "-":
            if self.light_layer.light_now > self.change_light_to:
                for i in range(3):
                    if self.light_layer.light_now[i] > self.change_light_to[i]:

                        self.light_layer.light_now[i] -= 1

            else:
                self.is_change_light = False
        else:
            if self.light_layer.light_now < self.change_light_to:
                for i in range(3):
                    if self.light_layer.light_now[i] < self.change_light_to[i]:

                        self.light_layer.light_now[i] += 1

            else:
                self.is_change_light = False

    def update(self, delta_time: float):
        if self.is_change_light:
            self.change_light()
        self.camera.use()

    def on_draw(self):
        self.clear()
        with self.light_layer:
            self.bg_list.draw()
            arcade.draw_text("txt", 100, 100)
        self.light_layer.draw(ambient_color=self.light_layer.light_now)



a = Game()
arcade.run()

"""


"""***"""


"""  # Дешифратор по Цезарю
while True:
    new_text = ""
    text = input("1 - Зашифровать, 2 - Первичная расшифровать, 3 - Расшифровка с заданным смещением\n")

    if text == "1":  # Шифровка
        try:
            text = input("Введите текст:\n")
            offset = int(input("Введите смещение:\n"))

            new_text = [chr(ord(symbol) + offset) for symbol in text]
            
            new_text = "".join(new_text)
            print(new_text))

            input()
        except:
            print("Ошибка")

    elif text == "2":  # Расшифровка
        try:
            text = input("Введите текст:\n")
            min_offset = int(input("Введите минимально возможное смещение:\n"))
            max_offset = int(input("Введите максимально возможное смещение:\n"))

            for offset in range(min_offset, max_offset + 1):
                for symbol in text[:60]:
                    new_text += chr(ord(symbol) - offset)
                print(new_text)
                print("Смещение :", offset, "\n")
                new_text = ""

            input()
        except:
            print("Ошибка")

    elif text == "3":  # Полная расшифровка (с уже известным смещением)
        text = input("Введите текст:\n")
        offset = int(input("Введите смещение:\n"))

        new_text = [chr(ord(symbol) - offset) for symbol in text]
    
        new_text = "".join(new_text)
        print(new_text)

    else:
        print("Ошибка")
        input()
"""


"""***"""


"""  # Шифр Виженера (только английский)
message = input("Введите сообщение: ").lower()  # большие буквы кодировать невозможно
key = input("Введите ключ: ")

operator = int(input("0 - зашифровать, 1 - расшифровать: "))

special_count = 0  # счётчик особых символов

language_len_min = ord("a")
language_len_max = ord("z")

message2 = ""

for i, lit in enumerate(message):  # i - индекс буквы (это для ключа)
    if ord(lit) >= language_len_min:  # особые символы

        i -= special_count  # исключаем все особые символы
        i %= len(key)  # теперь индекс в пределах ключа

        offset = (ord(key[i]) - language_len_min)

        if operator:
            lit = ord(lit) - offset  # смещаем букву сообщения
        else:
            lit = ord(lit) + offset  # смещаем букву сообщения

        # если смещение вышло за пределы алфавита
        if lit > language_len_max:
            lit %= language_len_max
            lit += language_len_min - 1

        elif lit < language_len_min:
            lit += offset
            offset -= lit - language_len_min
            lit = language_len_max - offset + 1

        message2 += chr(lit)

    else:
        # если встречаются особые символы
        special_count += 1
        message2 += lit
        continue

print(message2)
"""
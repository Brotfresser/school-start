import arcade
import random

# Текстуры
CELL_CLOSED_TEXTURE = arcade.load_texture("cell_closed.png")
CELL_OPENED_PATH = "cell_opened_"
CELL_BOMB_TEXTURE = arcade.load_texture("cell_bomb.png")
CELL_FLAGGED_TEXTURE = arcade.load_texture("cell_flagged.png")

# Размер клетки
CELL_SPRITE_SIZE = 50  # Введите настоящий размер текстуры
CELL_SIZE = 50  # Каким он будет в игре
CELL_SPRITE_SCALE = CELL_SIZE / CELL_SPRITE_SIZE  # Формула масштаба

MAP_SIZE = "50 50".split()  # input("Введите размер поля через пробел:\n").split()
MAP_SIZE = list(map(int, MAP_SIZE))

MAP_RANGE_X = MAP_SIZE[0]
MAP_RANGE_Y = MAP_SIZE[1]

ALL_BOMBS = 400  # int(input("Введите кол-во бомб:\n"))

DEBUG_MODE = 1  # 0, 1, 2


class Cell(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__(scale=CELL_SPRITE_SCALE)
        self.bombs_around = 0
        self.type = "Пусто"  # Бомба, Пусто

        self.is_opened = False
        self.is_flagged = False
        self.checked = False
        self.check_again = True

        self.text = arcade.draw_text("0", self.center_x, self.center_y)

        self.center_x = x
        self.center_y = y

        self.log_txt = ""

        self.texture = CELL_CLOSED_TEXTURE

    def open(self):
        if not self.is_flagged:
            self.is_opened = True
            if self.type == "Бомба":
                self.texture = CELL_BOMB_TEXTURE

            else:
                self.texture = arcade.load_texture(CELL_OPENED_PATH+str(self.bombs_around)+".png")
                if not self.checked:
                    self.checked = True

                    if not self.bombs_around:
                        code = 'self.cell_list[cell_x + mod_x][cell_y + mod_y].open()'

                        window.cell_checking(self, code)
                        self.log_txt += "\n"

                else:
                    if self.check_again:
                        self.check_again = False
                        code = 'if self.cell_list[cell_x + mod_x][cell_y + mod_y].is_flagged: cell.check_again = True'

                        window.cell_checking(self, code)
                        self.log_txt += "\n"

                        if self.check_again:
                            self.check_again = False
                            code = 'if not self.cell_list[cell_x + mod_x][cell_y + mod_y].is_flagged'
                            code += ' and self.cell_list[cell_x + mod_x][cell_y + mod_y].check_again'
                            code += ' and not self.cell_list[cell_x + mod_x][cell_y + mod_y].type == "Бомба"'
                            code += ': self.cell_list[cell_x + mod_x][cell_y + mod_y].open()'

                            window.cell_checking(self, code)

                    else:
                        self.check_again = True

        if DEBUG_MODE:
            print(self.log_txt)

    def mark(self):
        if not self.is_opened:
            answer = ""
            if not self.is_flagged:
                self.texture = CELL_FLAGGED_TEXTURE
                self.is_flagged = True
            else:
                self.texture = CELL_CLOSED_TEXTURE
                self.is_flagged = False
                answer += "Флаг убран"

            if self.type == "Бомба":
                answer += "Есть бомба"
            else:
                answer += "Нет бомбы"

            return answer


class Game(arcade.Window):
    def __init__(self):
        super().__init__()
        self.cell_list = []
        self.flags_correct_count = 0

        self.camera = arcade.Camera()

    def on_draw(self):
        self.clear()
        self.camera.use()
        for cell_list_x in self.cell_list:  # Отрисовка клеток по х
            cell_list_x.draw()
        #print(self.camera.position)

    def setup(self):
        # Генерация клеток
        for x in range(CELL_SIZE // 2, MAP_RANGE_X * CELL_SIZE, CELL_SIZE):
            self.cell_list.append(arcade.SpriteList())

            for y in range(CELL_SIZE // 2, MAP_RANGE_Y * CELL_SIZE, CELL_SIZE):
                cell = Cell(x, y)
                self.cell_list[(x - CELL_SIZE // 2) // CELL_SIZE].append(cell)

        # Расстановка бомб
        for _ in range(ALL_BOMBS):
            rand_cell = random.choice(random.choice(self.cell_list))
            while rand_cell.type == "Бомба":  # Если случайная клетка уже - бомба
                rand_cell = random.choice(random.choice(self.cell_list))

            rand_cell.type = "Бомба"

        # Просчёт кол-ва бомб вокруг каждой клетки
        for cell_x in range(MAP_RANGE_X):
            for cell_y in range(MAP_RANGE_Y):
                cell = self.cell_list[cell_x][cell_y]
                cell.log_txt += f"{cell_x} {cell_y} - "

                code1 = 'if self.cell_list[cell_x + mod_x][cell_y + mod_y].type == "Бомба": '
                code1 += 'cell.bombs_around += 1; cell.log_txt += "success  "'

                code2 = 'if not self.cell_list[cell_x + mod_x][cell_y + mod_y].type == "Бомба":'
                code2 += 'cell.log_txt += "dont find  "'

                self.cell_checking(cell, code1, code2)

                cell.log_txt += f"{cell.center_x} {cell.center_y}\n"

        if DEBUG_MODE >= 2:  # Сразу открывает все клетки
            for cell_list_x in self.cell_list:
                for cell in cell_list_x:
                    cell.open()

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        x += self.camera.position[0]
        y += self.camera.position[1]
        convert_x_to_list_position = (x - CELL_SIZE // 2) / CELL_SIZE

        cell_clicked = arcade.get_sprites_at_point((x, y), self.cell_list[round(convert_x_to_list_position)])[0]

        print(x, y)
        if button == 1:
            cell_clicked.open()

        elif button == 4:
            answer = cell_clicked.mark()
            if "Есть бомба" in answer:
                if "Флаг убран" not in answer:
                    self.flags_correct_count += 1
                else:
                    self.flags_correct_count -= 1

            elif answer == "Нет бомбы":
                pass

            if DEBUG_MODE:
                print(self.flags_correct_count)

        elif button == 2 and x > self.width + self.camera.position[0] - 100:
            camera_x = self.camera.position[0]
            camera_y = self.camera.position[1]
            self.camera.move_to((camera_x + self.width, camera_y), 0.1)

        elif button == 2 and x < self.camera.position[0] + 100:
            camera_x = self.camera.position[0]
            camera_y = self.camera.position[1]
            self.camera.move_to((camera_x - self.width, camera_y), 0.1)

        elif button == 2 and y > self.height + self.camera.position[1] - 100:
            camera_x = self.camera.position[0]
            camera_y = self.camera.position[1]
            self.camera.move_to((camera_x, camera_y + self.height), 0.1)

        elif button == 2 and y < self.camera.position[1] + 100:
            camera_x = self.camera.position[0]
            camera_y = self.camera.position[1]
            self.camera.move_to((camera_x, camera_y - self.height), 0.1)

        if self.flags_correct_count == ALL_BOMBS:
            print("победа")
            arcade.exit()

    def cell_checking(self, cell, code1, code2=''):
        # Перевод в систему координат списка
        cell_x = int((cell.center_x - CELL_SIZE // 2) / CELL_SIZE)
        cell_y = int((cell.center_y - CELL_SIZE // 2) / CELL_SIZE)

        for mod_x in range(-1, 2):
            for mod_y in range(-1, 2):

                if cell_x + mod_x >= 0 and cell_y + mod_y >= 0:  # Чтобы не смотреть клетку по индексу -1
                    cell.log_txt += f"[{cell_x + mod_x}][{cell_y + mod_y}]-"

                    try:
                        exec(code1)
                        exec(code2)
                    except IndexError:
                        cell.log_txt += "nothing  "


if __name__ == "__main__":
    window = Game()
    window.setup()
    arcade.run()
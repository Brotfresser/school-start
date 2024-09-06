import arcade
from arcade.experimental.lights import LightLayer, Light
import random
from math import ceil

import items
import statics
import craft_system
import functions
# Добавить режим аттестации

DAY_LIGHT = [255, 245, 235]
EVENING_LIGHT = [160, 120, 110]
NIGHT_LIGHT = [1, 1, 1]
DAY = 1

PLAYER_SPEED = 5
PLAYER_SANITY = 200
PLAYER_HEALTH = 150
PLAYER_HUNGER = 150

TIME_TO_ANGLE = 80  # 80 или 10 (примерно 60 тиков в секунду)

MAP_SIZE_X = random.randint(-10000, -3000), random.randint(3000, 10000)
MAP_SIZE_Y = random.randint(-10000, -3000), random.randint(3000, 10000)
OBJECT_IN_LINE = random.randint(5, 20)


print("ПКМ - взаимодействовать с предметом в инвентаре, нажатие на колесо мыши - разделить предмет")
print("ходить - WASD, ЛКМ, меню крафта можно менять колесом мыши")
print("1,2,3 - установить время суток, F4 - остановить время")
print("/ - консольная команда")

FULL_SCREEN = False

THE_GAME = None  # ссылка на объект класса Game()
MAIN_MENU = None

ALL_VOLUME = 0.2


class InventoryCell(arcade.Sprite):  # ui
    def __init__(self, ui_position, item=None, cell_type=None, is_mouse_cell=False):
        super().__init__()
        self.texture = arcade.load_texture(f"ui/inventory icon_None.png")
        self.item = item

        self.type = cell_type  # None, Рука, Тело, Голова
        self.is_mouse_cell = is_mouse_cell

        self.ui_position = ui_position

    def update(self):
        if self.item is not None and not self.is_mouse_cell:
            # Чтобы предмет отображался в ячейке
            #try:
            self.item.position = self.position
            """except KeyError:
                print(self.item, self.item.type, self.item.position, self.position)"""

    def inventory_use(self):  # Перестановка предметов между текущей клетки и клетки мыши

        if self.item is not None:
            # Постановка предмета из этой ячейки в конец списка (чтобы он отображался поверх других)
            THE_GAME.items_inventory_list.remove(self.item)
            THE_GAME.items_inventory_list.append(self.item)

        mouse_item = THE_GAME.inventory[-1].item

        if self.item is not None and self.item + mouse_item:
            #print(f"{self.item.type}.{self.item.count} и {mouse_item.type}.{mouse_item.count} успешно сложились")
            pass
        else:  # Если хоть одно условие не соблюдено, то предметы просто меняются местами
            new_item = mouse_item

            if self.type is not None and new_item is not None and new_item.inventory_slot != self.type:
                # Если пытаются вставить предмет в неподходящую ячейку (траву в руки, кремень в голову)
                cell_index = THE_GAME.inventory.index(self)
                print(f"В ячейку {self.type} {cell_index} пытались положить неподходящий предмет {new_item.type} 2")
                THE_GAME.items_inventory_list.remove(new_item)
                THE_GAME.items_inventory_list.append(new_item)
            else:
                cell_old_item = self.item
                self.item = new_item
                THE_GAME.inventory[-1].item = cell_old_item

                if cell_old_item is not None and cell_old_item.inventory_slot is not None and cell_old_item.is_equipped:
                    cell_old_item.un_equip()
                if self.item is not None and self.item.inventory_slot == self.type and not self.item.is_equipped:
                    self.item.equip()

    def inventory_sort(self):  # Складирование части предметов по нажатии колеса мыши

        if not THE_GAME.inventory[-1].item and self.item is not None:  # Если слот мыши пустой
            # Разделение предмета пополам

            if self.item.count > 1:  # Не может произойти с особыми или надеваемыми предметами
                cell_count = self.item.count

                self.item.count = int(cell_count / 2)

                item_type = self.item.type
                item_count = int(cell_count / 2 + 0.5)

                mouse_cell = THE_GAME.inventory[-1]
                functions.set_cell_item(THE_GAME, mouse_cell, item_type, item_count)

        elif THE_GAME.inventory[-1].item is not None:  # Если слот мыши не пустой
            # Складирование единицы предмета
            mouse_cell = THE_GAME.inventory[-1]

            if not self.item:  # Если слот пустой

                if functions.set_cell_item(THE_GAME, self, mouse_cell.item):  # Если успешно положили в ячейку
                    if mouse_cell.item.count != 1:
                        mouse_cell.item.count -= 1
                    else:
                        mouse_cell.item = None

            elif self.item.type == mouse_cell.item.type:  # Если в слоте тот же предмет
                if self.item.count < self.item.max_count:
                    mouse_cell.item.count -= 1
                    self.item.count += 1

            try:
                if mouse_cell.item.count < 1:  # Удаление предмета
                    item = mouse_cell.item
                    THE_GAME.items_inventory_list.remove(item)
                    THE_GAME.inventory[-1].item = None
            except AttributeError:  # 'NoneType' object has no attribute 'count'
                """if functions.set_cell_item(THE_GAME, self, mouse_cell.item):  # Если успешно положили в ячейку
                        if mouse_cell.item.count != 1:
                            ...
                        else:
                            mouse_cell.item = None"""
                pass


class PlayerStatus:  # Значки, показывающие характеристики игрока (здоровье, голод, рассудок)
    def __init__(self, status_type):
        sprite_scale = 0.6

        self.type = status_type

        self.ui_position = 0, 0

        self.white_count = arcade.Text("", self.ui_position[0], self.ui_position[1], (255, 255, 255),
                                       font_size=22, font_name="bigdonstarve",
                                       anchor_x="center", anchor_y="center")
        self.black_count = arcade.Text("", self.ui_position[0], self.ui_position[1], (0, 0, 0),
                                       font_size=25, font_name="bigdonstarve",
                                       anchor_x="center", anchor_y="center")

        self.background = arcade.Sprite(scale=sprite_scale)
        self.main_sprite = arcade.Sprite(scale=sprite_scale)
        self.ring = arcade.Sprite(scale=sprite_scale)

        self.background.ui_position = self.ui_position
        self.main_sprite.ui_position = self.ui_position
        self.ring.ui_position = self.ui_position
        self.black_count.ui_position = self.ui_position
        self.white_count.ui_position = self.ui_position

    def status_check(self):
        player = THE_GAME.player
        status_percent = 100
        main_sprite_ui_position_mod = 0, 0

        if self.type == "hunger":
            status_percent = player.hunger / player.max_hunger * 100
            self.black_count.text = ceil(player.hunger)
            self.white_count.text = ceil(player.hunger)
        elif self.type == "health":
            status_percent = player.health / player.max_health * 100
            self.black_count.text = ceil(player.health)
            self.white_count.text = ceil(player.health)
        elif self.type == "sanity":
            status_percent = player.sanity / player.max_sanity * 100
            main_sprite_ui_position_mod = 0, -6
            self.black_count.text = ceil(player.sanity)
            self.white_count.text = ceil(player.sanity)

        back_index = ceil((100 - status_percent) / 4.55)
        main_index = ceil(status_percent / 25)

        try:
            if not THE_GAME.player.is_dead:
                self.main_sprite.texture = arcade.load_texture(f"ui/player_status/{self.type}/main_{main_index}.png")
                self.background.texture = arcade.load_texture(f"ui/player_status/{self.type}/background/Слой {back_index}.png")
        except FileNotFoundError:
            THE_GAME.player.is_dead = True
            arcade.Sound("sounds/player voice/player dead.mp3").play(volume=ALL_VOLUME)
            self.main_sprite.texture = arcade.load_texture("ui/player_status/health/main_1.png")
            self.background.texture = arcade.load_texture("ui/player_status/health/background/Слой 22.png")

        self.ring.texture = arcade.load_texture(f"ui/player_status/{self.type}/ring.png")

        self.background.ui_position = self.ui_position
        self.main_sprite.ui_position = (self.ui_position[0] + main_sprite_ui_position_mod[0],
                                        self.ui_position[1] + main_sprite_ui_position_mod[1])

        self.ring.ui_position = self.ui_position
        self.black_count.ui_position = self.ui_position[0] - 1, self.ui_position[1] - 1
        self.white_count.ui_position = self.ui_position


class Player(arcade.AnimatedWalkingSprite):
    def __init__(self):
        super().__init__()

        self.moving_by_mouse = False
        self.mouse_position = 0, 0

        self.position = 0, 0

        self.scale = 0.5

        self.is_dead = False

        self.max_sanity = 200
        self.sanity = PLAYER_SANITY

        self.max_health = 150
        self.health = PLAYER_HEALTH

        self.max_hunger = 150
        self.hunger = PLAYER_HUNGER

        self.science_craft_level = 0  # Находиться ли рядом с научной машиной/алхимической машиной
        self.magic_craft_level = 0  # Находиться ли рядом с шляпусником/теневым манипулятором
        self.already_craft_items_list = []
        self.crafted_statics_list = []  # Список объектов выделенных синим в крафте
        self.placed_now_static = None  # Объект, который игрок пытается разместить

        self.footseps_list = []
        self.last_step_sound = None
        for i in range(1, 4):
            sound = arcade.Sound(f"sounds/footstep_grass_{i}.mp3")
            self.footseps_list.append(sound)

        self.load_textures()

    def load_textures(self):  # Одноразовая загрузка всех анимаций

        for i in range(9, 19):  # Текстуры стояния
            texture_right = arcade.load_texture(f"standing/Слой {i}.png")
            texture_left = arcade.load_texture(f"standing/Слой {i}.png", mirrored=True)
            self.stand_right_textures.append(texture_right)
            self.stand_left_textures.append(texture_left)

        for i in range(20, 42):  # Текстуры ходьбы
            texture_right = arcade.load_texture(f"walking_left/Слой {i}.png", mirrored=True)
            texture_left = arcade.load_texture(f"walking_left/Слой {i}.png")
            self.walk_right_textures.append(texture_right)
            self.walk_left_textures.append(texture_left)

    def moving(self, symbol=None, key_pressed=True, mouse_position=None):

        if symbol is not None:  # Передвижение через клавиатуру
            self.moving_by_mouse = False
            THE_GAME.drag_mouse = False

            if key_pressed:  # Если кнопка нажата
                if symbol == arcade.key.W:
                    self.change_y = PLAYER_SPEED
                elif symbol == arcade.key.S:
                    self.change_y = -PLAYER_SPEED
                elif symbol == arcade.key.D:
                    self.change_x = PLAYER_SPEED
                elif symbol == arcade.key.A:
                    self.change_x = -PLAYER_SPEED
            else:  # Если кнопку отпустили
                if symbol == arcade.key.W or symbol == arcade.key.S:
                    self.change_y = 0
                elif symbol == arcade.key.D or symbol == arcade.key.A:
                    self.change_x = 0

        elif self.moving_by_mouse:  # Передвижение через мышь
            for tab in THE_GAME.ui_sprites["craft_tabs"]:  # Закрытие всех вкладок крафтов
                if tab.is_open:
                    tab.tab_clicked()

            self.mouse_position = mouse_position

            mouse_x = self.mouse_position[0]
            mouse_y = self.mouse_position[1]

            if mouse_x > self.center_x:
                self.change_x = PLAYER_SPEED
            elif mouse_x < self.center_x:
                self.change_x = -PLAYER_SPEED

            if mouse_y > self.bottom:
                self.change_y = PLAYER_SPEED
            elif mouse_y < self.bottom:
                self.change_y = -PLAYER_SPEED

            # Если игрок в промежутке места, где была нажата мышь
            if mouse_x - 5 < self.center_x < mouse_x + 5:
                self.change_x = 0
            if mouse_y - 5 < self.bottom < mouse_y + 5:
                self.change_y = 0

            if not self.change_x and not self.change_y:  # Если в обоих промежутках (достиг точки назначения)
                self.moving_by_mouse = False

        elif not self.moving_by_mouse:
            self.moving_by_mouse = True
            self.mouse_position = mouse_position

    def update(self, delta_time: float = 1 / 60):
        if not self.is_dead:
            self.center_x += self.change_x
            self.center_y += self.change_y

            if self.moving_by_mouse:
                self.moving(mouse_position=self.mouse_position)

            if self.change_x != 0 or self.change_y != 0:
                if not THE_GAME.timer_on:  # Звуки шагов
                    if self.last_step_sound is None:
                        self.last_step_sound = random.choice(self.footseps_list)

                    while True:  # Генерация звука, не совпадающего с предыдущим
                        step_sound = random.choice(self.footseps_list)
                        if step_sound is not self.last_step_sound:
                            break
                    self.last_step_sound = step_sound
                    once_code = f"self.sounds_player(self.player.last_step_sound, sound_volume=0.05)"
                    THE_GAME.timer(18, once_code)


class Game(arcade.View):
    def __init__(self):
        super().__init__()
        # Спрайты
        self.all_craft_tabs_sprite = arcade.Sprite("UI/craft/all craft tabs sprite.png")
        self.craft_recipe_sprite = arcade.Sprite("UI/craft/craft recipe.png")
        self.craft_recipe_sprite.cell_list = []  # Список клеток для рецепта крафта
        self.inventory_background_sprite = arcade.Sprite("ui/inventory.png")
        self.day_cycle = arcade.Sprite("UI/day cycle.png", scale=1.35)  # Значок времени
        self.time_cycle_meter = arcade.Sprite("UI/time cycle meter.png", scale=1.2)  # Стрелка времени

        self.day = DAY

        # Свет
        self.light_layer = LightLayer(main_window.width, main_window.height)  # Свет мира
        self.light_layer.light_now = DAY_LIGHT.copy()  # Оттенок света

        self.player_light_1 = Light(0, 0, 250, (0, 0, 0), "soft")  # (170, 150, 130)
        self.player_light_2 = Light(0, 0, 500, (0, 0, 0), "soft")  # (4, 4, 4)
        self.craft_static_light = Light(0, 0, color=(0, 0, 0), mode="soft")

        self.light_layer.add(self.player_light_1)
        self.light_layer.add(self.player_light_2)
        self.light_layer.add(self.craft_static_light)

        self.change_light_on = False  # Изменить время суток, или нет
        self.change_light_to = None  # На какое время суток изменить

        # Звуки
        self.sound_player_is_playing = False  # Работает ли функция sounds_player
        self.playable_sounds_list = None  # Список звуков, которые функция должна сыграть
        self.playable_sounds_volume = None
        self.playable_sounds_id = None  # id текущего звука в списке
        self.sounds_player_value = None

        self.player_voice_list = []
        for i in range(1, 11):
            player_voice = arcade.Sound(f"sounds/player voice/player voice_{i}.mp3")
            self.player_voice_list.append(player_voice)
        else:
            player_voice = arcade.Sound(f"sounds/player voice/player voice_end.mp3")
            self.player_voice_list.append(player_voice)
        self.music_list =[]
        for i in range(2):
            music = arcade.Sound(f"music/{i}.mp3")
            self.music_list.append(music)

        # Игрок
        self.player = Player()
        # здесь будет описываться реакция и мнение персонажа на событие или предмет
        self.player_text = arcade.Text("", self.player.center_x, self.player.center_y, (220, 220, 220),
                                       anchor_x="center", anchor_y="bottom", align="center",
                                       font_size=26, font_name="bigdonstarve", multiline=True, width=460)
        self.player_text_black = arcade.Text("", self.player.center_x, self.player.center_y, (0, 0, 0),
                                       anchor_x="center", anchor_y="bottom", align="center",
                                       font_size=26, font_name="bigdonstarve", multiline=True, width=460)

        # Прочие спрайты
        self.floor_list = arcade.SpriteList()

        # Некоторые списки
        self.static_list = arcade.SpriteList()  # Деревья, кусты и т.д.
        self.static_updating_list = arcade.SpriteList()  # Деревья, кусты и всё, что нужно обновлять
        self.statics_aura_list = arcade.SpriteList()  # Ауры статиков
        self.outside_items_list = arcade.SpriteList()  # Предметы во всём мире
        self.inventory = arcade.SpriteList()  # Список с клетками инвентаря
        self.items_inventory_list = arcade.SpriteList()  # Предметы, которые находятся в инвентаре
        self.is_chosen_craft_recipes_sprite = False
        self.player_status_list = []  # Статусы игрока
        self.food_list = []  # Список всей еды, которая будет портиться

        vars = list(self.__dict__)

        for var in vars:
            if isinstance(self.__dict__[var], arcade.SpriteList):
                self.__dict__[var].type = var

        # Мышь
        self.mouse_x = 0  # координата мыши по x
        self.mouse_y = 0  # координата мыши по y
        self.drag_mouse = False  # Позволяет изменять mouse_x и mouse_y, если активна (нужна для ходьбы через мышь)

        self.chosen_by_mouse_item_inventory = None  # Предмет в инвентаре, на который навели мышью
        self.chosen_by_mouse_item = None  # Предмет снаружи на который навели мышью
        self.chosen_by_mouse_craft = None  # Крафт, на который навели мышью
        self.last_chosen_by_mouse_craft = None  # Последний крафт, на который навели мышью
        self.chosen_by_mouse_static = None
        self.chosen_by_mouse_status = None  # Статус игрока, на который навели мышью
        self.chosen_by_mouse_light_ui = None  # Иконка смена дня и ночи (часов)

        self.mouse_player_task = None  # Объект, к которому идёт игрок

        # Таймер
        self.timer_on = False  # Включить таймер
        self.timer_time = 0
        self.timer_limit = 0
        self.repeat_code = None
        self.at_end_code = None
        self.timer2_on = False  # Включить таймер
        self.timer2_time = 0
        self.timer2_limit = 0
        self.repeat_code2 = None
        self.at_end_code2 = None
        self.time_go = True

        # Прочее
        self.time_meter = 0  # Текущее время (используется для изменения градусной стрелки)
        self.global_game_time = 0  # Текущее время (использовать это)
        self.camera = arcade.Camera()

        # ui (перенесены в setup())
        self.ui_sprites = arcade.Scene()

        self.player_status_sanity = None
        self.player_status_hunger = None
        self.player_status_health = None

        # Добавление в self.ui_sprites (перенесено в setup() )

    def on_draw(self):
        with self.light_layer:
            self.floor_list.draw()
            self.outside_items_list.draw()
            self.static_list.draw()

            if self.player.placed_now_static is not None:
                self.player.placed_now_static.draw()
            if not self.player.is_dead:
                self.player.draw()

        self.light_layer.draw(ambient_color=self.light_layer.light_now)

        camera_x = self.camera.position[0]
        camera_y = self.camera.position[1]

        # ui
        for sprite in self.ui_sprites["all_ui"]:
            sprite.center_x = camera_x + sprite.ui_position[0]
            sprite.center_y = camera_y + sprite.ui_position[1]

        # Добавлены отдельно сюда, чтобы не отображаться поверх меню крафта
        self.all_craft_tabs_sprite.center_x = camera_x + self.all_craft_tabs_sprite.ui_position[0]
        self.all_craft_tabs_sprite.center_y = camera_y + self.all_craft_tabs_sprite.ui_position[1]
        self.all_craft_tabs_sprite.draw()
        self.ui_sprites["craft_tabs_background"].draw()

        for tab in self.ui_sprites["craft_tabs"]:  # Крафты из вкладок крафта (например факел из вкладки Свет)
            if tab.is_open:
                for sprite in tab.all_crafts_spritelist:
                    sprite.center_x = camera_x + sprite.ui_position[0]
                    sprite.center_y = camera_y + sprite.ui_position[1]
                    sprite.draw()
            else:
                for sprite in tab.all_crafts_spritelist:
                    sprite.center_x = main_window.width + 500
                    sprite.center_y = main_window.height + 500
        for craft_recipe_sprite in self.ui_sprites["craft_recipe_sprite"]:
            craft_recipe_sprite.center_x = craft_recipe_sprite.ui_position[0] + camera_x
            craft_recipe_sprite.center_y = craft_recipe_sprite.ui_position[1] + camera_y
        self.ui_sprites.draw()

        # Отрисовка клеток инвентаря
        for cell in self.inventory:
            cell.position = camera_x + cell.ui_position[0], camera_y + cell.ui_position[1]
            cell.update()
        self.inventory.draw()
        self.items_inventory_list.draw()

        # Текст иконок статуса (голод, здоровье, рассудок)
        for status in self.player_status_list:
            status.black_count.position = (camera_x + status.black_count.ui_position[0],
                                           camera_y + status.black_count.ui_position[1])

            status.white_count.position = (camera_x + status.white_count.ui_position[0],
                                           camera_y + status.white_count.ui_position[1])
            # status.black_count.draw()
            # status.white_count.draw()

        # Счётчики над статусами игрока
        if self.chosen_by_mouse_status is not None:
            self.chosen_by_mouse_status.black_count.draw()
            self.chosen_by_mouse_status.white_count.draw()

        # ui Текст
        for item in self.items_inventory_list:  # Отрисовка кол-ва предметов в каждой ячейке
            if not item.max_count == 1:  # (числа почему-то дрожат, иногда)
                arcade.draw_text(f"{item.count}", item.center_x - 1, item.center_y + 15, (0, 0, 0),
                                 anchor_x="center", anchor_y="center", align="center",
                                 multiline=True, width=100,
                                 font_size=24, font_name="bigdonstarve")
                arcade.draw_text(f"{item.count}", item.center_x - 2, item.center_y + 15, (255, 255, 255),
                                 anchor_x="center", anchor_y="center", align="center",
                                 multiline=True, width=100,
                                 font_size=22, font_name="bigdonstarve")

            if item.durability is not None and item.max_durability != 0:
                durability_percent = int(item.durability / (item.max_durability / 100))
                arcade.draw_text(f"{durability_percent}%", item.center_x - 2, item.center_y - 12, (0, 0, 0),
                                 anchor_x="center", anchor_y="center", align="center",
                                 multiline=True, width=100,
                                 font_size=20, font_name="bigdonstarve")
                arcade.draw_text(f"{durability_percent}%", item.center_x - 1, item.center_y - 11, (255, 255, 255),
                                 anchor_x="center", anchor_y="center", align="center",
                                 multiline=True, width=100,
                                 font_size=18, font_name="bigdonstarve")

        if self.chosen_by_mouse_item_inventory:  # Название и возможные действия предмета, на который навели мышью
            item = self.chosen_by_mouse_item_inventory
            item_description = item.name

            item_description += "\n"
            if item.is_in_inventory:

                if item.is_activating:
                    item_description += "активировать"
                elif item.is_food:
                    item_description += "съесть"
                else:
                    item_description += "осмотреть"
            else:
                item_description += "выбросить"

            # Чёрный текст
            arcade.draw_text(f"{item_description}",
                             self.mouse_x + camera_x - 22,
                             self.mouse_y + camera_y + 38,
                             (0, 0, 0),
                             font_size=25, font_name="bigdonstarve", align="center", width=100)
            # Белый текст
            arcade.draw_text(f"{item_description}",
                             self.mouse_x + camera_x - 20,
                             self.mouse_y + camera_y + 40,
                             (255, 255, 255),
                             font_size=25, font_name="bigdonstarve", align="center", width=100)

        elif self.chosen_by_mouse_item:
            item = self.chosen_by_mouse_item
            item_description = item.name
            if item.count > 1:
                item_description += " " + str(item.count) + "x"
            item_description += "\nПодобрать"

            # Чёрный текст
            arcade.draw_text(f"{item_description}",
                             self.mouse_x + camera_x - 22,
                             self.mouse_y + camera_y + 46,
                             (0, 0, 0),
                             font_size=25, font_name="bigdonstarve", align="center", width=100)
            # Белый текст
            arcade.draw_text(f"{item_description}",
                             self.mouse_x + camera_x - 20,
                             self.mouse_y + camera_y + 48,
                             (255, 255, 255),
                             font_size=25, font_name="bigdonstarve", align="center", width=100)

        elif self.chosen_by_mouse_static:  # Название и действия со статичным объектом, на который навели мышью
            static = self.chosen_by_mouse_static

            if static.is_empty or not static.is_can_grow:
                static_description = f"Осмотреть {static.name}"
            else:
                static_description = static.activating_description

            # Чёрный текст
            arcade.draw_text(f"{static_description}",
                             self.mouse_x + camera_x - 3,
                             self.mouse_y + camera_y + 35 - 3,
                             (0, 0, 0),
                             font_size=26, font_name="bigdonstarve",
                             anchor_x="center", anchor_y="center", align="center",
                             multiline=True, width=400)
            # Белый текст
            arcade.draw_text(f"{static_description}",
                             self.mouse_x + camera_x,
                             self.mouse_y + camera_y + 35,
                             (255, 255, 255),
                             font_size=26, font_name="bigdonstarve",
                             anchor_x="center", anchor_y="center", align="center",
                             multiline=True, width=400)

        elif self.chosen_by_mouse_craft or self.is_chosen_craft_recipes_sprite:  # Навели мышью на крафт
            try:
                if self.chosen_by_mouse_craft:
                    self.last_chosen_by_mouse_craft = self.chosen_by_mouse_craft

                self.craft_recipe_sprite.center_x = self.last_chosen_by_mouse_craft.center_x + 230
                self.craft_recipe_sprite.center_y = self.last_chosen_by_mouse_craft.center_y
                self.craft_recipe_sprite.draw()

                # craft_x | y это центр для ячеек рецепта крафта
                craft_x = self.craft_recipe_sprite.center_x + 40
                craft_y = self.craft_recipe_sprite.top - 135

                craft = self.last_chosen_by_mouse_craft
                # craft_recipe - полный рецепт предмета
                craft_recipe = craft.type["tab"].all_crafts[craft.type["subtype"]["item"]]["рецепт"]
                cell_list = []  # Список с клетками, показывающими рецепт крафта
                items_sprite_list = arcade.SpriteList()  # Список предметов в клетках, нужных для крафта

                for cell in self.craft_recipe_sprite.cell_list:
                    cell_list.append(cell)  # Клетки на старте всё равно пустые, не обращайте внимание

                if len(craft_recipe) == 1:  # Если в рецепте нужен всего лишь 1 предмет
                    cell_list[0].position = craft_x, craft_y

                    cell_list[0].draw()

                elif len(craft_recipe) == 2:
                    cell_list[0].position = craft_x - 35, craft_y
                    cell_list[1].position = craft_x + 35, craft_y

                    cell_list[0].draw()
                    cell_list[1].draw()
                elif len(craft_recipe) == 3:
                    cell_list[0].position = craft_x, craft_y
                    cell_list[1].position = craft_x - 75, craft_y
                    cell_list[2].position = craft_x + 75, craft_y

                    cell_list[0].draw()
                    cell_list[1].draw()
                    cell_list[2].draw()

                for i, recipe_item in enumerate(craft_recipe):  # Заполнение списка нужных для крафта предметов
                    item = arcade.Sprite(f"items/{recipe_item[0]}.png")
                    # item.texture = arcade.load_texture(f"items/{craft[0]}.png") - слишком нагружает комп
                    item.position = cell_list[i].position
                    item.text_black = arcade.Text(f"0/{recipe_item[1]}",
                                 item.center_x - 2, item.center_y - 38, (40, 0, 0),
                                 font_size=20, font_name="bigdonstarve",
                                 anchor_x="center", anchor_y="center", align="center",
                                 multiline=True, width=100)
                    item.text_white = arcade.Text(f"0/{recipe_item[1]}",
                                            item.center_x, item.center_y - 35, (250, 40, 65),
                                            font_size=20, font_name="bigdonstarve",
                                            anchor_x="center", anchor_y="center", align="center",
                                            multiline=True, width=100)
                    items_sprite_list.append(item)

                # Есть ли предметы для крафта у игрока
                inventory_outside_items_list = functions.player_items_in_inventory(THE_GAME)
                for i, recipe_item in enumerate(craft_recipe):

                    if recipe_item[0] in inventory_outside_items_list:
                        # Если предмет есть, то пишем, сколько именно и сколько нужно
                        inventory_item_count = inventory_outside_items_list[recipe_item[0]]
                        items_sprite_list[i].text_black.text = f"{inventory_item_count}/{recipe_item[1]}"
                        items_sprite_list[i].text_white.text = f"{inventory_item_count}/{recipe_item[1]}"

                    # Проверка, есть ли предметы у игрока в нужном кол-ве
                    if functions.is_items_in_inventory(THE_GAME, recipe_item):  # Если есть
                        items_sprite_list[i].text_white.color = (255, 255, 255)

                        cell_list[i].texture = arcade.load_texture("UI/inventory icon_None.png")
                        cell_list[i].scale = 1.45
                    else:
                        items_sprite_list[i].text_white.color = (250, 40, 65)
                        cell_list[i].texture = arcade.load_texture("UI/craft/inventory cell_miss.png")
                        cell_list[i].scale = 1

                items_sprite_list.draw()
                for item in items_sprite_list:
                    item.text_black.draw()
                    item.text_white.draw()

                # Название предмета, который пытаются скрафтить

                # Чёрный текст
                arcade.draw_text(f"{self.last_chosen_by_mouse_craft.type['subtype']['name']}",
                                 craft_x - 3,
                                 craft_y + 67,
                                 (0, 0, 0),
                                 font_size=34, font_name="bigdonstarve",
                                 anchor_x="center", anchor_y="center", align="center",
                                 multiline=True, width=400)
                # Белый текст
                arcade.draw_text(f"{self.last_chosen_by_mouse_craft.type['subtype']['name']}",
                                 craft_x,
                                 craft_y + 70,
                                 (255, 255, 255),
                                 font_size=34, font_name="bigdonstarve",
                                 anchor_x="center", anchor_y="center", align="center",
                                 multiline=True, width=400)
            except AttributeError:
                # Иногда, если мышью быстро переместиться между крафтом и craft_recipe_sprite, то craft_recipe_sprite
                # не успеет переместиться за экран, в итоге chosen_by_mouse_craft is None и конец кода
                print("AttributeError")

        elif not self.chosen_by_mouse_craft and not self.is_chosen_craft_recipes_sprite:
            for cell in self.craft_recipe_sprite.cell_list:
                cell = arcade.Sprite("UI/craft/inventory cell_miss.png")

        if not self.chosen_by_mouse_light_ui:
            # Чёрный текст
            arcade.draw_text(f"День: {self.day}", self.day_cycle.center_x - 3, self.day_cycle.center_y - 3, (0, 0, 0),
                             font_size=29, font_name="bigdonstarve",
                             anchor_x="center", anchor_y="center")
            # Белый текст
            arcade.draw_text(f"День: {self.day}", self.day_cycle.center_x, self.day_cycle.center_y, (255, 255, 255),
                             font_size=29, font_name="bigdonstarve",
                             anchor_x="center", anchor_y="center")

        self.player_text.x = self.player.center_x
        self.player_text.y = self.player.center_y + 40
        self.player_text_black.x = self.player_text.x - 2
        self.player_text_black.y = self.player_text.y - 2

        self.player_text_black.draw()
        self.player_text.draw()

    def on_update(self, delta_time: float):
        self.player.update()
        self.player.update_animation()
        self.player_light_1.position = self.player.position
        self.player_light_2.position = self.player.position

        def mouse_select_object():  # Определение, на какой именно объект навели мышью
            mouse_x = self.camera.position[0] + self.mouse_x
            mouse_y = self.camera.position[1] + self.mouse_y

            mouse_pos = mouse_x, mouse_y

            # Если навёл мышью на объект
            selected_item_inventory = arcade.get_sprites_at_point(mouse_pos, self.items_inventory_list)
            selected_item = arcade.get_sprites_at_point(mouse_pos, self.outside_items_list)
            selected_static = arcade.get_sprites_at_point(mouse_pos, self.static_list)
            selected_light_ui = arcade.get_sprites_at_point(mouse_pos, self.ui_sprites["day_cycle"])
            selected_craft_recipes_sprite = arcade.get_sprites_at_point(mouse_pos,
                                                                        self.ui_sprites["craft_recipe_sprite"])
            for tab in self.ui_sprites["craft_tabs"]:
                selected_craft = arcade.get_sprites_at_point((mouse_x, mouse_y), tab.all_crafts_spritelist)
                if selected_craft:
                    selected_craft = (selected_craft[0], tab)
                    break
            # selected_tab_sprite и selected_tab перенесены в on_mouse_scroll
            self.chosen_by_mouse_item_inventory = None
            self.chosen_by_mouse_item = None
            self.chosen_by_mouse_static = None
            self.chosen_by_mouse_craft = None
            self.chosen_by_mouse_light_ui = None
            self.is_chosen_craft_recipes_sprite = False

            if selected_craft or selected_craft_recipes_sprite:  # Крафт, на который навели мышью
                if selected_craft_recipes_sprite:
                    self.is_chosen_craft_recipes_sprite = True
                else:
                    selected_craft = selected_craft[0]
                    if selected_craft.type["type"] == "craft" or selected_craft.type["type"] == "background":
                        self.chosen_by_mouse_craft = selected_craft

            else:
                if selected_item_inventory:  # Предмет в инвентаре, на который навели мышью
                    self.chosen_by_mouse_item_inventory = selected_item_inventory[0]
                    if self.inventory[-1].item is not None:  # Если предмет держит мышь
                        self.chosen_by_mouse_item_inventory.is_in_inventory = False
                    else:
                        self.chosen_by_mouse_item_inventory.is_in_inventory = True

                elif selected_item:
                    self.chosen_by_mouse_item = selected_item[0]
                elif selected_static:
                    self.chosen_by_mouse_static = selected_static[0]
                elif selected_light_ui:
                    self.chosen_by_mouse_light_ui = selected_light_ui[0]

        mouse_select_object()

        if self.time_go:
            self.time_cycle()  # Главные игровые часы для смены времени суток, статистики игрока и пр.

        for status in self.player_status_list:  # Проверка характеристик игрока
            status.status_check()

        for static in self.static_list:
            static.update(static)

        for aura in self.statics_aura_list:
            aura.position = aura.static.position
            collide_aura = arcade.check_for_collision(self.player, aura)
            if collide_aura:
                aura.is_collide = True
                aura.static.aura_enter(aura.static, THE_GAME)

            elif aura.is_collide:
                aura.is_collide = False
                aura.static.aura_leave(aura.static, THE_GAME)


        if self.timer_on:
            self.timer()
        if self.timer2_on:
            self.timer2()
        if self.change_light_on:  # Плавное освещения
            self.change_light()
        if self.sound_player_is_playing:
            self.sounds_player()

        if self.drag_mouse:  # Перемещение через мышь
            mouse_position = (self.mouse_x + self.camera.position[0], self.mouse_y + self.camera.position[1])
            self.player.moving(mouse_position=mouse_position)
        elif self.mouse_player_task and not self.player.moving_by_mouse:
            if self.mouse_player_task[1] == "pickup_item":
                self.mouse_player_task[0].pickup_item()
            elif self.mouse_player_task[1] == "static_activating":
                if len(self.mouse_player_task[0].variables_send_to_func) > 1:
                    self.mouse_player_task[0].static_activating(*self.mouse_player_task[0].variables_send_to_func)
                else:
                    self.mouse_player_task[0].static_activating()
            self.mouse_player_task = None

        self.camera_using()  # Перемещение камеры к игроку

        # ui, на который навели мышью
        mouse_position = (self.mouse_x + self.camera.position[0], self.mouse_y + self.camera.position[1])
        selected_status = arcade.get_sprites_at_point(mouse_position, self.ui_sprites["player_status"])
        if selected_status:  # Статусы игрока
            selected_status = selected_status[0]

            for status in self.player_status_list:
                # Проверка, какой это статус
                if status.background == selected_status or status.main_sprite == selected_status:
                    self.chosen_by_mouse_status = status
                    break
        else:
            self.chosen_by_mouse_status = None

    def setup(self):
        for _ in range(3):
            cell = arcade.Sprite("UI/craft/inventory cell_miss.png")
            self.craft_recipe_sprite.cell_list.append(cell)

        # Статистика игрока
        self.player_status_sanity = PlayerStatus("sanity")
        self.player_status_hunger = PlayerStatus("hunger")
        self.player_status_health = PlayerStatus("health")

        self.player_status_list.append(self.player_status_sanity)
        self.player_status_list.append(self.player_status_hunger)
        self.player_status_list.append(self.player_status_health)

        # Вкладки крафта
        instruments_craft_tab = craft_system.CraftTab("Инструменты", THE_GAME)
        light_craft_tab = craft_system.CraftTab("Свет", THE_GAME)
        science_craft_tab = craft_system.CraftTab("Наука", THE_GAME)

        self.ui_sprites.add_sprite("craft_tabs", instruments_craft_tab)
        self.ui_sprites.add_sprite("craft_tabs", light_craft_tab)
        self.ui_sprites.add_sprite("craft_tabs", science_craft_tab)

        # местоположение на экране (кроме крафтов)
        self.craft_recipe_sprite.ui_position = main_window.width + 500, main_window.height + 500
        self.inventory_background_sprite.ui_position = main_window.width // 2, 35
        self.all_craft_tabs_sprite.ui_position = 37, main_window.height // 2

        self.day_cycle.ui_position = main_window.width - 140, main_window.height - 100
        self.time_cycle_meter.ui_position = self.day_cycle.ui_position

        self.player_status_sanity.ui_position = self.day_cycle.ui_position[0], self.day_cycle.ui_position[1] - 195
        self.player_status_health.ui_position = self.day_cycle.ui_position[0] + 50, self.day_cycle.ui_position[1] - 110
        self.player_status_hunger.ui_position = (self.player_status_health.ui_position[0] - 100,
                                                 self.player_status_health.ui_position[1])

        # Добавление всех ui в self.ui_sprites
        self.ui_sprites.add_sprite("craft_tabs_background", arcade.Sprite("empty sprite.png"))
        # Добавление пустого спрайта чтобы craft_tabs_background не отображались последними поверх других

        for status in self.player_status_list:
            self.ui_sprites.add_sprite("player_status", status.background)
            self.ui_sprites.add_sprite("player_status", status.main_sprite)
            self.ui_sprites.add_sprite("player_status", status.ring)

        self.ui_sprites.add_sprite("day_cycle", self.day_cycle)
        self.ui_sprites.add_sprite("day_cycle", self.time_cycle_meter)

        # self.ui_sprites.add_sprite("all_ui", self.all_craft_tabs_sprite) (перенесён в on_draw())
        self.ui_sprites.add_sprite("craft_recipe_sprite", self.craft_recipe_sprite)
        self.ui_sprites.add_sprite("all_ui", self.inventory_background_sprite)
        for player_status in self.ui_sprites["player_status"]:  # Иконки статусов
            self.ui_sprites.add_sprite("all_ui", player_status)
        for day_cycle in self.ui_sprites["day_cycle"]:  # Игровые часы
            self.ui_sprites.add_sprite("all_ui", day_cycle)
        for y, tab in enumerate(self.ui_sprites["craft_tabs"]):  # Крафты

            tab.ui_position = (self.all_craft_tabs_sprite.ui_position[0] - 10,
                               self.all_craft_tabs_sprite.ui_position[1] + 340 - y * 60)
            tab.setup()
            self.ui_sprites.add_sprite("all_ui", tab.tab_background)
            self.ui_sprites.add_sprite("craft_tabs_background", tab.tab_background)
            self.ui_sprites.add_sprite("all_ui", tab)

        # Генерация пола
        for x in range(*MAP_SIZE_X, 256):
            for y in range(*MAP_SIZE_Y, 256):
                texture = arcade.Sprite("floor.png", scale=1.9)
                texture.center_x = x
                texture.center_y = y

                self.floor_list.append(texture)

        # Генерация клеток инвентаря
        for i, x in enumerate(range(50, 1040, 55)):
            inventory_background_sprite_left_ui_position = (main_window.width - 1075) / 2
            cell = InventoryCell((inventory_background_sprite_left_ui_position + x + (i // 5 * 13), 28))
            self.inventory.append(cell)
        else:
            self.inventory[-3].type = "Рука"
            self.inventory[-2].type = "Тело"
            self.inventory[-1].type = "Голова"
            for cell_id in range(-3, 0):
                cell = self.inventory[cell_id]
                cell.ui_position = (cell.ui_position[0] - 2, cell.ui_position[1])
                self.inventory[cell_id].texture = arcade.load_texture(f"UI/inventory icon_{cell.type}.png")

            cell = InventoryCell((main_window.width + 30, 27), is_mouse_cell=True)
            self.inventory.append(cell)

        max_types = 4
        max_types += 1
        # Генерация всякого
        for y in range(*MAP_SIZE_Y, 200):
            for object_type, x in enumerate(range(OBJECT_IN_LINE)):
                if object_type % max_types == 0:
                    created_object = statics.Static("саженец", THE_GAME)
                    self.static_list.append(created_object)

                elif object_type % max_types == 1:
                    created_object = items.Item(f"цветок_1", THE_GAME)
                    self.outside_items_list.append(created_object)

                elif object_type % max_types == 2:
                    created_object = statics.Static("ягодный куст", THE_GAME)
                    self.static_list.append(created_object)
                elif object_type % max_types == 3:
                    created_object = statics.Static("трава", THE_GAME)
                    self.static_list.append(created_object)
                elif object_type % max_types == 4:
                    created_object = items.Item("кремень", THE_GAME)
                    self.outside_items_list.append(created_object)

                created_object.center_x = random.randint(*MAP_SIZE_X)
                created_object.center_y = y + random.randint(-100, 100)

                # Если созданный объект касается других, то он удаляется
                if functions.check_for_collision(THE_GAME, created_object):

                    functions.delete_object_outside(THE_GAME, created_object)

    def console_command_exec(self, console_command):  # вызывается в MAIN_MENU
        code = console_command
        if "giveme" in code:
            code = code.replace("giveme ", "")
            code = code.split()
            item = items.Item(code[0], THE_GAME, int(code[1]), True)
            functions.append_item(THE_GAME, item)
        elif "setcell" in code:
            code = code.replace("setcell ", "")
            code = code.split()
            functions.set_cell_item(THE_GAME, int(code[0]), code[1], int(code[2]))
        elif "increase" in code:
            code = code.replace("increase ", "")
            code = code.split()
            functions.increase_status(code[0], int(code[1]), THE_GAME)
        else:
            exec(code)

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:  # Выход
            main_window.show_view(MAIN_MENU)
            MAIN_MENU.game_pause()

        elif symbol == arcade.key.LALT:
            main_window.show_view(MAIN_MENU)
            MAIN_MENU.open_console()

        elif symbol == 46 or symbol == 47:  # / - кнопка
            print("Консоль: giveme, setcell, increase")
            code = input()
            if "giveme" in code:
                code = code.replace("giveme ", "")
                code = code.split()
                item = items.Item(code[0], THE_GAME, int(code[1]), True)
                functions.append_item(THE_GAME, item)
            elif "setcell" in code:
                code = code.replace("setcell ", "")
                code = code.split()
                functions.set_cell_item(THE_GAME, int(code[0]), code[1], int(code[2]))
            elif "increase" in code:
                code = code.replace("increase ", "")
                code = code.split()
                functions.increase_status(code[0], int(code[1]), THE_GAME)
            else:
                exec(code)

        elif symbol == arcade.key.TAB:
            print(self.player.science_craft_level)

        elif symbol == arcade.key.CAPSLOCK:
            sounds_list = []
            for i in range(11):
                sounds_list.append(self.player_voice_list[i])
            else:
                sounds_list.append(self.player_voice_list[-1])
                self.sounds_player(*sounds_list)

        elif symbol == arcade.key.F4:
            self.time_go = not self.time_go

        elif symbol == arcade.key.KEY_1:
            self.change_light_to = DAY_LIGHT
            self.change_light_on = True

        elif symbol == arcade.key.KEY_2:
            self.change_light_to = EVENING_LIGHT
            self.change_light_on = True

        elif symbol == arcade.key.KEY_3:
            self.change_light_to = NIGHT_LIGHT
            self.change_light_on = True

        else:  # Если WASD - ходьба через клавиатуру
            self.mouse_player_task = None
            self.player.moving(symbol)

    def on_key_release(self, symbol: int, modifiers: int):
        self.player.moving(symbol, False)

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        mouse_x = self.camera.position[0] + x
        mouse_y = self.camera.position[1] + y

        selected_cell = arcade.get_sprites_at_point((mouse_x, mouse_y), self.inventory)
        selected_item = arcade.get_sprites_at_point((mouse_x, mouse_y), self.outside_items_list)
        selected_static = arcade.get_sprites_at_point((mouse_x, mouse_y), self.static_list)
        selected_craft_tab = arcade.get_sprites_at_point((mouse_x, mouse_y), self.ui_sprites["craft_tabs"])
        selected_craft_tab_bg = arcade.get_sprites_at_point((mouse_x, mouse_y), self.ui_sprites["craft_tabs_background"])
        for tab in self.ui_sprites["craft_tabs"]:
            selected_craft = arcade.get_sprites_at_point((mouse_x, mouse_y), tab.all_crafts_spritelist)
            if selected_craft:
                selected_craft = (selected_craft[0], tab)
                break

        if button == arcade.MOUSE_BUTTON_LEFT:  # Если нажата левая кнопка мыши
            if self.player.placed_now_static:
                new_static = functions.create_static(THE_GAME, self.player.placed_now_static.static_type, mouse_x, mouse_y)

                # Если касается статика или предмета
                if functions.check_for_collision(THE_GAME, new_static):
                    functions.delete_object_outside(THE_GAME, new_static)
                else:  # Если удачно поставил
                    if self.player.placed_now_static.static_type in self.player.crafted_statics_list:
                        self.player.crafted_statics_list.remove(self.player.placed_now_static.static_type)
                    self.player.placed_now_static = None
                    self.craft_static_light._color = 0, 0, 0

            elif not selected_cell and not selected_craft_tab and not selected_craft:
                if selected_item:  # Добавление предмета в инвентарь
                    selected_item = selected_item[0]
                    # Если игрок рядом с предметом
                    if selected_item.center_x - 80 < self.player.center_x < selected_item.center_x + 80 and \
                            selected_item.center_y - 80 < self.player.center_y < selected_item.center_y + 80:
                        selected_item.pickup_item()
                        self.mouse_player_task = None

                    else:  # Иначе подойти к предмету
                        self.mouse_player_task = (selected_item, "pickup_item")
                        self.drag_mouse = True

                elif selected_static:  # Взаимодействие со статичным объектом
                    selected_static = selected_static[0]
                    # Если игрок рядом с объектом
                    if selected_static.center_x - 80 < self.player.center_x < selected_static.center_x + 80 and \
                            selected_static.center_y - 80 < self.player.center_y < selected_static.center_y + 80:
                        selected_static.static_activating(*selected_static.variables_send_to_func)
                        self.mouse_player_task = None

                    else:  # Иначе подойти к объекту
                        self.mouse_player_task = (selected_static, "static_activating")
                        self.drag_mouse = True

                else:  # Иначе ходьба через мышь
                    self.mouse_player_task = None
                    self.drag_mouse = True

            elif selected_cell:  # Перестановка в инвентаре
                selected_cell[0].inventory_use()

            elif selected_craft_tab or selected_craft_tab_bg:  # Открытие вкладок крафта
                if selected_craft_tab_bg:
                    selected_craft_tab_bg = selected_craft_tab_bg[0]
                    selected_craft_tab = selected_craft_tab_bg.type["tab"]
                else:
                    selected_craft_tab = selected_craft_tab[0]

                selected_craft_tab.tab_clicked()

            elif selected_craft:  # Нажатие на крафт
                selected_craft[1].craft_list_clicked(selected_craft[0])

        elif button == arcade.MOUSE_BUTTON_MIDDLE:  # Сортировка предметов
            if selected_cell:
                selected_cell[0].inventory_sort()

        elif button == arcade.MOUSE_BUTTON_RIGHT:
            if self.player.placed_now_static:
                if self.player.placed_now_static.static_type not in self.player.crafted_statics_list:
                    self.player.crafted_statics_list.append(self.player.placed_now_static.static_type)
                self.player.placed_now_static = None
                self.craft_static_light._color = (0, 0, 0)

            # Описание и активация предметов
            if selected_cell and self.chosen_by_mouse_item_inventory is not None and\
                    self.chosen_by_mouse_item_inventory.is_in_inventory:

                selected_cell = selected_cell[0]

                if selected_cell.item.is_activating:  # Если предмет активируемый
                    selected_cell.item.item_activating(selected_cell.item)

                elif selected_cell.item.is_food:  # Если предмет - еда
                    selected_cell.item.item_eat()

                else:  # Если предмет не активируемый
                    self.player_opinion(selected_cell.item.player_description)

            elif self.inventory[-1].item is not None and not selected_static:  # Выкидывание предметов
                drop_item = self.inventory[-1].item

                drop_item.position = mouse_x, mouse_y
                drop_item.scale = 1
                drop_item.is_in_inventory = False

                self.outside_items_list.append(drop_item)
                self.items_inventory_list.remove(drop_item)
                self.inventory[-1].item = None

            elif selected_static:
                self.player_opinion(selected_static[0].player_description)

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        self.mouse_x = x
        self.mouse_y = y
        if self.player.placed_now_static:  # Если игрок хочет поставить статик
            camera_mouse_x = x + self.camera.position[0]
            camera_mouse_y = y + self.camera.position[1]

            self.player.placed_now_static.position = camera_mouse_x, camera_mouse_y
            self.craft_static_light.position = self.player.placed_now_static.position
            if functions.check_for_collision(THE_GAME, self.player.placed_now_static):
                self.craft_static_light._color = (255, 0, 0)
            else:
                self.craft_static_light._color = (0, 255, 0)

    def on_mouse_scroll(self, x: int, y: int, scroll_x: int, scroll_y: int):
        mouse_x = x + self.camera.position[0]
        mouse_y = y + self.camera.position[1]

        selected_tab = arcade.get_sprites_at_point((mouse_x, mouse_y), self.ui_sprites["craft_tabs"])
        selected_craft_tab_bg = arcade.get_sprites_at_point((mouse_x, mouse_y), self.ui_sprites["craft_tabs_background"])
        if selected_tab:
            if selected_craft_tab_bg:
                selected_craft_tab_bg = selected_craft_tab_bg[0]
                selected_tab = selected_craft_tab_bg.type["tab"]
            else:
                selected_tab = selected_tab[0]

            if not selected_tab.is_open:
                selected_tab.tab_clicked()
            selected_tab.craft_list_clicked(mouse_scroll=scroll_y)

        else:
            for tab in self.ui_sprites["craft_tabs"]:  # Крафты из вкладок крафта (например факел из вкладки Свет)
                if tab.is_open:
                    selected_tab_sprite = arcade.get_sprites_at_point((mouse_x, mouse_y), tab.all_crafts_spritelist)
                    selected_tab_sprite = selected_tab_sprite[0]
                    selected_tab = selected_tab_sprite.type["tab"]
                    selected_tab.craft_list_clicked(mouse_scroll=scroll_y)
                    break

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        if button == 1:
            self.drag_mouse = False

    def camera_using(self):  # Перемещение камеры к игроку
        camera_x = self.player.center_x - main_window.width // 2
        camera_y = self.player.center_y - main_window.height // 2

        self.camera.move_to((camera_x, camera_y), 0.06)

        if self.inventory[-1].item is not None:  # Почему-то перемещается будто бы с задержкой
            self.inventory[-1].item.position = self.mouse_x + self.camera.position[0], self.mouse_y + \
                                               self.camera.position[1]

        self.camera.use()

    def time_cycle(self):  # Главные игровые часы для смены времени суток, статистики игрока и пр.
        # 22.5 градуса - одно деление на шкале времени
        self.time_meter -= 1
        self.time_cycle_meter.angle = self.time_meter / TIME_TO_ANGLE  # отрицательное, чтобы стрелка крутилась вправо
        self.global_game_time = -self.time_cycle_meter.angle  # положительное для удобства

        # 'if global_game_time % 1 == 0:' - выполняется каждый градус
        # 'if global_game_time / 1 == 1:' - выполняется, когда время = 1 градус

        # Выполняется каждый градус
        if self.global_game_time % 1 == 0:
            for i in range(-4, -1):  # Каждый экипированный предмет
                if self.inventory[i].item is not None:
                    self.inventory[i].item.update()
            for food in self.food_list:  # Вся еда гниёт
                if food.durability > 0:
                    food.durability -= 1
                if food.durability <= 0:
                    food.item_type_init("гниль")
                    self.food_list.remove(food)

            if self.player.hunger <= 0:  # Отнимается здоровье, если голод игрока = 0
                functions.increase_status("health", -1.25, THE_GAME)

            if self.change_light_to == EVENING_LIGHT:
                functions.increase_status("sanity", -0.1, THE_GAME, False)

            elif self.change_light_to == NIGHT_LIGHT:
                functions.increase_status("sanity", -0.4, THE_GAME, False)

        if self.global_game_time % 5 == 0:  # Со временем игрок голодает (каждые 5 градусов)
            if self.player.hunger > 0:
                functions.increase_status("hunger", -1, THE_GAME, False)
            else:
                self.player.hunger = 0
                self.player_opinion("Умираю с голода")

        if self.global_game_time / 180 == 1:  # Если стрелка сделала 180 градусов, наступает вечер
            self.change_light_to = EVENING_LIGHT
            self.change_light_on = True
            self.sounds_player(self.music_list[0])

        if self.global_game_time / 270 == 1:  # Если стрелка сделала 270 градусов, наступает ночь
            self.change_light_to = NIGHT_LIGHT
            self.change_light_on = True

        if self.global_game_time / 360 == 1:  # Если стрелка сделала 360 градусов, начинается новый день
            self.global_game_time = 0
            self.change_light_to = DAY_LIGHT
            self.change_light_on = True
            self.time_cycle_meter.angle = 0
            self.time_meter = 0
            self.day += 1
            self.sounds_player(self.music_list[1])

    def player_opinion(self, description):  # на время отображается описание
        description_time = len(description) * 3
        once_code = f'self.player_text.text = "{description}"; self.player_text_black.text = "{description}"'
        at_end_code = f'self.player_text.text = ""; self.player_text_black.text = ""'
        self.timer(description_time, once_code, at_end_code=at_end_code)

        sounds_list = []
        description_time = ceil(description_time / 70)
        if description_time:
            for _ in range(description_time):
                i = random.randint(0, 9)
                if self.player_voice_list[i] not in sounds_list:
                    sounds_list.append(self.player_voice_list[i])

        else:
            sounds_list.append(random.choice(self.player_voice_list))
        self.sounds_player(*sounds_list)

    def sounds_player(self, *sounds_list, sound_volume=ALL_VOLUME):
        if not sounds_list:
            sounds_list = self.playable_sounds_list
            sound_volume = self.playable_sounds_volume
        else:
            self.sound_player_is_playing = True
            self.playable_sounds_id = 0
            self.playable_sounds_list = sounds_list
            self.playable_sounds_volume = sound_volume
            self.sounds_player_value = arcade.play_sound(sounds_list[0], volume=sound_volume)

        if not sounds_list[self.playable_sounds_id].is_playing(self.sounds_player_value):
            self.playable_sounds_id += 1
            try:
                self.sounds_player_value = arcade.play_sound(sounds_list[self.playable_sounds_id], sound_volume)
            except IndexError:
                self.sound_player_is_playing = False
                return "test"

    def change_light(self):
        if self.change_light_to == self.light_layer.light_now:
            self.change_light_on = False
        else:
            for i in range(3):

                if self.light_layer.light_now[i] != self.change_light_to[i]:
                    if self.change_light_to == DAY_LIGHT:
                        self.light_layer.light_now[i] += 1
                    else:
                        self.light_layer.light_now[i] -= 1

    def timer(self, timer_limit=0, once_code=None, repeat_code=None, at_end_code=None):
        if self.timer_on:
            repeat_code = self.repeat_code
            at_end_code = self.at_end_code
            timer_limit = self.timer_limit
        else:
            if once_code:
                exec(once_code)
            self.timer_on = True
            self.timer_limit = timer_limit
            self.repeat_code = repeat_code
            self.at_end_code = at_end_code

        if repeat_code:
            exec(self.repeat_code)

        self.timer_time += 1

        if self.timer_time >= timer_limit:
            if at_end_code:
                exec(self.at_end_code)
            self.timer_time = 0
            self.timer_on = False

            self.repeat_code = None
            self.at_end_code = None

    def timer2(self, timer2_limit=0, once_code2=None, repeat_code2=None, at_end_code2=None):
        if self.timer2_on:
            repeat_code2 = self.repeat_code2
            at_end_code2 = self.at_end_code2
            timer2_limit = self.timer2_limit
        else:
            if once_code2:
                exec(once_code2)
            self.timer2_time = 0
            self.timer2_on = True
            self.timer2_limit = timer2_limit
            self.repeat_code2 = repeat_code2
            self.at_end_code2 = at_end_code2

        if repeat_code2:
            exec(self.repeat_code2)

        self.timer2_time += 1

        if self.timer2_time >= timer2_limit:
            if at_end_code2:
                exec(self.at_end_code2)
            self.timer2_time = 0
            self.timer2_on = False

            self.repeat_code2 = None
            self.at_end_code2 = None


class MainMenu(arcade.View):
    def __init__(self):
        super().__init__()
        self.is_open_console = False
        self.send_to_console = ''
        self.upper_letter = False

        self.buttons_list = arcade.SpriteList()

        self.start_button = arcade.Sprite(":resources:onscreen_controls/flat_dark/play.png")
        self.buttons_list.append(self.start_button)

        self.options_button = arcade.Sprite(":resources:onscreen_controls/flat_dark/wrench.png")
        self.music_button = arcade.Sprite(":resources:onscreen_controls/flat_dark/music_off.png")
        self.music_button.is_on = False
        self.exit_button = arcade.Sprite(":resources:onscreen_controls/flat_dark/close.png")
        self.buttons_list.append(self.options_button)
        self.buttons_list.append(self.music_button)
        self.buttons_list.append(self.exit_button)
        self.main_theme = arcade.Sound("music/MainTheme.mp3").play(loop=True, volume=ALL_VOLUME)
        self.main_theme.pause()

        for i, button in enumerate(self.buttons_list):
            button.ui_position = main_window.width // 2, main_window.height // 3 - i * 60
            button.position = button.ui_position

    def on_draw(self):
        self.buttons_list.draw()

    def game_pause(self):
        for button in self.buttons_list:
            button.center_x = button.ui_position[0] + THE_GAME.camera.position[0]
            button.center_y = button.ui_position[1] + THE_GAME.camera.position[1]

    def setup_game(self):
        global THE_GAME
        if not THE_GAME:
            global MAIN_MENU
            THE_GAME = Game()
            THE_GAME.setup()
            MAIN_MENU = self
            count_text = arcade.Text("", 0, 0)
            count_text.ui_position = THE_GAME.window.width // 2, THE_GAME.window.height - 50
            THE_GAME.count_text = count_text
            main_window.show_view(THE_GAME)
        else:
            main_window.show_view(THE_GAME)

    def open_console(self):
        self.is_open_console = True
        self.send_to_console = ''

        for button in self.buttons_list:  # убираем кнопки подальше
            button.center_x = THE_GAME.camera.position[0] - 100
            button.center_y = THE_GAME.camera.position[1] - 100

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT:
            if not THE_GAME:
                selected_sprite = arcade.get_sprites_at_point((x, y), self.buttons_list)
            else:
                mouse_pos = x + THE_GAME.camera.position[0], y + THE_GAME.camera.position[1]
                selected_sprite = arcade.get_sprites_at_point(mouse_pos, self.buttons_list)

            if selected_sprite[0] == self.start_button:
                self.setup_game()

            elif selected_sprite[0] == self.options_button:
                print("Кажется, некая тёмная сила блокирует эту кнопку. Она наверняка работает, вы чувствуете это, но"
                      "не сейчас... Вероятно, вашему персонажу нужно что-то сделать, чтобы разблокировать доступ к"
                      "настройкам")
            elif selected_sprite[0] == self.music_button:
                if self.music_button.is_on:
                    self.music_button.is_on = False
                    texture = ":resources:onscreen_controls/flat_light/music_off.png"
                    self.music_button.texture = arcade.load_texture(texture)
                    self.main_theme.pause()
                else:
                    self.music_button.is_on = True
                    texture = ":resources:onscreen_controls/flat_light/music_on.png"
                    self.music_button.texture = arcade.load_texture(texture)
                    self.main_theme.play()

            elif selected_sprite[0] == self.exit_button:
                arcade.exit()

    def on_key_press(self, symbol: int, modifiers: int):
        if self.is_open_console:

            if self.upper_letter:
                self.send_to_console += chr(symbol).upper()
            else:
                self.send_to_console += chr(symbol)

            self.send_to_console = self.send_to_console.replace("￢", "SHIFT")
            self.send_to_console = self.send_to_console.replace("￡", "SHIFT")
            self.send_to_console = self.send_to_console.replace("SHIFT-", "_")
            self.send_to_console = self.send_to_console.replace("SHIFT9", "(")
            self.send_to_console = self.send_to_console.replace("SHIFT0", ")")
            self.send_to_console = self.send_to_console.replace("SHIFT;", ":")
            self.send_to_console = self.send_to_console.replace("SHIFT'", '"')
            self.send_to_console = self.send_to_console.replace(chr(arcade.key.CAPSLOCK), '')


            if symbol == arcade.key.BACKSPACE:
                if len(self.send_to_console) >= 5 and self.send_to_console[-6:-1] == "SHIFT":
                    self.send_to_console = self.send_to_console[:-6]
                else:
                    self.send_to_console = self.send_to_console[:-2]

            elif symbol == arcade.key.CAPSLOCK:
                if self.upper_letter:
                    self.upper_letter = False
                else:
                    self.upper_letter = True

            elif symbol == arcade.key.ENTER:
                self.send_to_console = self.send_to_console.replace("SHIFT", "")
                THE_GAME.console_command_exec(self.send_to_console[:-1])
                self.send_to_console = ''

            elif symbol == arcade.key.ESCAPE:
                self.is_open_console = False
                self.setup_game()

            print(self.send_to_console)

        elif symbol == arcade.key.SPACE or symbol == arcade.key.ENTER:
            self.setup_game()

        elif symbol == arcade.key.ESCAPE:
            arcade.exit()


# if __name__ == "__main__":
main_window = arcade.Window(1280, 920, title="Game", center_window=True, fullscreen=FULL_SCREEN)

main_window.show_view(MainMenu())
arcade.run()

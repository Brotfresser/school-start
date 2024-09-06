import arcade

from items import Item
import functions

MAX_VISIBLE_CRAFTS = 6


class CraftTab(arcade.Sprite):
    def __init__(self, tab_type, THE_GAME):
        super().__init__()
        self.THE_GAME = THE_GAME

        self.type = tab_type

        self.is_open = False

        self.ui_position = 0, 0

        self.scale = 0.4

        self.texture = arcade.load_texture(f"UI/craft/{self.type}_craft_tab.png")
        self.tab_background = None
        # макс. размер крафта - 3
        if self.type == "Инструменты":
            self.all_crafts = {
                "ягоды": {"рецепт": (("ветки", 1),), "знания": None, "запоминаемый": True, "статичный": False},

                "ветки": {"рецепт": (("цветок_1", 2), ("ягоды", 50), ("ветки", 3)), "знания": None, "запоминаемый": True, "статичный": False},

                "кремень": {"рецепт": (), "знания": None, "запоминаемый": True, "статичный": False},

                "факел": {"рецепт": (), "знания": {"ветвь": "наука", "уровень": 1}, "запоминаемый": False, "статичный": False},

                "верёвка": {"рецепт": (("ветки", 1),), "знания": {"ветвь": "наука", "уровень": 1}, "запоминаемый": True, "статичный": False},

                "рюкзак": {"рецепт": (("кремень", 1),), "знания": None, "запоминаемый": True, "статичный": False},

                "лечебная мазь": {"рецепт": (("кремень", 1),), "знания": None, "запоминаемый": True, "статичный": False},

                "топор_кремниевый": {"рецепт": (("кремень", 1),), "знания": None, "запоминаемый": True, "статичный": False}
                                     }
        elif self.type == "Свет":
            self.all_crafts = {
                "факел": {"рецепт": (("срезанная трава", 2), ("ветки", 2)), "знания": None, "запоминаемый": True, "статичный": False},
                                     }

        elif self.type == "Наука":
            self.all_crafts = {
                "научная машина": {"рецепт": (("ягоды", 1),), "знания": None, "запоминаемый": True, "статичный": True},
                                     }

        self.visible_crafts = []
        for i, craft in enumerate(self.all_crafts):
            if i < MAX_VISIBLE_CRAFTS:
                self.visible_crafts.append(craft)
            else:
                break
        self.all_crafts_spritelist = arcade.SpriteList()

    def setup(self):
        for y, item in enumerate(self.all_crafts):
            if y >= MAX_VISIBLE_CRAFTS:
                for sprite in self.all_crafts_spritelist:
                    sprite.type["tab_index"] = self.all_crafts_spritelist.index(sprite)
                break

            if "_" in item:
                item_name = item[:item.index("_")]
            else:
                item_name = item
            if self.all_crafts[item]["статичный"]:
                craft = arcade.Sprite(f"static/спрайты для клеток/{item}.png")
            else:
                craft = arcade.Sprite(f"items/{item}.png")
            craft.type = {"type": "craft", "subtype": {"name": item_name, "item": item}, "tab": self}

            craft_background = arcade.Sprite("UI/craft/craft cell.png")
            craft_background.type = {"type": "background", "subtype": {"name": item_name, "item": item}, "tab": self}

            craft.ui_position = (self.THE_GAME.all_craft_tabs_sprite.ui_position[0] + 100,
                                 self.THE_GAME.all_craft_tabs_sprite.ui_position[1] + 200 - y * 78)
            craft_background.ui_position = craft.ui_position

            # Верёвки
            if y < MAX_VISIBLE_CRAFTS - 1:
                craft_background_connecting = arcade.Sprite("UI/craft/connecting.png")
                craft_background_connecting.ui_position = craft.ui_position[0], craft.ui_position[1] - 38
                self.all_crafts_spritelist.append(craft_background_connecting)
                craft_background_connecting.type = {"type": "connecting", "subtype": None, "tab": self}

            # Стрелки
            if y == 0:
                arrow = arcade.Sprite("UI/craft/arrow_off.png", flipped_vertically=True)
                arrow.type = {"type": "arrow", "subtype": "up", "tab": self}
                arrow.ui_position = craft.ui_position[0], craft.ui_position[1] + 100
                self.all_crafts_spritelist.append(arrow)

                self.tab_background = arcade.Sprite("UI/craft/craft tab_none.png", scale=0.4)
                self.tab_background.type = {"type": "tab_background", "subtype": None, "tab": self}
                self.tab_background.ui_position = self.ui_position[0], self.ui_position[1]

            elif y == MAX_VISIBLE_CRAFTS - 1:
                arrow = arcade.Sprite("UI/craft/arrow_default.png")
                arrow.type = {"type": "arrow", "subtype": "down", "tab": self}
                arrow.ui_position = craft.ui_position[0], craft.ui_position[1] - 100
                self.all_crafts_spritelist.append(arrow)

            self.all_crafts_spritelist.append(craft_background)
            self.all_crafts_spritelist.append(craft)

    def craft_list_clicked(self, clicked_sprite=None, mouse_scroll=None):
        if mouse_scroll:  # Если игрок водит колесом мыши (вверх, вниз)

            # Ищем стрелки
            for sprite in self.all_crafts_spritelist:
                if sprite.type["subtype"] == "up" and mouse_scroll == 1:
                    clicked_sprite = sprite
                    break
                elif sprite.type["subtype"] == "down" and mouse_scroll == -1:
                    clicked_sprite = sprite
                    break
            else:
                print("error arrow not find "*20)

        # Крафт
        if clicked_sprite.type["type"] == "craft" or clicked_sprite.type["type"] == "background":
            craft_item_name = clicked_sprite.type["subtype"]["item"]
            craft_item_list = self.all_crafts[clicked_sprite.type["subtype"]["item"]]

            # Проверка, есть ли все предметы из рецепта в инвентаре игрока

            if not functions.is_items_in_inventory(self.THE_GAME, *craft_item_list["рецепт"]) and\
                craft_item_name not in self.THE_GAME.player.crafted_statics_list:
                # Если хоть одного предмета нет, то
                print("Какого-то предмета нет в инвентаре или его нет в нужном кол-ве")

            else:  # Если все предметы у игрока есть и в нужном кол-ве

                if craft_item_list["знания"] is not None:  # Если для крафта нужны знания
                    if craft_item_name not in self.THE_GAME.player.already_craft_items_list:
                        # Если этот предмет ещё не крафтили

                        if craft_item_list["знания"]["ветвь"] == "наука":  # Наука
                            if not self.THE_GAME.player.science_craft_level >= craft_item_list["знания"]["уровень"]:
                                print("Не хватает науки", self.THE_GAME.player.science_craft_level, craft_item_list["знания"]["уровень"])
                                return False
                        elif craft_item_list["знания"]["ветвь"] == "магия":  # Магия
                            if not self.THE_GAME.player.magic_craft_level >= craft_item_list["знания"]["уровень"]:
                                print("Не хватает магии", self.THE_GAME.player.magic_craft_level, craft_item_list["знания"]["уровень"])
                                return False

                # Создание предмета/статичного объекта
                if craft_item_name not in self.THE_GAME.player.crafted_statics_list:  # Если статик ещё не создан
                    functions.spend_item(self.THE_GAME, *craft_item_list["рецепт"])
                if craft_item_list["статичный"]:
                    static = functions.create_static(self.THE_GAME, craft_item_name)
                    static_scale = static.scale
                    functions.delete_object_outside(self.THE_GAME, static)

                    static_sprite = arcade.Sprite(f"static/{craft_item_name}.png", scale=static_scale)
                    static_sprite.static_type = craft_item_name

                    self.THE_GAME.player.placed_now_static = static_sprite

                else:
                    item = Item(craft_item_name, self.THE_GAME, is_in_inventory=True)
                    item.pickup_item()

                if craft_item_list["запоминаемый"] and craft_item_name not in self.THE_GAME.player.already_craft_items_list:
                    self.THE_GAME.player.already_craft_items_list.append(craft_item_name)

                # Непонятно зачем
                """self.THE_GAME.items_inventory_list = arcade.SpriteList()
                for cell in self.THE_GAME.inventory:
                    if cell.item is not None:
                        self.THE_GAME.items_inventory_list.append(cell.item)"""

        # Если игрок листает список крафтов (нажимая на стрелки или крутит колесо мыши)
        elif clicked_sprite.type["type"] == "arrow":
            arrow_type = clicked_sprite.type
            arrow_tab_index = self.THE_GAME.ui_sprites["craft_tabs"].index(arrow_type["tab"])

            for sprite in self.all_crafts_spritelist:  # Поиск стрелок в списке
                if sprite.type["type"] == "arrow":
                    if sprite.type["subtype"] == "up":
                        arrow_up = sprite
                    elif sprite.type["subtype"] == "down":
                        arrow_down = sprite

            # Изменение списка видимых крафтов для игрока
            all_crafts = []
            for craft in self.all_crafts:  # Превращение ключей словаря в список (знаю, это глупо)
                all_crafts.append(craft)

            if arrow_type["subtype"] == "up":  # Если листают вверх
                up_craft = all_crafts[all_crafts.index(self.visible_crafts[0]) - 1]
                if all_crafts[0] != self.visible_crafts[0]:  # Если выше ещё можно листать
                    self.visible_crafts.insert(0, up_craft)
                    self.visible_crafts.pop(-1)
                    self.THE_GAME.sounds_player(arcade.Sound("sounds/ui/HUD_craft_up_v2.mp3"))

                    # Мигание кнопки
                    # Текущая кнопка вверх
                    once_code = f'self.ui_sprites["craft_tabs"][{arrow_tab_index}].'
                    once_code += f'all_crafts_spritelist[{arrow_up.type["tab_index"]}].texture = '
                    once_code += 'arcade.load_texture("UI/craft/arrow_on.png", flipped_vertically=True);'
                    # Кнопка вниз
                    once_code += f'self.ui_sprites["craft_tabs"][{arrow_tab_index}].'
                    once_code += f'all_crafts_spritelist[{arrow_down.type["tab_index"]}].texture = '
                    once_code += 'arcade.load_texture("UI/craft/arrow_default.png")'

                    if all_crafts[0] != self.visible_crafts[0]:  # Если вверх можно листать
                        # Кнопка принимает обычный вид
                        at_end_code = f'self.ui_sprites["craft_tabs"][{arrow_tab_index}].'
                        at_end_code += f'all_crafts_spritelist[{arrow_up.type["tab_index"]}].texture = '
                        at_end_code += 'arcade.load_texture("UI/craft/arrow_default.png", flipped_vertically=True)'
                    else:
                        # Кнопка принимает выключенный вид
                        at_end_code = f'self.ui_sprites["craft_tabs"][{arrow_tab_index}].'
                        at_end_code += f'all_crafts_spritelist[{arrow_up.type["tab_index"]}].texture = '
                        at_end_code += 'arcade.load_texture("UI/craft/arrow_off.png", flipped_vertically=True)'

                    self.THE_GAME.timer(5, once_code, at_end_code=at_end_code)

            elif arrow_type["subtype"] == "down":  # Если листают вниз
                try:
                    down_craft = all_crafts[all_crafts.index(self.visible_crafts[-1]) + 1]
                except IndexError:
                    pass
                if all_crafts[-1] != self.visible_crafts[-1]:  # Если ниже ещё можно листать
                    self.visible_crafts.append(down_craft)
                    self.visible_crafts.pop(0)
                    self.THE_GAME.sounds_player(arcade.Sound("sounds/ui/HUD_craft_down_v2.mp3"))

                    # Мигание кнопки
                    # Текущая кнопка вниз
                    once_code = f'self.ui_sprites["craft_tabs"][{arrow_tab_index}].'
                    once_code += f'all_crafts_spritelist[{arrow_down.type["tab_index"]}].texture = '
                    once_code += 'arcade.load_texture("UI/craft/arrow_on.png");'
                    # Кнопка вверх
                    once_code += f'self.ui_sprites["craft_tabs"][{arrow_tab_index}].'
                    once_code += f'all_crafts_spritelist[{arrow_up.type["tab_index"]}].texture = '
                    once_code += 'arcade.load_texture("UI/craft/arrow_default.png", flipped_vertically=True)'

                    if all_crafts[-1] != self.visible_crafts[-1]:  # Если вниз можно листать
                        # Кнопка принимает обычный вид
                        at_end_code = f'self.ui_sprites["craft_tabs"][{arrow_tab_index}].'
                        at_end_code += f'all_crafts_spritelist[{arrow_down.type["tab_index"]}].texture = '
                        at_end_code += 'arcade.load_texture("UI/craft/arrow_default.png")'
                    else:
                        # Кнопка принимает выключенный вид
                        at_end_code = f'self.ui_sprites["craft_tabs"][{arrow_tab_index}].'
                        at_end_code += f'all_crafts_spritelist[{arrow_down.type["tab_index"]}].texture = '
                        at_end_code += 'arcade.load_texture("UI/craft/arrow_off.png")'

                    self.THE_GAME.timer(5, once_code, at_end_code=at_end_code)

        i = 0
        for sprite in self.all_crafts_spritelist:  # Загрузка текстур и типов для крафтов
            item = self.visible_crafts[i]
            if "_" in item:
                item_name = item[:item.index("_")]
            else:
                item_name = item

            if sprite.type["type"] == "craft":
                if self.all_crafts[item]["статичный"]:
                    sprite.texture = arcade.load_texture(f"static/спрайты для клеток/{item}.png")
                else:
                    sprite.texture = arcade.load_texture(f"items/{item}.png")
                sprite.type["subtype"] = {"name": item_name, "item": item}
                i += 1
            elif sprite.type["type"] == "background":
                sprite.type["subtype"] = {"name": item_name, "item": item}

    def tab_clicked(self):  # Если игрок нажал на вкладку крафта (не на сам крафт), например на вкладку Инструменты
        for tab in self.THE_GAME.ui_sprites["craft_tabs"]:  # Закрытие всех вкладок, кроме текущей
            if tab.is_open and tab is not self:
                tab.tab_background.texture = arcade.load_texture("UI/craft/craft tab_none.png")
                tab.tab_background.scale -= 0.1
                tab.scale -= 0.1
                tab.is_open = False

        if self.is_open:
            self.tab_background.texture = arcade.load_texture("UI/craft/craft tab_none.png")
            self.tab_background.scale -= 0.1
            self.scale -= 0.1
            self.is_open = False
            self.THE_GAME.sounds_player(arcade.Sound("sounds/ui/HUD_craft_close.mp3"))
        else:
            self.tab_background.texture = arcade.load_texture("UI/craft/craft tab_selected.png")
            self.tab_background.scale += 0.1
            self.scale += 0.1
            self.is_open = True
            self.THE_GAME.sounds_player(arcade.Sound("sounds/ui/HUD_craft_open.mp3"))


if __name__ == "__main__":
    print("Вы попали в модуль класса CraftTab, здесь хранятся все типы вкладок крафта с их свойствами")
    import main

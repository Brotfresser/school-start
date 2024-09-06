import arcade

import functions

ITEM_SCALE_IN_INVENTORY = 0.6


class Item(arcade.Sprite):
    def __init__(self, item_type, THE_GAME, count=1, is_in_inventory=False):
        super().__init__()  # У некоторых предметов своя текстура на полу

        self.THE_GAME = THE_GAME

        self.name = None

        self.player_description = ""

        self.is_activating = False
        self.decline = False
        self.durability = None
        self.max_durability = None
        self.breakable = False  # Предмет может потерять прочность

        self.is_food = False
        self.hunger_points_add = 0  # Сколько восстанавливает сытости
        self.health_points_add = 0
        self.sanity_points_add = 0

        self.type = item_type
        self.count = count
        self.max_count = None

        self.is_in_inventory = is_in_inventory
        self.inventory_slot = None  # None, Руки, Тело, Голова
        self.is_equipped = False  # Предмет экипирован
        self.equip_code = ""  # Что произойдёт, когда экипируют
        self.un_equip_code = ""  # Что произойдёт, когда снимут

        #!! self.texture = arcade.load_texture(f"items/{self.type}.png")

        """if "_" in self.type:
            self.name = self.type[:item_type.index("_")]
        else:
            self.name = self.type
        self.name = self.name.title()

        if self.is_in_inventory:
            self.scale = ITEM_SCALE_IN_INVENTORY"""

        self.item_type_init(self.type)

    def item_type_init(self, item_type):
        if item_type[0] in "0123456789":
            item_type = convert_id_type(item_type)

        # Материалы
        if item_type == "ветки":
            self.max_count = 20
            self.player_description = "Куча мелких веток"
        elif item_type == "срезанная трава":
            self.max_count = 30
            self.player_description = "Срезанная трава, твори - созидай что хочешь"
        elif item_type == "кремень":
            self.max_count = 20
            self.player_description = "Это очень острый камень"

        else:  # Еда
            self.is_food = True
            self.decline = True

            if item_type == "ягоды":
                self.durability = 2160
                self.max_count = 10
                self.hunger_points_add = 12.5
            elif item_type == "гниль":
                self.durability = 0
                self.max_count = 40
                self.health_points_add = -1
                self.hunger_points_add = -10

            else:  # Инструменты, броня, амулеты
                self.max_count = 1
                self.is_food = False
                self.durability = 0

                if item_type == "топор_кремниевый":
                    self.inventory_slot = "Рука"
                    self.update = empty_func
                elif item_type == "факел":
                    self.inventory_slot = "Рука"
                    self.durability = 75
                    self.equip_code = "self.THE_GAME.player_light_1._color = (170, 150, 130);"
                    self.equip_code += "self.THE_GAME.player_light_2._color = (14, 14, 14)"
                    self.un_equip_code = "self.THE_GAME.player_light_1._color = (0, 0, 0);"
                    self.un_equip_code += "self.THE_GAME.player_light_2._color = (0, 0, 0)"
                elif item_type == "рюкзак":
                    self.inventory_slot = "Тело"
                    self.update = empty_func

                else:  # Особые предметы, активируемые предметы
                    self.decline = False
                    self.durability = None
                    self.is_activating = True
                    if item_type == "цветок_1":
                        self.item_activating = flower_1
                    elif item_type == "цветок_2":
                        self.item_activating = flower_2
                    elif item_type == "цветок_3":
                        self.is_activating = False
                        self.player_description = "Похоже, что этот цветок является чем-то очень важным..."

        if self.durability is not None:
            self.max_durability = self.durability
        if self.is_food:
            self.THE_GAME.food_list.append(self)
        self.type = item_type
        self.texture = arcade.load_texture(f"items/{self.type}.png")

        if "_" in self.type:
            self.name = self.type[:item_type.index("_")]
        else:
            self.name = self.type
        self.name = self.name.title()

        if self.is_in_inventory:
            self.scale = ITEM_SCALE_IN_INVENTORY

    def equip(self):
        self.is_equipped = True
        exec(self.equip_code)

    def un_equip(self):
        self.is_equipped = False
        exec(self.un_equip_code)

    def update(self):  # Выполняется каждый градус когда предмет носят
        if self.durability > 1:
            self.durability -= 1
        else:
            functions.delete_item(self.THE_GAME, self)
            self.un_equip()

    def item_activating(self):  # Когда предмет активируют в инвентаре
        # перенесён в самый низ модуля для оптимизации
        pass

    def item_eat(self):  # Когда предмет поедают
        if self.type != "гниль":
            durability_percent = int(self.durability / (self.max_durability / 100))
            if 50 > durability_percent > 20:  # Если еда испортилась
                self.hunger_points_add *= (2/3)
                self.health_points_add *= (1/3)
                self.sanity_points_add = 0
            elif durability_percent < 20:  # Если еда почти сгнила
                self.hunger_points_add *= (1/2)
                self.health_points_add = 0
                self.sanity_points_add = -10

        functions.increase_status("hunger", self.hunger_points_add, self.THE_GAME)
        functions.increase_status("health", self.health_points_add, self.THE_GAME)
        functions.increase_status("sanity", self.sanity_points_add, self.THE_GAME)

        if self.count > 1:  # Если в этой ячейке ещё есть еда
            self.count -= 1
        else:
            functions.delete_item(self.THE_GAME, self)

    def __add__(self, other):  # Когда предметы складывают
        if isinstance(other, Item):
            for _ in range(1):
                if self.type == other.type:

                    if self.count + other.count <= self.max_count:
                        self.count += other.count
                        if self.is_food:
                            self.durability = (self.durability + other.durability)/2

                        functions.delete_item(self.THE_GAME, other)
                        return True

                    elif self.count != self.max_count and other.count != other.max_count and other.count != 0:
                        other.count -= self.max_count - self.count
                        if self.is_food:
                            self.durability = (self.durability + other.durability)/2

                        self.count = self.max_count
                        return True

            else:
                return False

    def pickup_item(self):  # Вызывается, когда этот предмет подбирают (левая кнопка мыши)
        if functions.append_item(self.THE_GAME, self):  # Если место для предмета есть и его успешно подобрали
            """if self not in self.THE_GAME.items_inventory_list:
                self.THE_GAME.items_inventory_list.append(self)"""
            self.set_scale()
            if self in self.THE_GAME.outside_items_list:  # Если предмет был снаружи, его убирают
                self.THE_GAME.outside_items_list.remove(self)

    def set_scale(self, new_scale=ITEM_SCALE_IN_INVENTORY):
        self.scale = new_scale
        self.is_in_inventory = True


def empty_func():
    pass
# equip() Экипируемые предметы


# item_activating() Особые предметы


def flower_1(self):
    functions.increase_status("sanity", 10, self.THE_GAME)
    self.item_type_init("цветок_2")

def flower_2(self):
    functions.increase_status("sanity", 10, self.THE_GAME)
    self.item_type_init("цветок_3")

def convert_id_type(item_id):
    item_id = int(item_id)
    translate = ["ветки", "срезанная трава", "кремень", "ягоды", "гниль", "цветок_1"]

    return translate[item_id]



if __name__ == "__main__":
    print("Вы попали в модуль класса Item, здесь хранятся все типы предметов с их свойствами")
    import main
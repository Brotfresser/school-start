import arcade

import items


class Static(arcade.Sprite):
    def __init__(self, static_type, THE_GAME):
        super().__init__()
        self.THE_GAME = THE_GAME

        self.type = static_type

        self.player_description = ""
        self.activating_description = ""
        self.name = ""

        self.texture = arcade.load_texture(f"static/{self.type}.png")
        self.variables_send_to_func = []

        self.is_can_grow = None  # Если объект это ягодный куст, дерево и т.д.
        self.grow_time = None
        self.is_plant = None  # Если объект это ягодный куст, и т.д.
        self.is_empty = None
        self.empty_scale = 1  # Когда собрали
        self.normal_scale = 1  # Когда вырос
        self.empty_time = 0  # Когда очистили объект
        self.aura = None

        if "_" in static_type:
            self.name = self.type[:static_type.index("_")]
        else:
            self.name = static_type

        self.static_type_init()

    def static_activating(self):
        print("Вызванная пустая функция static_activating у", self.type)
        return "пустая static_activating"

    def update(self):
        pass

    def static_type_init(self):
        old_static_activating = self.static_activating
        # Растущие объекты (при {"days": 0, "time": 0} растение никогда не вырастит)
        self.is_can_grow = True
        self.is_plant = True
        self.static_activating = collecting_plants
        self.update = update_plants
        if self.type == "саженец":
            self.variables_send_to_func = [self, "ветки"]
            self.player_description = "Детки деревьев такие милые!"
            self.activating_description = "Собрать ветки с саженца"
            self.normal_scale = 0.35
            self.empty_scale = 1
            self.grow_time = {"days": 2, "time": 0}  # time выражена в градусах
        elif self.type == "ягодный куст":
            self.variables_send_to_func = [self, "ягоды"]
            self.player_description = "Красные ягоды на вкус самые лучшие"
            self.activating_description = "Собрать ягоды с ягодного куста"
            self.normal_scale = 0.33
            self.empty_scale = 0.33
            self.grow_time = {"days": 1, "time": 180}
        elif self.type == "трава":
            self.variables_send_to_func = [self, "срезанная трава"]
            self.player_description = "На дворе трава"
            self.activating_description = "Собрать траву"
            self.grow_time = {"days": 1, "time": 180}

        else:
            self.is_can_grow = False
            self.is_plant = False
            self.static_activating = old_static_activating

            if self.type == "шипы":
                self.player_description = "Они абсолютно не вписываются в стилистику игры. Вот что бывает, " \
                                          "когда руководство бездумно вмешивается и ограничивает чужое творчество"
            elif self.type == "научная машина":
                self.player_description = "Она разбивает предметы на научные составляющие"
                self.aura = arcade.Sprite("aura/standart_aura.png")
                self.aura_enter = science_machine_enter
                self.aura_leave = science_machine_leave
                self.normal_scale = 0.35

        self.scale = self.normal_scale
        if self.aura:
            self.aura.static = self
            self.aura.is_collide = False
            self.THE_GAME.statics_aura_list.append(self.aura)


# static_activating


def collecting_plants(self, item_type: str, count=1):
    if not self.is_empty:
        item = items.Item(item_type, self.THE_GAME, count, True)
        item.pickup_item()

        self.is_empty = True
        self.empty_time = {"day": self.THE_GAME.day, "time": self.THE_GAME.global_game_time}
        self.texture = arcade.load_texture(f"static/{self.type}_пусто.png")
        self.scale = self.empty_scale


# aura_collide
def science_machine_enter(self, THE_GAME):
    if THE_GAME.player.science_craft_level <= 1:
        THE_GAME.player.science_craft_level = 1

def science_machine_leave(self, THE_GAME):
    if THE_GAME.player.science_craft_level <= 1:
        THE_GAME.player.science_craft_level = 0



# update

def update_plants(self):
    game_time = self.THE_GAME.global_game_time
    if self.empty_time:
        if game_time >= self.empty_time["time"] + self.grow_time["time"] and \
                self.THE_GAME.day >= self.empty_time["day"] + self.grow_time["days"]:
            self.texture = arcade.load_texture(f"static/{self.type}.png")
            self.scale = self.normal_scale
            self.is_empty = False
            self.empty_time = 0


if __name__ == "__main__":
    print("Вы попали в модуль класса Static, здесь хранятся все типы статичных объектов с их свойствами")
    import main
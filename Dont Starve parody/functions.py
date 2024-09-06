import copy

import arcade
import items
import statics

import random


def increase_status(status_type, increase, THE_GAME, with_sound=True):
    if not increase == 0:
        if status_type == "hunger":
            status = THE_GAME.player.hunger
            max_status = THE_GAME.player.max_hunger
        elif status_type == "health":
            status = THE_GAME.player.health
            max_status = THE_GAME.player.max_health
        elif status_type == "sanity":
            status = THE_GAME.player.sanity
            max_status = THE_GAME.player.max_sanity

        if status + increase <= max_status:
            status += increase
        else:
            status = max_status

        if status_type == "hunger":
            THE_GAME.player.hunger = status

        elif status_type == "health":
            THE_GAME.player.health = status
        elif status_type == "sanity":
            THE_GAME.player.sanity = status

        if with_sound:
            if increase > 0:
                THE_GAME.sounds_player(arcade.Sound(f"sounds/ui/player status/HUD_{status_type}_up.mp3"))
            else:
                THE_GAME.sounds_player(arcade.Sound(f"sounds/ui/player status/HUD_{status_type}_down.mp3"))


def check_for_collision(THE_GAME, some_object):
    if arcade.check_for_collision_with_list(some_object, THE_GAME.static_list) or\
        arcade.check_for_collision_with_list(some_object, THE_GAME.outside_items_list):

        return True
    else:
        return False


# Действия с инвентарём

def is_items_in_inventory(THE_GAME, *items_list):  # Проверка есть ли предмет в нужном кол-ве
    inventory = player_items_in_inventory(THE_GAME)

    for item in items_list:
        item_type = item[0]
        item_count = item[1]

        if item_type in inventory and item_count <= inventory[item_type]:
            return True
        else:
            return False


def player_items_in_inventory(THE_GAME, show_None=False):  # Словарь предметов в инвентаре в формате {"ветки": 4, "трава": 1}
    if not show_None:
        inventory_items_list = {}  # Список предметов в инвентаре игрока

        for item in THE_GAME.items_inventory_list:
            if inventory_items_list.get(item.type) is None:
                inventory_items_list[item.type] = item.count
            else:
                inventory_items_list[item.type] += item.count

        return inventory_items_list
    else:
        inventory_items_list = []  # Список предметов в инвентаре игрока

        for cell in THE_GAME.inventory:
            if cell.item is None:
                inventory_items_list.append(None)
            else:
                inventory_items_list.append(cell.item.type)

        return inventory_items_list


def spend_item(THE_GAME, *items_list):
    if items_list:
        items_dict = {}
        for item in items_list:
            items_dict[item[0]] = item[1]

        for cell in THE_GAME.inventory:

            if cell.item is not None and cell.item.type in items_dict:
                cell.item.count -= items_dict[cell.item.type]

                if cell.item.count >= 0:
                    del items_dict[cell.item.type]
                    if cell.item.count == 0:
                        delete_item(THE_GAME, cell.item)
                else:
                    items_dict[cell.item.type] = -cell.item.count
                    delete_item(THE_GAME, cell.item)


def append_item(THE_GAME, *items_list):
    empty_cells_list = []
    for cell in THE_GAME.inventory:
        if cell.item is None:
            empty_cells_list.append(cell)

    while True:
        items_append_to_list = []

        for item in items_list:
            for _ in range(1):
                item_is_Item = isinstance(item, items.Item)
                inventory = player_items_in_inventory(THE_GAME, True)
                index = None

                if item_is_Item and item.type in inventory:
                    limit = inventory.count(item.type)
                    if limit == 1:
                        index = inventory.index(item.type)
                    else:
                        for _ in range(limit):
                            index = inventory.index(item.type)
                            game_inventory_item = THE_GAME.inventory[index].item
                            if game_inventory_item.count != game_inventory_item.max_count:
                                break
                            else:
                                inventory[index] = "spam"
                        else:
                            index = None

                if index is not None:
                    if THE_GAME.inventory[index].item + item:

                        if item.count != "del":
                            items_append_to_list.append(item)
                        break

            else:  # Если хоть одно условие не выполнено
                if empty_cells_list:
                    if not item_is_Item:
                        item = items.Item(item[0], THE_GAME, item[1], True)

                    if item.count > item.max_count:
                        item.count -= item.max_count
                        items_append_to_list.append(item)

                        set_cell_item(THE_GAME, empty_cells_list[0], item.type, item.max_count)
                        empty_cells_list.pop(0)
                    else:
                        set_cell_item(THE_GAME, empty_cells_list[0], item)
                        empty_cells_list.pop(0)

        if items_append_to_list:
            items_list = items_append_to_list
        else:
            return True

def set_cell_item(THE_GAME, cell, item_type, item_count=1) -> bool | int:  # Вставляет предмет в ячейку
    if isinstance(item_type, str):  # Если в формате ("ветки", 2)
        new_item = items.Item(item_type, THE_GAME, item_count, True)
    else:
        new_item = item_type
        item_count = new_item.count

    if isinstance(cell, int):  # Если вместо клетки ввели её индекс
        cell = THE_GAME.inventory[cell]
    if cell.item is not None:  # Если ячейка не пустая, то чистим её
        delete_item(THE_GAME, cell.item)
    if cell.type is not None and new_item.inventory_slot != cell.type:
        # Если пытаются вставить предмет в неподходящую ячейку (траву в руки, кремень в голову)
        cell_index = THE_GAME.inventory.index(cell)
        print(f"В ячейку {cell.type} {cell_index} пытались положить неподходящий предмет {item_type} 1")
        del new_item
        return False
    elif cell.type is not None and new_item.inventory_slot == cell.type:
        new_item.equip()
    if new_item.count > new_item.max_count:  # Если вставили слишком много
        new_item.count = new_item.max_count

    cell.item = new_item
    if new_item not in THE_GAME.items_inventory_list:
        THE_GAME.items_inventory_list.append(new_item)

    if not(item_count - new_item.count):  # Если поместилось - отправляем True
        return True
    else:  # иначе - кол-во оставшегося предмета
        remains = item_count - new_item.count

        if isinstance(item_type, str):  # Если в формате ("ветки", 2)
            return remains
        else:
            return items.Item(new_item.type, THE_GAME, remains, True)


def create_static(THE_GAME, static_type, x=0, y=0) -> statics.Static:
    new_static = statics.Static(static_type, THE_GAME)
    new_static.position = x, y
    THE_GAME.static_list.append(new_static)

    return new_static


def delete_item(THE_GAME, item):  # Удаляет предмет из инвентаря
    item.remove_from_sprite_lists()
    for cell in THE_GAME.inventory:
        if cell.item is item:
            cell.item = None

    item.count = "del"


def delete_object_outside(THE_GAME, object):  # удаляет упавший предмет или статик
    object.remove_from_sprite_lists()
    del object


if __name__ == "__main__":
    import main
import random

from rpg_battle.battle_actions_ren import ACTION_LIBRARY, BattleAction
from rpg_cards.cards_ren import Card, CARD_SUITS
from rpg_dungeon.dungeon_area_ren import DungeonArea, DUNGEON_AREAS
from rpg_npc.npc_ren import NPC
from rpg_role.roles_ren import *
from rpg_system.renpy_constant import renpy, battle_controller, battle_action_controller, npc_controller

"""renpy
init -50 python:
"""


class DungeonController:
    def __init__(self):
        self.available_roles = [
            ROLE_SLAVE,
            ROLE_CLERGY,
            ROLE_MONK,
            ROLE_THIEF,
            ROLE_HUNTER,
            ROLE_ADVENTURER,
            ROLE_BARD,
            ROLE_FARMER,
            ROLE_MERCHANT,
            ROLE_ALCHEMIST,
            ROLE_SCHOLAR,
            ROLE_MAGE,
            ROLE_SOLDIER,
            ROLE_KNIGHT,
            ROLE_PRINCE
        ]
        self.available_area = DUNGEON_AREAS
        self.current_area = self.available_area[0]
        self.dungeon_level = 1
        self.current_floor = 1
        self.current_enemy_list = []
        self.player_hands = []
        self.placed_card = None

    def create_enemy_list(self):
        enemy_count = random.choice([0, 1, 2])
        # todo max_level = self.dungeon_level + self.current_floor
        enemy_list = npc_controller.gen_dungeon_npc(enemy_count)
        return enemy_list

    def start(self, dungeon_level):
        self.player_hands = []
        self.dungeon_level = dungeon_level
        self.current_floor = 1
        self.step()
        renpy.call("start_dungeon")

    def player_place_card(self, card):
        self.placed_card = card
        self.player_hands.remove(card)

    def step(self):
        if self.placed_card is not None:
            if isinstance(self.placed_card.addition, NPC):
                card = self.placed_card
                self.placed_card = None
                battle_controller.start(card.addition)
                return
            elif isinstance(self.placed_card.addition, DungeonArea):
                self.current_area = self.placed_card.addition
                self.current_floor = self.placed_card.number
        self.placed_card = None
        self.player_hands.clear()
        self.player_hands.append(Card(14, "Hearts", "empty", "离开", "回家了", None))
        area_card_size = random.randint(1, 3)
        for i in range(area_card_size):
            area = random.choice(self.available_area)
            self.player_hands.append(
                Card(self.current_floor + 1, "Clovers", area.name, area.title, "前往" + area.title, area))
        enemy_list = self.create_enemy_list()
        for enemy in enemy_list:
            self.player_hands.append(enemy.card())

    def settle_battle_result(self, battle_result):
        result = battle_result[0]
        enemy = battle_result[1]
        player_rank = battle_result[2]
        if result == 'win':
            return battle_action_controller.enemy_draw_cards(enemy.id, 3)

    def player_choose_reward(self, card):
        battle_action_controller.player_get_action(card.addition)

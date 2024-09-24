# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 18:57:47 2024

@author: rikuto.yamada
"""

import pygame
import sys
import random

# 初期化
pygame.init()

# 画面サイズ
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# 色の定義
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
BLUE = (0, 0, 255)

# フォントの設定
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

# 画面の作成
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Card Game")

# ボタンクラス
class Button:
    def __init__(self, x, y, width, height, text, color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# カードクラス
class Card:
    def __init__(self, name, cost, damage, block):
        self.name = name
        self.cost = cost
        self.damage = damage
        self.block = block

    def use(self, player, enemy):
        player.energy -= self.cost
        enemy.hp -= self.damage
        player.block += self.block

# プレイヤークラス
class Player:
    def __init__(self):
        self.max_hp = 100
        self.hp = self.max_hp
        self.energy = 3
        self.max_energy = 3
        self.block = 0
        self.deck = [
            Card("Strike", 1, 6, 0),
            Card("Defend", 1, 0, 5),
            Card("Bash", 2, 8, 0),
        ]
        self.hand = []
        self.discard_pile = []

    def draw_card(self, num=1):
        for _ in range(num):
            if not self.deck:
                self.deck = self.discard_pile
                self.discard_pile = []
                random.shuffle(self.deck)
            if self.deck:
                self.hand.append(self.deck.pop())

    def start_turn(self):
        self.energy = self.max_energy
        self.draw_card(5)
        self.block = 0

    def end_turn(self):
        self.discard_pile.extend(self.hand)
        self.hand = []
        

# 敵クラス
class Enemy:
    def __init__(self, name, hp, actions):
        self.name = name
        self.hp = hp
        self.actions = actions
        self.current_action = None
        self.choose_action()

    def choose_action(self):
        self.current_action = random.choice(self.actions)

    def act(self, player):
        damage = self.current_action['damage']
        player.hp -= max(0, damage - player.block)
        player.block = max(0, player.block - damage)
        self.choose_action()

# 戦闘クラス
class Battle:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.turn = 1
        self.message = ""
        self.message_timer = 0

    def start_battle(self):
        self.player.start_turn()

    def play_card(self, card_index):
        if card_index < len(self.player.hand):
            card = self.player.hand[card_index]
            if self.player.energy >= card.cost:
                card.use(self.player, self.enemy)
                self.player.hand.pop(card_index)
                self.player.discard_pile.append(card)
                self.set_message(f"Player used {card.name}")

    def end_player_turn(self):
        self.player.end_turn()
        self.enemy.act(self.player)
        self.set_message(f"{self.enemy.name} used {self.enemy.current_action['name']}")
        self.turn += 1
        self.player.start_turn()

    def is_battle_over(self):
        return self.player.hp <= 0 or self.enemy.hp <= 0

    def get_result(self):
        if self.player.hp <= 0:
            return "defeat"
        elif self.enemy.hp <= 0:
            return "victory"
        else:
            return None

    def set_message(self, message):
        self.message = message
        self.message_timer = 120  # 2 seconds at 60 FPS

    def update(self):
        if self.message_timer > 0:
            self.message_timer -= 1
        else:
            self.message = ""

# メインメニュー画面
def main_menu():
    new_game_button = Button(300, 200, 200, 50, "New Game", GRAY, WHITE)
    continue_button = Button(300, 270, 200, 50, "Continue", GRAY, WHITE)
    exit_button = Button(300, 340, 200, 50, "Exit", GRAY, WHITE)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if new_game_button.is_clicked(event.pos):
                    return "new_game"
                elif continue_button.is_clicked(event.pos):
                    return "continue"
                elif exit_button.is_clicked(event.pos):
                    pygame.quit()
                    sys.exit()

        screen.fill(BLACK)
        new_game_button.draw(screen)
        continue_button.draw(screen)
        exit_button.draw(screen)

        title_text = font.render("Card Game", True, WHITE)
        screen.blit(title_text, (350, 100))

        pygame.display.flip()

# ダンジョンマップ画面
def dungeon_map():
    nodes = [
        {"pos": (100, 500), "type": "normal"},
        {"pos": (250, 400), "type": "elite"},
        {"pos": (400, 450), "type": "rest"},
        {"pos": (550, 350), "type": "merchant"},
        {"pos": (700, 500), "type": "boss"}
    ]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for node in nodes:
                    if (node["pos"][0] - event.pos[0])**2 + (node["pos"][1] - event.pos[1])**2 <= 30**2:
                        if node["type"] == "normal":
                            return "battle"
                        else:
                            print(f"Clicked on {node['type']} node")

        screen.fill(DARK_GRAY)

        # ノードの描画
        for i, node in enumerate(nodes):
            color = WHITE if node["type"] == "normal" else RED if node["type"] == "elite" else GREEN if node["type"] == "rest" else YELLOW if node["type"] == "merchant" else PURPLE
            pygame.draw.circle(screen, color, node["pos"], 30)
            if i < len(nodes) - 1:
                pygame.draw.line(screen, WHITE, node["pos"], nodes[i+1]["pos"], 2)

        # フロア情報とプレイヤー状態の表示
        floor_text = font.render("Floor 1", True, WHITE)
        screen.blit(floor_text, (10, 10))
        hp_text = font.render("HP: 75/100", True, WHITE)
        screen.blit(hp_text, (650, 10))

        pygame.display.flip()

# 戦闘画面
def battle_screen(player, enemy):
    battle = Battle(player, enemy)
    battle.start_battle()

    end_turn_button = Button(650, 500, 120, 50, "End Turn", GRAY, WHITE)

    while not battle.is_battle_over():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if end_turn_button.is_clicked(event.pos):
                    battle.end_player_turn()
                for i, card in enumerate(battle.player.hand):
                    card_rect = pygame.Rect(50 + i * 120, 450, 100, 140)
                    if card_rect.collidepoint(event.pos):
                        battle.play_card(i)

        battle.update()
        screen.fill(DARK_GRAY)

        # プレイヤーの情報表示
        pygame.draw.rect(screen, BLUE, (10, 10, 300, 100))
        player_hp_text = font.render(f"HP: {battle.player.hp}/{battle.player.max_hp}", True, WHITE)
        screen.blit(player_hp_text, (20, 20))
        player_energy_text = font.render(f"Energy: {battle.player.energy}/{battle.player.max_energy}", True, WHITE)
        screen.blit(player_energy_text, (20, 60))
        player_block_text = small_font.render(f"Block: {battle.player.block}", True, WHITE)
        screen.blit(player_block_text, (20, 100))

        # 敵の情報表示
        pygame.draw.rect(screen, RED, (490, 10, 300, 100))
        enemy_hp_text = font.render(f"{enemy.name}", True, WHITE)
        screen.blit(enemy_hp_text, (500, 20))
        enemy_hp_bar = pygame.Rect(500, 60, 280 * (enemy.hp / 50), 30)
        pygame.draw.rect(screen, GREEN, enemy_hp_bar)
        pygame.draw.rect(screen, WHITE, (500, 60, 280, 30), 2)
        enemy_hp_text = font.render(f"{enemy.hp}/50", True, WHITE)
        screen.blit(enemy_hp_text, (500, 100))

        # 敵の次のアクションを表示
        next_action_text = small_font.render(f"Next: {enemy.current_action['name']}", True, WHITE)
        screen.blit(next_action_text, (500, 130))

        # メッセージの表示
        if battle.message:
            message_surface = font.render(battle.message, True, YELLOW)
            screen.blit(message_surface, (SCREEN_WIDTH // 2 - message_surface.get_width() // 2, 200))

        # 手札の表示
        for i, card in enumerate(battle.player.hand):
            card_rect = pygame.Rect(50 + i * 120, 450, 100, 140)
            pygame.draw.rect(screen, WHITE, card_rect)
            card_name = small_font.render(card.name, True, BLACK)
            screen.blit(card_name, (card_rect.x + 5, card_rect.y + 5))
            card_cost = small_font.render(f"Cost: {card.cost}", True, BLACK)
            screen.blit(card_cost, (card_rect.x + 5, card_rect.y + 25))
            if card.damage > 0:
                card_damage = small_font.render(f"Damage: {card.damage}", True, RED)
                screen.blit(card_damage, (card_rect.x + 5, card_rect.y + 45))
            if card.block > 0:
                card_block = small_font.render(f"Block: {card.block}", True, BLUE)
                screen.blit(card_block, (card_rect.x + 5, card_rect.y + 65))

        end_turn_button.draw(screen)

        pygame.display.flip()

    result = battle.get_result()
    print(f"Battle ended with result: {result}")
    return "dungeon_map"

# メインループ
def main():
    current_screen = "main_menu"
    player = Player()
    enemy = Enemy("Slime", 50, [
        {"name": "Attack", "damage": 10},
        {"name": "Defend", "damage": 5},
        {"name": "Strong Attack", "damage": 15}
    ])

    while True:
        if current_screen == "main_menu":
            result = main_menu()
            if result == "new_game":
                current_screen = "dungeon_map"
        elif current_screen == "dungeon_map":
            result = dungeon_map()
            if result == "battle":
                current_screen = "battle"
        elif current_screen == "battle":
            result = battle_screen(player, enemy)
            if result == "dungeon_map":
                current_screen = "dungeon_map"

if __name__ == "__main__":
    main()
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 14:17:56 2024

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
BLUE = (0, 0, 255)

# フォントの設定
FONT = pygame.font.Font(None, 36)
SMALL_FONT = pygame.font.Font(None, 24)

# 画面の作成
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Card Game")

class Button:
    def __init__(self, x, y, width, height, text, color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        text_surface = FONT.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class Card:
    def __init__(self, name, cost, damage, block):
        self.name = name
        self.cost = cost
        self.damage = damage
        self.block = block

    def use(self, user, target):
        user.energy -= self.cost
        target.hp -= self.damage
        user.block += self.block

class GameEntity:
    def __init__(self, name, max_hp, max_energy, base_block):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.max_energy = max_energy
        self.energy = max_energy
        self.block = base_block
        self.deck = []
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

class Player(GameEntity):
    def __init__(self):
        super().__init__("Player", 100, 3)
        self.deck = [
            Card("Strike", 1, 6, 0),
            Card("Defend", 1, 0, 5),
            Card("Bash", 2, 8, 0),
        ] * 3  # 各カードを3枚ずつ入れる
        random.shuffle(self.deck)

class Enemy(GameEntity):
    def __init__(self, name, hp, actions):
        super().__init__(name, hp, 0)  # エネルギーは使用しないので0
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

def draw_battle_screen(battle):
    screen.fill(DARK_GRAY)

    # プレイヤーの情報表示
    pygame.draw.rect(screen, BLUE, (10, 10, 300, 100))
    player_hp_text = FONT.render(f"HP: {battle.player.hp}/{battle.player.max_hp}", True, WHITE)
    screen.blit(player_hp_text, (20, 20))
    player_energy_text = FONT.render(f"Energy: {battle.player.energy}/{battle.player.max_energy}", True, WHITE)
    screen.blit(player_energy_text, (20, 60))

    # 敵の情報表示
    pygame.draw.rect(screen, RED, (490, 10, 300, 100))
    enemy_hp_text = FONT.render(f"{battle.enemy.name}", True, WHITE)
    screen.blit(enemy_hp_text, (500, 20))
    enemy_hp_bar = pygame.Rect(500, 60, 280 * (battle.enemy.hp / battle.enemy.max_hp), 30)
    pygame.draw.rect(screen, GREEN, enemy_hp_bar)
    pygame.draw.rect(screen, WHITE, (500, 60, 280, 30), 2)
    enemy_hp_text = FONT.render(f"{battle.enemy.hp}/{battle.enemy.max_hp}", True, WHITE)
    screen.blit(enemy_hp_text, (500, 100))

    # メッセージの表示
    if battle.message:
        message_surface = FONT.render(battle.message, True, WHITE)
        screen.blit(message_surface, (SCREEN_WIDTH // 2 - message_surface.get_width() // 2, 200))

    # 手札の表示
    for i, card in enumerate(battle.player.hand):
        card_rect = pygame.Rect(50 + i * 120, 450, 100, 140)
        pygame.draw.rect(screen, WHITE, card_rect)
        card_name = SMALL_FONT.render(card.name, True, BLACK)
        screen.blit(card_name, (card_rect.x + 5, card_rect.y + 5))
        card_cost = SMALL_FONT.render(f"Cost: {card.cost}", True, BLACK)
        screen.blit(card_cost, (card_rect.x + 5, card_rect.y + 25))
        if card.damage > 0:
            card_damage = SMALL_FONT.render(f"Damage: {card.damage}", True, RED)
            screen.blit(card_damage, (card_rect.x + 5, card_rect.y + 45))
        if card.block > 0:
            card_block = SMALL_FONT.render(f"Block: {card.block}", True, BLUE)
            screen.blit(card_block, (card_rect.x + 5, card_rect.y + 65))

    # ターン終了ボタンの表示
    end_turn_button = Button(650, 500, 120, 50, "End Turn", GRAY, WHITE)
    end_turn_button.draw(screen)

    pygame.display.flip()

def battle_screen(player, enemy):
    battle = Battle(player, enemy)
    battle.start_battle()

    end_turn_button = Button(650, 500, 120, 50, "End Turn", GRAY, WHITE)

    clock = pygame.time.Clock()

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
        draw_battle_screen(battle)
        clock.tick(60)

    result = battle.get_result()
    print(f"Battle ended with result: {result}")
    return "dungeon_map"

def main():
    player = Player()
    enemy = Enemy("Slime", 50, [
        {"name": "Attack", "damage": 10},
        {"name": "Defend", "damage": 5},
        {"name": "Strong Attack", "damage": 15}
    ])

    battle_screen(player, enemy)

if __name__ == "__main__":
    main()
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 18:10:25 2024

@author: rikuto.yamada
"""

import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Backpack Battles Prototype")

# Set up clock for frame rate control
clock = pygame.time.Clock()

### CLASSES ###
class Item:
    def __init__(self, name, size, color, effect):
        self.name = name
        self.size = size  # size is a tuple (width, height)
        self.color = color
        self.effect = effect  # Effects on stats like attack, defense, etc.

    def draw(self, surface, x, y):
        pygame.draw.rect(surface, self.color, (x, y, self.size[0] * 40, self.size[1] * 40))

class Inventory:
    def __init__(self, rows, cols):
        self.grid = [[None for _ in range(cols)] for _ in range(rows)]
        self.cell_size = 40  # Each grid cell is 40x40 pixels

    def draw(self, surface, x_offset, y_offset):
        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                rect = pygame.Rect(x_offset + col * self.cell_size, y_offset + row * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(surface, BLACK, rect, 1)

                # Draw item if one is in the cell
                if self.grid[row][col] is not None:
                    item = self.grid[row][col]
                    item.draw(surface, x_offset + col * self.cell_size, y_offset + row * self.cell_size)

    def add_item(self, item, position):
        x, y = position
        if self.grid[y][x] is None:
            self.grid[y][x] = item  # For simplicity, assume items fit into a single cell for now

    def clear(self):
        self.grid = [[None for _ in range(len(self.grid[0]))] for _ in range(len(self.grid))]

class Character:
    def __init__(self, name, hp, attack, defense, speed):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.speed = speed

    def take_damage(self, amount):
        self.hp -= max(amount - self.defense, 0)
        if self.hp < 0:
            self.hp = 0

    def is_alive(self):
        return self.hp > 0

    def attack_opponent(self, opponent):
        damage = max(self.attack - opponent.defense, 0)
        opponent.take_damage(damage)
        return damage

    def apply_item_effects(self, item):
        self.attack += item.effect.get('attack', 0)
        self.defense += item.effect.get('defense', 0)

class Battle:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.turn_order = sorted([self.player, self.enemy], key=lambda x: x.speed, reverse=True)
        self.current_turn = 0

    def take_turn(self):
        attacker = self.turn_order[self.current_turn % 2]
        defender = self.enemy if attacker == self.player else self.player
        damage = attacker.attack_opponent(defender)
        
        print(f"{attacker.name} attacks {defender.name} for {damage} damage!")
        print(f"{defender.name} HP: {defender.hp}")
        
        self.current_turn += 1

        # End battle if one is dead
        if not self.player.is_alive():
            print("Player has been defeated!")
        elif not self.enemy.is_alive():
            print("Enemy has been defeated!")
    
    def is_battle_over(self):
        return not (self.player.is_alive() and self.enemy.is_alive())

### GAME MANAGER ###
class GameManager:
    def __init__(self):
        self.state = 'inventory'  # Initial state is inventory phase
        self.player = Character("Player", 100, 10, 5, 10)
        self.enemy = Character("Enemy", 80, 15, 3, 8)
        self.battle = None  # Initialize during battle phase
        self.inventory = Inventory(4, 4)
        
        # Define player items
        self.sword = Item("Sword", (1, 2), RED, {'attack': 5})
        self.shield = Item("Shield", (2, 2), GREEN, {'defense': 3})

        # Add player items to inventory
        self.inventory.add_item(self.sword, (0, 0))
        self.inventory.add_item(self.shield, (2, 0))

        # Define enemy items
        self.enemy_items = [Item("Enemy Sword", (1, 1), BLUE, {'attack': 4}),
                            Item("Enemy Shield", (2, 1), BLUE, {'defense': 2})]

    def update(self, event):
        # Handle state-specific updates
        if self.state == 'inventory':
            self.inventory_phase(event)
        elif self.state == 'battle':
            self.battle_phase(event)
    
    def inventory_phase(self, event):
        # When player presses space, start battle with equipped items
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print("Starting battle...")
                self.start_battle()

    def battle_phase(self, event):
        # Press any key to advance battle turn
        if event.type == pygame.KEYDOWN:
            if self.battle and not self.battle.is_battle_over():
                self.battle.take_turn()

    def start_battle(self):
        # Apply player item effects
        for row in self.inventory.grid:
            for item in row:
                if item:
                    self.player.apply_item_effects(item)
        
        # Apply enemy item effects
        for item in self.enemy_items:
            self.enemy.apply_item_effects(item)

        # Start the battle
        self.battle = Battle(self.player, self.enemy)
        self.state = 'battle'

    def draw(self):
        # Handle state-specific drawing
        if self.state == 'inventory':
            self.draw_inventory_phase()
        elif self.state == 'battle':
            self.draw_battle_phase()

    def draw_inventory_phase(self):
        # Draw the inventory
        screen.fill(WHITE)
        self.inventory.draw(screen, 100, 100)
        font = pygame.font.SysFont(None, 36)
        text = font.render('Press SPACE to start battle', True, BLACK)
        screen.blit(text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 50))

    def draw_battle_phase(self):
        screen.fill(WHITE)
        font = pygame.font.SysFont(None, 36)
        
        # Display HP of both players
        player_hp = font.render(f'Player HP: {self.player.hp}', True, BLUE)
        enemy_hp = font.render(f'Enemy HP: {self.enemy.hp}', True, RED)
        
        screen.blit(player_hp, (50, 50))
        screen.blit(enemy_hp, (SCREEN_WIDTH - 250, 50))

        # Draw player inventory
        self.inventory.draw(screen, 50, SCREEN_HEIGHT - 200)

        # Draw enemy inventory (simplified display of enemy items)
        self.draw_enemy_inventory(screen, SCREEN_WIDTH - 250, SCREEN_HEIGHT - 200)

        if self.battle.is_battle_over():
            result = "Player wins!" if self.player.is_alive() else "Enemy wins!"
            result_text = font.render(result, True, BLACK)
            screen.blit(result_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))

    def draw_enemy_inventory(self, surface, x_offset, y_offset):
        # Draw enemy items (simplified, not in a grid like the player)
        for idx, item in enumerate(self.enemy_items):
            item.draw(surface, x_offset, y_offset + idx * 50)

### MAIN GAME LOOP ###
game_manager = GameManager()

running = True
while running:
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Update game state
        game_manager.update(event)

    # Draw game elements
    game_manager.draw()

    # Update display
    pygame.display.flip()

    # Frame rate control (60 FPS)
    clock.tick(60)

pygame.quit()

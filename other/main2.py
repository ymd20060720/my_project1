# -*- coding: utf-8 -*-
"""
Created on Sat Sep 14 19:07:01 2024

@author: rikuto.yamada
"""
import pygame
import numpy
from random import randint, choice
from sys import exit
from enum import Enum



#constant
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600

class Game():
    def run(self):
        # Initialize Pygame and set up the game window
        pygame.init()
        pygame.display.set_caption('yamada')
        self.screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        self.clock = pygame.time.Clock()
        self.current_state = GameState.START
        self.last_state = GameState.START
        
        # Create button objects
        self.create_buttons()
        
        # Map game states to their corresponding buttons
        self.state_buttons = {
            GameState.START: [self.buttons[0]],
            GameState.HOME: [self.buttons[1], self.buttons[2], self.buttons[3], self.buttons[6]],
            GameState.RESULT: [self.buttons[4]],
            GameState.SHOP: [self.buttons[5], self.buttons[6]],
            GameState.BATTLE: [self.buttons[6]],
            GameState.SETTING: [self.buttons[7]]
        }
        
        # Main game loop
        while True:
            events = pygame.event.get()
            self.handle_events(events)
            self.update_game_state()
            self.draw_current_state(events)
            
            pygame.display.update()
            self.clock.tick(60)  # Maintain 60 FPS

    def create_buttons(self):
        # Create multiple button objects and store them in a list
        self.buttons = [
            Button((400, 500), "buttons/press_button0.png", "buttons/press_button1.png", (200, 400)),
            Button((150, 250), "buttons/start_button0.png", "buttons/start_button1.png", (100, 200)),
            Button((150, 350), "buttons/item_button0.png", "buttons/item_button1.png", (100, 200)),
            Button((150, 450), "buttons/exit_button0.png", "buttons/exit_button1.png", (100, 200)),
            Button((400, 500), "buttons/return_button0.png", "buttons/return_button1.png", (200, 400)),
            Button((400, 50), "buttons/battle_button0.png", "buttons/battle_button1.png", (100, 200)),
            Button((770, 30), "buttons/setting_button0.png", "buttons/setting_button0.png", (100, 100)),
            Button((770, 30), "buttons/setting_button0.png", "buttons/setting_button0.png", (100, 100))
        ]

    def handle_events(self, events):
        for event in events:
            # Handle quit event
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            # Handle keydown events to change game states
            if event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)

    def handle_keydown(self, key):
        # Map keys to game states
        key_state_map = {
            pygame.K_a: GameState.START,
            pygame.K_b: GameState.HOME,
            pygame.K_c: GameState.SHOP,
            pygame.K_d: GameState.BATTLE,
            pygame.K_e: GameState.SETTING,
            pygame.K_f: GameState.RESULT
        }
        
        # Update the current state if a valid key is pressed
        if key in key_state_map:
            self.current_state = key_state_map[key]

    def update_game_state(self):
        # Update the screen based on the current state
        self.screen_state_update()
        self.state()

    def draw_current_state(self, events):
        # Draw buttons for the current game state
        if self.current_state in self.state_buttons:
            for button in self.state_buttons[self.current_state]:
                button.update(events)
                button.draw(self.screen)

    def screen_state_update(self):
        if self.buttons[0].pushed == True:
            self.current_state = GameState.HOME
        if self.buttons[1].pushed == True:
            self.current_state = GameState.SHOP
        # if self.buttons[2].pushed == True:
        #     self.current_state = GameState.
        if self.buttons[3].pushed == True:
            pygame.quit()
            exit()
        if self.buttons[4].pushed == True:
            self.current_state = GameState.HOME
        if self.buttons[5].pushed == True:
            self.current_state = GameState.BATTLE
        if self.buttons[6].pushed == True:
            self.last_state = self.current_state
            self.current_state = GameState.SETTING
        if self.buttons[7].pushed == True:
            self.current_state = self.last_state
        for i in range(len(self.buttons)):
            self.buttons[i].pushed = False
            
    def state(self):
        if self.current_state == GameState.START:
            self.screen.fill((0,255,0))
        if self.current_state == GameState.HOME:
            self.screen.fill((255,0,0))
        if self.current_state == GameState.SHOP:
            self.screen.fill((0,0,255))
        if self.current_state == GameState.BATTLE:
            self.screen.fill((0,255,255))
        if self.current_state == GameState.SETTING:
            self.screen.fill((255,0,255))
        if self.current_state == GameState.RESULT:
            self.screen.fill((255,255,0))
            
# Define screen states using Enum
class GameState(Enum):
    START = 1
    HOME = 2
    SHOP = 3
    BATTLE = 4
    RESULT = 5
    SETTING = 6
    PAUSE = 7
    
class ButtonName(Enum):
    PRESS = 0
    START = 1
    ITEM = 2
    EXIT = 3
    RETURN = 4
            
class Button(pygame.sprite.Sprite):
    def __init__(self, pos, img_path_default, img_path_hover, size):
        super().__init__()
        self.image_default = self._load_and_scale_image(img_path_default, size)
        self.image_hover = self._load_and_scale_image(img_path_hover, size)
        self.image = self.image_default
        self.rect = self.image.get_rect(center=pos)
        self.mask = pygame.mask.from_surface(self.image_default)
        self.pushed = False

    def _load_and_scale_image(self, img_path, size):
        return pygame.transform.scale(pygame.image.load(img_path), size)

    def update(self, events):
        mouse_pos = pygame.mouse.get_pos()
        relative_mouse_pos = (mouse_pos[0] - self.rect.x, mouse_pos[1] - self.rect.y)
        
        is_hovering = self._is_mouse_over(mouse_pos, relative_mouse_pos)
        self.image = self.image_hover if is_hovering else self.image_default

        self._handle_click_events(events, mouse_pos, relative_mouse_pos)

    def _is_mouse_over(self, mouse_pos, relative_mouse_pos):
        return (self.rect.collidepoint(mouse_pos) and 
                self.mask.get_at(relative_mouse_pos))

    def _handle_click_events(self, events, mouse_pos, relative_mouse_pos):
        for event in events:
            if (event.type == pygame.MOUSEBUTTONDOWN and 
                self._is_mouse_over(mouse_pos, relative_mouse_pos)):
                self.pushed = True

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

        
        
class Player(pygame.sprite.Sprite):
    def __init__(self,groups,obstacle_sprites):
        super().__init__(groups)
        player_walk1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk1, player_walk2]
        self.player_index = 0
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80,300))
        
        self.obstacle_sprites = obstacle_sprites
        
    # def p_input(self):
    #     keys = pygame.key.get_pressed()
    #     #mouse = pygame.mouse.get_pressed()
    #     if keys[pygame.K_SPACE]:
    #         print('a')
    #     else:
    #         print('b')
            
        
        
    def animation_state(self):
        self.player_index += 0.1
        if self.player_index >= len(self.player_walk):self.player_index = 0
        self.image = self.player_walk[int(self.player_index)]
        
    def update(self):
        self.player_input()
        self.animation_state()

class Obstacle():
    def __init__(self):
        super().__init__()
        obstacle_image1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        obstacle_image2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.obstacle_image = [obstacle_image1, obstacle_image2]
        self.obstacle_index = 0
        self.surf = self.obstacle_image[self.obstacle_index]
        self.rect = self.surf.get_rect(midbottom = (80,300))
        
        
    def animation_state(self):
        self.obstacle_index += 0.1
        if self.obstacle_index >= len(self.obstacle_image):self.obstacle_index = 0
        self.image = self.obstacle_image[int(self.obstacle_index)]
        
    def update(self):
        self.animation_state()
        
class Item():
    def __init__(self):
        super().__init__()
        item_image1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        item_image2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.item_image = [item_image1, item_image2]
        self.item_index = 0
        self.surf = self.item_image[self.item_index]
        self.rect = self.surf.get_rect(midbottom = (80,300))
    
    def animation_state(self):
        self.item_index += 0.1
        if self.item_index >= len(self.item_image):self.item_index = 0
        self.image = self.item_image[int(self.item_index)]
        
    def update(self):
        self.animation_state()
    


#def

# def event_check():
#     if pygame.event == pygame.KEYDOWN:
#         print('key down')
#     if pygame.event == pygame.QUIT:
#         pygame.quit()
#         exit()

#main
if __name__ == "__main__":
    game = Game()
    game.run()
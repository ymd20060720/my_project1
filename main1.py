# -*- coding: utf-8 -*-
"""
Created on Sat Sep 14 09:45:18 2024

@author: rikuto.yamada
"""
#import
import pygame
import numpy
from random import randint, choice
from sys import exit
from enum import Enum



#constant
display_width = 800
display_height = 600

class Game():
    def run(self):
        # Initialize Pygame and set up the game window
        pygame.init()
        pygame.display.set_caption('yamada')
        self.screen = pygame.display.set_mode((display_width, display_height))
        self.clock = pygame.time.Clock()
        self.current_state = GameState.START
        
        # Create button objects
        self.create_buttons()
        
        # Map game states to their corresponding buttons
        self.state_buttons = {
            GameState.START: [self.buttons[0]],
            GameState.HOME: [self.buttons[1], self.buttons[2], self.buttons[3]],
            GameState.RESULT: [self.buttons[4]]
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
            Button((400, 500), "buttons/return_button0.png", "buttons/return_button1.png", (200, 400))
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
            self.current_state = GameState.SETTING
        if self.buttons[2].pushed == True:
            self.current_state = GameState.BATTLE
        if self.buttons[3].pushed == True:
            pygame.quit()
            exit()
        if self.buttons[4].pushed == True:
            self.current_state = GameState.HOME
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
        """
        pos: ボタンの表示位置 (x, y)
        img_path_default: 通常状態のボタン画像ファイルパス
        img_path_hover: ホバー/押下状態のボタン画像ファイルパス
        """
        # 通常状態のボタン画像をロード
        self.image_default = pygame.image.load(img_path_default)
        self.image_hover = pygame.image.load(img_path_hover)
        self.image_default = pygame.transform.scale(self.image_default, size)
        self.image_hover = pygame.transform.scale(self.image_hover, size)
        
        # Create the button rect and mask for collision detection
        self.button = self.image_default.get_rect(center=pos)
        self.mask = pygame.mask.from_surface(self.image_default)  # Create mask from the default image
        
        self.image = self.image_default  # 初期状態は通常画像
        self.pushed = False
        
    def update(self, events):
        mouse_pos = pygame.mouse.get_pos()
    
        # Check if mouse is within the button rect
        if self.button.collidepoint(mouse_pos):
            # Calculate the mouse position relative to the button's top-left corner
            relative_mouse_pos = (mouse_pos[0] - self.button.x, mouse_pos[1] - self.button.y)
            
            # Only check the mask if the mouse is inside the button rect
            if self.mask.get_at(relative_mouse_pos):  # Check non-transparent pixel
                self.image = self.image_hover  # Hover state
            else:
                self.image = self.image_default  # Default state
        else:
            self.image = self.image_default  # Default state when outside button
    
        # Mouse click detection
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Again, check relative mouse position only if inside button rect
                if self.button.collidepoint(mouse_pos):
                    if self.mask.get_at(relative_mouse_pos):  # Click only on non-transparent part
                        self.pushed = True
                            

                        
    def draw(self, screen):
        """
        ボタンを画面に描画する関数
        """
        screen.blit(self.image, self.button.topleft)

        
        
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
        self.player_index += 0.1
        if self.player_index >= len(self.player_walk):self.player_index = 0
        self.image = self.player_walk[int(self.player_index)]
        
    def update(self):
        self.animation_state()
        
class Item():
    def __init__(self):
        super().__init__()
        obstacle_image1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        obstacle_image2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.obstacle_image = [obstacle_image1, obstacle_image2]
        self.obstacle_index = 0
        self.surf = self.obstacle_image[self.obstacle_index]
        self.rect = self.surf.get_rect(midbottom = (80,300))
    
    def animation_state(self):
        self.player_index += 0.1
        if self.player_index >= len(self.player_walk):self.player_index = 0
        self.image = self.player_walk[int(self.player_index)]
        
    def update(self):
        self.animation_state()
    


#def

def event_check():
    if pygame.event == pygame.KEYDOWN:
        print('key down')
    if pygame.event == pygame.QUIT:
        pygame.quit()
        exit()

#main
if __name__ == "__main__":
    game = Game()
    game.run()
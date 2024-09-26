import pygame
from .scene_manager import SceneManager
from .input_manager import InputManager
from .render_manager import RenderManager

class GameManager():
    def __init__(self, screen, scene_list):
        self.screen = screen
        self.scene_list = scene_list
        self.scene_manager = SceneManager(scene_list)
        self.input_manager = InputManager(self.scene_manager.scenes)
        self.render_manager = RenderManager(screen)
        self.save_load_manager = SaveLoadManager()

    def handle_event(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.happened_event = self.input_manager.handle_event(event)
                if type(self.happened_event) == (self.scene_manager.Scene):
                    self.scene_manager.put_next_scene(self.happened_event)
                print('handle_event')

    def update(self):
        #self.input_manager.update()
        self.next_scene = self.scene_manager.get_next_scene()
        self.scene_manager.update()
        self.render_manager.update(self.next_scene)
        print('update')

    def draw(self):
        self.render_manager.clear
        self.render_manager.draw()
        self.render_manager.present()
        print('draw')

    def save(self):
        self.save_load_manager.save()

    def load(self):
        self.save_load_manager.load()

#単体テストで実行するときは
#python -m game.game_manager
def test():
    print('a')

if __name__ == '__main__':
    test()
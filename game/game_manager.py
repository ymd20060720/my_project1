import pygame
from .scene_manager import SceneManager
from .input_manager import InputManager
from .render_manager import RenderManager
from .save_load_manager import SaveLoadManager

class GameManager():
    def __init__(self, screen, scene_list):
        self.running = True
        self.screen = screen
        self.scene_list = scene_list
        self.scene_manager = SceneManager(scene_list)
        self.input_manager = InputManager(self.scene_manager.scenes)
        self.render_manager = RenderManager(screen)
        self.save_load_manager = SaveLoadManager()

    def handle_event(self):#self.events_happenedで受け取る
        self.events_happened = self.input_manager.handle_event()
        if self.events_happened == ['quit']:
            self.running = False
        if type(self.events_happened) == (self.scene_manager.Scene):
            self.scene_manager.change_scene(self.events_happened)

    def update(self):#self.events_happenedをforで回して分解して適した引数にぶち込む
        for i, event in enumerate(self.events_happened):
            if type(event) == self.scene_manager.Scene:
                self.scene_manager.change_scene(event)
        self.current_scene = self.scene_manager.get_current_scene()
        self.render_manager.update(self.current_scene)
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
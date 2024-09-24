import pygame
from .scene_manager import SceneManager
from .input_manager import InputManager
from .render_manager import RenderManager

class GameManager():
    def __init__(self, screen, scene_list):
        self.screen = screen
        self.scene_manager = SceneManager(scene_list)
        self.input_manager = InputManager()
        self.render_manager = RenderManager(screen)

    def handle_event(self,event):
        self.input_manager.handle_event(event)
        # 他の必要なイベント処理
        print('handle_event')
    def update(self):
        self.input_manager.update()
        self.current_scene = self.scene_manager.get_current_scene()
        print('update')

    def draw(self):
        self.render_manager.clear
        self.render_manager.draw()
        self.render_manager.present()
        print('draw')

#単体テストで実行するときは
#python -m game.game_manager
def test():
    print('a')

if __name__ == '__main__':
    test()
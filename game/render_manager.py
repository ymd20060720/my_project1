import pygame
from .constants import BLACK

class RenderManager():
    def __init__(self, screen):
        print('render_manager initialize')
        self.screen = screen

    def update(self, current_scene):
        self.current_scene = current_scene
        print('update')

    def draw(self):
        self.screen.fill(self.current_scene.color)
        print('draw')

    def clear(self):
        self.screen.fill(BLACK)

def test():
    print('a')

if __name__ == '__main__':
    test()
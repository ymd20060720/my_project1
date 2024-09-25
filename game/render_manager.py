import pygame

class RenderManager():
    def __init__(self, screen):
        print('render_manager initialize')
        self.screen = screen

    def update(self, next_scene):
        self.next_scene = next_scene
        print('update')

    def draw(self):
        self.screen.fill(self.next_scene.color)
        print('draw')

    def clear(self):
        print('clear')

    def present(self):
        print('a')

def test():
    print('a')

if __name__ == '__main__':
    test()
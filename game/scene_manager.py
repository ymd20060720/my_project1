import pygame
from dataclasses import dataclass
from .constants import SCENE_LIST

class SceneManager():
    @dataclass
    class Scene():
        name: str
        color: tuple

    def __init__(self, scene_list):
        self.scenes = [self.Scene(key,value) for key, value in SCENE_LIST.items()]
        self.current_scene = self.scenes[0]
        self.next_scene = self.scenes[1]
        self.previous_scene = None


    '''def put_next_scene(self, next_scene):
        if next_scene in self.scenes:
            self.next_scene = next_scene
        else:
            print(f'error: {next_scene} do not exist in scenes')

    def update(self):
        self.previous_scene = self.current_scene
        self.current_scene = self.next_scene'''
    
    def change_scene(self, next_scene):
        if next_scene in self.scenes:
            self.previous_scene = self.current_scene
            self.current_scene = next_scene
        else:
            print(f'error: {next_scene} do not exist in scenes')

    '''def get_next_scene(self):
        return self.next_scene'''

    def get_current_scene(self):
        return self.current_scene
    
    '''def get_previous_scene(self):
        return self.previous_scene'''
    
def test():
    scene_manager = SceneManager(SCENE_LIST)
    scene_manager.change_scene(scene_manager.scenes[5])
    print(scene_manager.get_current_scene().name)

if __name__ == '__main__':
    test()
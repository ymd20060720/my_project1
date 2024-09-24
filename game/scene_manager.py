import pygame

class SceneManager():
    def __init__(self, scene_list):
        print('scene_manager initialize')
        self.current_scene = scene_list[0]

    def get_current_scene(self):
        return self.current_scene
    

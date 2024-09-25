import pygame

class Player():
    def __init__(self, hp, mp):
        self.hp = hp
        self.mp = mp

    def get_hp(self):
        return self.hp
    
    def put_hp(self, hp):
        self.hp = hp

    def get_mp(self):
        return self.mp
    
    def put_mp(self, mp):
        self.mp = mp
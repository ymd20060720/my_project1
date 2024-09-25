import pygame

class InputManager():
    def __init__(self, scenes):
        print('InputManager initialize')
        self.scenes = scenes

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.happened_event = self.scenes[0]
            if event.key == pygame.K_b:
                self.happened_event = self.scenes[1]
            if event.key == pygame.K_c:
                self.happened_event = self.scenes[2]
            if event.key == pygame.K_d:
                self.happened_event = self.scenes[3]
            if event.key == pygame.K_e:
                self.happened_event = self.scenes[4]
            if event.key == pygame.K_f:
                self.happened_event = self.scenes[5]
            return self.happened_event

    def update(self):
        print('a')

def test():
    print('a')

if __name__ == '__main__':
    test()
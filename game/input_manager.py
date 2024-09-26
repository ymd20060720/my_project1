import pygame

class InputManager():
    def __init__(self, scenes):
        print('InputManager initialize')
        self.scenes = scenes

    def handle_event(self)->list:
        self.events_happened = []
        for i, event in enumerate(pygame.event.get()):
                if event.type == pygame.QUIT:#停止を最優先するためにquitで上書き
                    self.events_happened = ['quit']
                    break
                if event.type == pygame.KEYDOWN:
                    self.handle_event_scene(event)
        return self.events_happened
    
    def handle_event_scene(self, event)->None:
        if event.key == pygame.K_a:
            self.events_happened.append(self.scenes[0])
        if event.key == pygame.K_b:
            self.events_happened.append(self.scenes[1])
        if event.key == pygame.K_c:
            self.events_happened.append(self.scenes[2])
        if event.key == pygame.K_d:
            self.events_happened.append(self.scenes[3])
        if event.key == pygame.K_e:
            self.events_happened.append(self.scenes[4])
        if event.key == pygame.K_f:
            self.events_happened.append(self.scenes[5])


    def get_input_state(self):
        return self.events_happened
        print('a')

def test():
    print('a')

if __name__ == '__main__':
    test()
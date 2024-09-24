import pygame
import sys
from game.game_manager import GameManager
from game.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.game_manager = GameManager(self.screen)

    def run(self):
        running = True
        while running:
            # イベント処理
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.game_manager.handle_event(event)

            # ゲーム状態の更新
            self.game_manager.update()

            # 画面描画
            self.screen.fill((0, 0, 0))  # 画面を黒でクリア
            self.game_manager.draw()
            pygame.display.flip()

            # フレームレートの制御
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
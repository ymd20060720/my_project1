# GameManager構造と役割分担

## GameManager の主な役割

GameManagerは、ゲーム全体を管理し、他のManagerを調整する中心的な役割を果たします。

- ゲームの状態管理（メニュー、プレイ中、ポーズなど）
- 他のManagerの初期化と管理
- ゲームループの制御（更新と描画の呼び出し）
- グローバルなイベント処理

## 分割したManagerの役割

1. SceneManager
   - 異なるゲームシーン（メインメニュー、バトル、マップ探索など）の管理
   - シーン間の遷移処理

2. InputManager
   - ユーザー入力（キーボード、マウス）の処理
   - 入力イベントの適切なハンドラへの配信

3. RenderManager
   - 画面描画の管理
   - レイヤー順序の制御
   - カメラ/ビューポートの管理（必要な場合）

4. AudioManager
   - BGMと効果音の再生管理
   - 音量調整

5. ResourceManager
   - 画像、音声、フォントなどのリソースのロードと管理
   - リソースのキャッシュ管理

6. UIManager
   - ユーザーインターフェース要素の管理
   - メニュー、ダイアログ、HUDの制御

7. EntityManager
   - ゲーム内のエンティティ（プレイヤー、敵、NPCなど）の管理
   - エンティティの更新とライフサイクル管理

8. BattleManager
   - 戦闘システムの管理
   - ターン制御、ダメージ計算

9. MapManager
   - マップの生成と管理
   - プレイヤーの移動とマップ内のイベント処理

10. CardManager
    - デッキとカードの管理
    - カードの効果処理

11. SaveManager
    - ゲームのセーブとロード機能の管理

## GameManagerと他のManagerの連携例

```python
class GameManager:
    def __init__(self, screen):
        self.screen = screen
        self.scene_manager = SceneManager(self)
        self.input_manager = InputManager()
        self.render_manager = RenderManager(screen)
        self.audio_manager = AudioManager()
        self.resource_manager = ResourceManager()
        self.ui_manager = UIManager(self)
        self.entity_manager = EntityManager()
        self.battle_manager = BattleManager(self)
        self.map_manager = MapManager()
        self.card_manager = CardManager()
        self.save_manager = SaveManager()

    def update(self):
        self.input_manager.update()
        current_scene = self.scene_manager.get_current_scene()
        current_scene.update()
        self.entity_manager.update()
        self.ui_manager.update()

    def draw(self):
        self.render_manager.clear()
        current_scene = self.scene_manager.get_current_scene()
        current_scene.draw(self.render_manager)
        self.ui_manager.draw(self.render_manager)
        self.render_manager.present()

    def handle_event(self, event):
        self.input_manager.handle_event(event)
        # 他の必要なイベント処理
```

この構造により、各Managerが特定の責任を持ち、GameManagerがそれらを調整します。これにより、コードの管理が容易になり、機能の追加や変更が簡単になります。

# ゲームクラス構造の概要

1. GameManager
   - `Initialize()`: ゲームの初期化
   - `Update()`: ゲームループの更新
   - `ChangeGameState(GameState newState)`: ゲーム状態の変更
   - `SaveGame()`: ゲームの保存
   - `LoadGame()`: ゲームのロード

2. RenderManager
   - `DrawScene()`: 現在のシーンを描画
   - `UpdateUI()`: UI要素の更新
   - `LoadAssets()`: グラフィックアセットの読み込み

3. Artifact (GameItemから派生)
   - `ApplyEffect(Player player)`: 装備効果の適用
   - `RemoveEffect(Player player)`: 装備効果の解除
   - `Upgrade()`: アーティファクトのアップグレード

4. Card (GameItemから派生)
   - `Play(Target target)`: カードのプレイ
   - `DrawCard()`: カードを引く
   - `DiscardCard()`: カードを捨てる

5. Creature (Monsterの代わり)
   - `TakeTurn()`: ターンの実行
   - `TakeDamage(int amount)`: ダメージの受け取り
   - `UseAbility(Ability ability, Target target)`: 能力の使用

6. Effect
   - `ApplyEffect(Target target)`: 効果の適用
   - `UpdateEffect()`: 効果の更新（持続時間など）
   - `RemoveEffect(Target target)`: 効果の除去

7. Player
   - `TakeTurn()`: プレイヤーのターン実行
   - `DrawCard()`: カードを引く
   - `PlayCard(Card card, Target target)`: カードのプレイ
   - `LevelUp()`: レベルアップ処理

8. Obstacle
   - `Interact(Player player)`: プレイヤーとの相互作用
   - `ApplyEffect(Target target)`: 効果の適用（例：ダメージ、状態異常）

9. Deck
   - `ShuffleDeck()`: デッキのシャッフル
   - `DrawCard()`: カードを引く
   - `AddCard(Card card)`: カードの追加
   - `RemoveCard(Card card)`: カードの削除

10. Map
    - `GenerateMap()`: マップの生成
    - `MovePlayer(Direction direction)`: プレイヤーの移動
    - `GetCurrentRoom()`: 現在の部屋の情報取得
    - `RevealRoom(int x, int y)`: 部屋の発見

11. BattleManager
    - `StartBattle(Player player, Creature enemy)`: 戦闘の開始
    - `ExecuteTurn()`: ターンの実行
    - `CheckBattleEnd()`: 戦闘終了条件のチェック
    - `DistributeRewards()`: 報酬の配布

12. ItemManager
    - `AddItemToInventory(GameItem item)`: アイテムの追加
    - `RemoveItemFromInventory(GameItem item)`: アイテムの削除
    - `UseItem(GameItem item, Target target)`: アイテムの使用
    - `GenerateRandomItem()`: ランダムアイテムの生成

13. SaveManager
    - `SaveGameState()`: ゲーム状態の保存
    - `LoadGameState()`: ゲーム状態のロード
    - `CreateSaveFile()`: セーブファイルの作成
    - `DeleteSaveFile()`: セーブファイルの削除

14. UIManager
    - `UpdateUI()`: UI全体の更新
    - `ShowMenu(MenuType type)`: メニューの表示
    - `HideMenu(MenuType type)`: メニューの非表示
    - `UpdateHealthBar(float currentHealth, float maxHealth)`: HPバーの更新

    Button (UIManagerの一部として実装):
    - `OnClick()`: クリック時の動作
    - `SetEnabled(bool enabled)`: ボタンの有効/無効設定

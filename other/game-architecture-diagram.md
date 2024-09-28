:::mermaid
classDiagram
    class Game {
        -clock
        -game_manager
        +run()
    }
    class GameManager {
        -scene_manager: SceneManager
        -input_manager: InputManager
        -render_manager: RenderManager
        -save_load_manager: SaveLoadManager
        +handle_event(dt)
        +update()
        +draw()
        +save()
        +load()
    }
    class SceneManager {
        -scenes : Scene
        -current_scene: Scene
        +get_current_scene() -> current_scene
        +change_scene(next_scene: Scene)
    }
    class InputManager {
        -scenes: Scene
        +handle_event() -> events_happened:list
        +handle_event_scene(event)
        +get_input_state() -> events_happened:list
    }
    class RenderManager {
        -screen: pygame.display.set_mode
        -assets
        +load_assets(assets_path)
        +update(scene: Scene)
        +draw()
        +clear()
    }
    class SaveLoadManager {
        -data: Data
        +save(data_info: Data)
        +load()
    }
    class Scene {
        -name: str
        -image: pygame.image.load
    }
    class Player{
        -name
        -image
        -hp
        +change_name(name)
        +
    }
    class Data{
        -path
    }
    Game --> GameManager
    GameManager --> SceneManager
    GameManager --> InputManager
    GameManager --> RenderManager
    GameManager --> SaveLoadManager
    SceneManager --> Scene
    SaveLoadManager --> Data
:::
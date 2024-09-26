:::mermaid
classDiagram
    class Main {
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
        +get_current_scene()
        +change_scene(next_scene: Scene)
    }
    class InputManager {
        +handle_events() -> event_happened:list
        +get_input_state()
    }
    class RenderManager {
        -screen: pygame.display.set_mode
        +draw_scene(scene: Scene)
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
    class Data{
        -path
    }
    Main --> GameManager
    GameManager --> SceneManager
    GameManager --> InputManager
    GameManager --> RenderManager
    GameManager --> SaveLoadManager
    SceneManager --> Scene
    SaveLoadManager --> Data
:::
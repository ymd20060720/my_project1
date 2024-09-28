:::mermaid
classDiagram
    class Broker {
        -Dict[str, Any] events
        -Dict[str, List[Subscriber]] events_subscribers
        +event_add(event_name: str) -> None
        +subscriber_add(event_name: str, subscriber: Subscriber) -> None
        +subscriber_remove(event_name: str, subscriber: Subscriber) -> None
        +event_remove(event_name: str) -> None
        +clear() -> None
        +update(event_name: str, event_content: Any) -> None
        +check(event_name: str, subscriber: Subscriber) -> Any
    }
    class Publisher {
        -Broker broker
        -List[str] events_published
        +publish_event(event_name: str) -> None
        +unpublish(event_name: str) -> None
        +update(event_name: str, event_content: Any) -> None
    }
    class Subscriber {
        -Broker broker
        -List[str] events_subscribed
        +subscribe_event(event_name: str) -> None
        +unsubscribe(event_name: str) -> None
        +check(event_name: str) -> Any
    }
    class GenericPublisher {
        -Publisher publisher
        +__init__(event_names: List[str])
        +update(event_name: str, event_content: Any) -> None
        +unpublish(event_name: str) -> None
    }
    class GenericSubscriber {
        -Subscriber subscriber
        -Callable[[str, Any], None] callback
        +__init__(event_names: List[str], callback: Callable[[str, Any], None])
        +update() -> None
        +unsubscribe(event_name: str) -> None
    }
    
    Broker --* Publisher : uses
    Broker --* Subscriber : uses
    Publisher --o GenericPublisher : contains
    Subscriber --o GenericSubscriber : contains
:::
:::mermaid
classDiagram
    class Publisher{
        <<abstract>>
        -events_published: list[event_name]
        +publish(event_name) %%if event_name is in events, pass
        +unpublish(event_name) %%if event_name is not in events, pass
        +unpublish_all() %%all of events_published. if events_published = [], pass
        +update(event_name, event_content)
        +search_event() -> list[event_name]
        +check_subscribers(event_name) -> list[subscriber]
        +check_event_content(event_name) -> event_content
    }
    class Broker{
        -events: dict[event_name, event_content]
        -events_subscribers: dict[event_name, list[subscriber]]
        +event_add(event_name)
        +subscriber_add(event_name, subscriber)
        +event_remove(event_name)
        +subscriber_remove(event_name, subscriber)
        +clear()
        +update(event_name, event_content)
        +Is_in_events(event_name) ->bool
        +Is_not_in_events(event_name) ->bool
        +Is_in_events_subscribers(event_name, subscribers) ->bool
        +Is_not_in_events_subscribers(event_name, subscribers) ->bool
    }
    class Subscriber{
        <<abstract>>
        -events_subscribed: list[event_name]
        +subscribe(event_name)
        +unsubscribe(event_name)
        +unsubscribe_all()
        +check(event_name) -> event_content
        +search_event() -> list[event_name] = events.keys()
        +(receive(event_name, event_content))for Broker
    }
    Publisher <--> Broker
    Broker <--> Subscriber
:::
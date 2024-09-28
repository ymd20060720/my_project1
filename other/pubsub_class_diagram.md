:::mermaid
classDiagram
    class Publisher{
        -events_published
        +publish_event(event)
        +notify_broker()
    }
    class Broker{
        -publish_events_list
        -subscribers_list
        +notify_subscriber()
    }
    class Subscriber{
        -events_subscribed
        +subscribe_event(event)
        +unsubscribe_event(event)
    }
    Publisher --> Broker
    Broker --> Subscriber
:::
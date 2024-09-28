# Publish-Subscribe System Specification and Usage Guide

## Overview

This module implements a publish-subscribe (pub-sub) pattern in Python, providing a flexible and efficient way to manage event-driven communication between different parts of an application.

## Key Components

1. **Broker**: Manages events and subscribers centrally.
2. **Publisher**: Publishes events to the broker.
3. **Subscriber**: Subscribes to events and receives updates.
4. **GenericPublisher**: A wrapper around Publisher for easier use.
5. **GenericSubscriber**: A wrapper around Subscriber for easier use.

## Detailed Specification

### Broker

The Broker is a singleton class that manages all events and their subscribers.

Methods:
- `event_add(event_name: str) -> None`: Adds a new event.
- `subscriber_add(event_name: str, subscriber: Subscriber) -> None`: Adds a subscriber to an event.
- `subscriber_remove(event_name: str, subscriber: Subscriber) -> None`: Removes a subscriber from an event.
- `event_remove(event_name: str) -> None`: Removes an event and all its subscribers.
- `clear() -> None`: Clears all events and subscriptions.
- `update(event_name: str, event_content: Any) -> None`: Updates the content of an event.
- `check(event_name: str, subscriber: Subscriber) -> Any`: Retrieves the content of an event for a subscriber.

### Publisher

The Publisher class is responsible for publishing events to the Broker.

Methods:
- `publish_event(event_name: str) -> None`: Publishes a new event.
- `unpublish(event_name: str) -> None`: Unpublishes an event.
- `update(event_name: str, event_content: Any) -> None`: Updates the content of a published event.

### Subscriber

The Subscriber class is used to subscribe to events and receive updates.

Methods:
- `subscribe_event(event_name: str) -> None`: Subscribes to an event.
- `unsubscribe(event_name: str) -> None`: Unsubscribes from an event.
- `check(event_name: str) -> Any`: Retrieves the content of a subscribed event.

### GenericPublisher

A wrapper around Publisher for easier use with multiple events.

Methods:
- `__init__(event_names: List[str])`: Initializes with a list of event names to publish.
- `update(event_name: str, event_content: Any) -> None`: Updates the content of a published event.
- `unpublish(event_name: str) -> None`: Unpublishes an event.

### GenericSubscriber

A wrapper around Subscriber for easier use with multiple events and a callback function.

Methods:
- `__init__(event_names: List[str], callback: Callable[[str, Any], None])`: Initializes with a list of event names to subscribe to and a callback function.
- `update() -> None`: Checks for updates on all subscribed events and calls the callback function for each.
- `unsubscribe(event_name: str) -> None`: Unsubscribes from an event.

## Usage

Here's a basic example of how to use this publish-subscribe system:

```python
from pub_sub import GenericPublisher, GenericSubscriber

# Create a publisher for two events
publisher = GenericPublisher(["event1", "event2"])

# Create a subscriber that listens to both events
def event_callback(event_name: str, event_content: Any) -> None:
    print(f"Received update for {event_name}: {event_content}")

subscriber = GenericSubscriber(["event1", "event2"], event_callback)

# Publish updates
publisher.update("event1", "Hello")
publisher.update("event2", "World")

# Check for updates
subscriber.update()

# Unsubscribe from an event
subscriber.unsubscribe("event2")

# Unpublish an event
publisher.unpublish("event2")
```

This system can be used in various scenarios where you need loose coupling between components in your application. It's particularly useful in event-driven architectures, GUI applications, or any situation where you need to broadcast changes to multiple listeners.

## Error Handling

The system uses custom `EventError` exceptions to handle error cases. Be sure to wrap your code in try-except blocks to handle these exceptions gracefully.

## Performance Considerations

While this system is designed to be efficient, be mindful when dealing with a very large number of events or subscribers, as it may impact performance. In such cases, consider implementing additional optimizations or using a more specialized pub-sub system.

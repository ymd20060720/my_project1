"""
pub_sub.py - A restructured publish-subscribe system with compatible type annotations

This module implements a publish-subscribe (pub-sub) pattern, using structured data types
for events and subscribers management, with type annotations compatible with older Python versions.

Data structures:
- events: Dict[str, Any] - {event_name: event_content}
- events_subscribers: Dict[str, List[Subscriber]] - {event_name: [subscriber1, subscriber2, ...]}

Classes:
    Broker: Manages events and subscribers
    Publisher: Publishes events
    Subscriber: Subscribes to and receives events
    InputClass: Example class that publishes events
    OutputClass: Example class that subscribes to events

Usage:
    from pub_sub import Publisher, Subscriber, InputClass, OutputClass, Broker

    # Create instances
    input_obj = InputClass()
    output_obj = OutputClass()

    # Publish and receive events
    input_obj.change_x(5)
    output_obj.update()

    # Unsubscribe from an event
    output_obj.subscriber.unsubscribe('x_change')

    # Unpublish an event
    input_obj.publisher.unpublish('x_change')

    # Clear all events and subscriptions
    Broker().clear()
"""

from typing import Dict, List, Any, Optional

class Broker:
    """
    Singleton class that manages events and subscribers.

    This class is responsible for maintaining events and their subscribers.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Broker, cls).__new__(cls)
            cls._instance.events = {}  # type: ignore # type: Dict[str, Any]
            cls._instance.events_subscribers = {}  # type: ignore # type: Dict[str, List['Subscriber']]
        return cls._instance

    def event_add(self, event_name:str) -> None:
        """
        Add a new event to the broker.

        Args:
            event_name (str): The name of the event to add.
            event_content (Any): The content of the event.
        """
        if event_name not in self.events:
            self.events[event_name] = None
            self.events_subscribers[event_name] = []
        if self.Is_in_events(event_name):
            pass

    def subscriber_add(self, event_name: str, subscriber: 'Subscriber') -> None:
        """
        Add a subscriber to an event.

        Args:
            event_name (str): The name of the event to subscribe to.
            subscriber (Subscriber): The subscriber object.
        """
        if self.Is_not_in_events(event_name):pass
        else:
            if self.Is_in_events_subscribers(event_name, subscriber):pass
            else:
                self.events_subscribers[event_name].append(subscriber)

    def subscriber_remove(self, event_name: str, subscriber: 'Subscriber') -> None:
        """
        Remove a subscriber from an event.

        Args:
            event_name (str): The name of the event to unsubscribe from.
            subscriber (Subscriber): The subscriber object to remove.
        """
        if self.Is_not_in_events_subscribers(event_name, subscriber):pass
        else:
            self.events_subscribers[event_name].remove(subscriber)

    def event_remove(self, event_name: str) -> None:
        """
        Remove an event and all its subscribers.

        Args:
            event_name (str): The name of the event to remove.
        """
        if self.Is_not_in_events(event_name):pass
        else:
            #del self.events[event_name]
            self.events.pop(event_name)
            #del self.events_subscribers[event_name]
            self.events_subscribers.pop(event_name)

    def clear(self) -> None:
        """
        Clear all events and subscriptions.
        """
        self.events.clear()
        self.events_subscribers.clear()

    def update(self, event_name, event_content):
        self.events[event_name] = event_content

    def check(self, event_name: str, subscriber: 'Subscriber') -> Any:
        if event_name in self.events:
            if self.Is_not_in_events_subscribers(event_name, subscriber):pass
            else:return self.events[event_name]

    def Is_in_events(self, event_name: str) -> bool:
        if event_name in self.events:
            print('info: this event already exist')
            return True
        return False
    
    def Is_not_in_events(self, event_name: str) -> bool:
        if event_name not in self.events:
            print('info: this event do not exist')
            return True
        return False
        
    def Is_in_events_subscribers(self, event_name: str,subscriber: 'Subscriber') -> bool:
        if subscriber in self.events_subscribers[event_name]:
            print('info: it has already subscribed')
            return True
        return False
    
    def Is_not_in_events_subscribers(self, event_name: str,subscriber: 'Subscriber') -> bool:
        if event_name in self.events:
            if subscriber not in self.events_subscribers[event_name]:
                print(f'info: it is not subscribing ({event_name})')
                return True
        return False


class Publisher:
    """
    Class responsible for publishing events.

    This class can publish events and notify the broker when events occur.
    """

    def __init__(self):
        self.broker = Broker()
        self.events_published = []

    def publish_event(self, event_name: str) -> None:
        """
        Publish a new event.

        Args:
            event_name (str): The name of the event to publish.
            event_content (Any): The content of the event.
        """
        self.events_published.append(event_name)
        self.broker.event_add(event_name)

    def unpublish(self, event_name: str) -> None:
        """
        Unpublish an event.

        Args:
            event_name (str): The name of the event to unpublish.
        """
        if event_name in self.events_published:
            self.events_published.remove(event_name)
            self.broker.event_remove(event_name)
        else:
            print(f'info: {event_name} is not published')

    def update(self, event_name, event_content):
        if event_name in self.events_published:
            self.broker.update(event_name, event_content)
        else:
            print(f'info: {event_name} is not published')

class Subscriber:
    """
    Class responsible for subscribing to and receiving events.

    This class can subscribe to events and receive event notifications.
    """

    def __init__(self):
        self.broker = Broker()
        self.events_subscribed = []

    def subscribe_event(self, event_name: str) -> None:
        """
        Subscribe to an event.

        Args:
            event_name (str): The name of the event to subscribe to.
        """
        if event_name not in self.events_subscribed:
            self.broker.subscriber_add(event_name, self)
            self.events_subscribed.append(event_name)
        else:
            print(f'info: {self} has already subscribed {event_name}')

    def unsubscribe(self, event_name: str) -> None:
        """
        Unsubscribe from an event.

        Args:
            event_name (str): The name of the event to unsubscribe from.
        """
        if event_name in self.events_subscribed:
            self.broker.subscriber_remove(event_name, self)
            self.events_subscribed.remove(event_name)
        else:
            print(f'info: {self} is not subscribing {event_name}')

    def check(self, event_name: str) -> Any:
        """
        Get the content of a received event.

        Args:
            event_name (str): The name of the event to retrieve.

        Returns:
            Optional[Any]: The event content if received, None otherwise.
        """
        if event_name in self.events_subscribed:
            event_content = self.broker.check(event_name, self)
            return event_content
        else:
            print(f'{self} is not subscribing {event_name}')

class InputClass:
    def __init__(self):
        self.publisher = Publisher()
        self.x = 10
        self.publisher.publish_event('x_change')

    def update(self, event_name, event_content):
        self.publisher.update(event_name, event_content)

class OutputClass:
    def __init__(self):
        self.subscriber = Subscriber()
        self.subscriber.subscribe_event('x_change')

    def update(self):
        # type: () -> None
        self.event_content = self.subscriber.check('x_change')
        if self.event_content is not None:
            print(f'x changed to {self.event_content}')

def test() -> None:
    input_class = InputClass()
    output_class = OutputClass()
    
    print("Initial state:")
    output_class.update()
    
    print("\nChanging x value:")
    for event_content in range(3):
        input_class.update('x_change', event_content)
        output_class.update()
    
    print("\nUnsubscribing from 'x_change' event:")
    output_class.subscriber.unsubscribe('x_change')
    input_class.update('x_change', 10)
    output_class.update()
    
    print("\nUnpublishing 'x_change' event:")
    input_class.publisher.unpublish('x_change')
    output_class.update()
    
    print("\nRe-subscribing to 'x_change' event:")
    output_class.subscriber.subscribe_event('x_change')
    input_class.update('x_change', 20)
    output_class.update()
    
    print("\nClearing all events and subscriptions:")
    Broker().clear()
    input_class.update('x_change', 30)
    output_class.update()

if __name__ == "__main__":
    test()
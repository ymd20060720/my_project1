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
"""

from typing import Dict, List, Any, Optional, Callable
import time

class EventError(Exception):
    """Base class for exceptions in this module."""
    pass

class Broker:
    _instance: Optional['Broker'] = None
    events: Dict[str, Any]
    events_subscribers: Dict[str, List['Subscriber']]

    def __new__(cls) -> 'Broker':
        if cls._instance is None:
            cls._instance = super(Broker, cls).__new__(cls)
            cls._instance.events = {}
            cls._instance.events_subscribers = {}
        return cls._instance

    def event_add(self, event_name: str) -> None:
        if event_name not in self.events:
            self.events[event_name] = None
            self.events_subscribers[event_name] = []
        else:
            raise EventError(f"Event '{event_name}' already exists")

    def subscriber_add(self, event_name: str, subscriber: 'Subscriber') -> None:
        if event_name not in self.events:
            raise EventError(f"Event '{event_name}' does not exist")
        if subscriber in self.events_subscribers[event_name]:
            raise EventError(f"Subscriber already subscribed to event '{event_name}'")
        self.events_subscribers[event_name].append(subscriber)

    def subscriber_remove(self, event_name: str, subscriber: 'Subscriber') -> None:
        if event_name not in self.events:
            raise EventError(f"Event '{event_name}' does not exist")
        if subscriber not in self.events_subscribers[event_name]:
            raise EventError(f"Subscriber not subscribed to event '{event_name}'")
        self.events_subscribers[event_name].remove(subscriber)

    def event_remove(self, event_name: str) -> None:
        if event_name not in self.events:
            raise EventError(f"Event '{event_name}' does not exist")
        del self.events[event_name]
        del self.events_subscribers[event_name]

    def clear(self) -> None:
        self.events.clear()
        self.events_subscribers.clear()

    def update(self, event_name: str, event_content: Any) -> None:
        if event_name not in self.events:
            raise EventError(f"Event '{event_name}' does not exist")
        self.events[event_name] = event_content

    def check(self, event_name: str, subscriber: 'Subscriber') -> Any:
        if event_name not in self.events:
            raise EventError(f"Event '{event_name}' does not exist")
        if subscriber not in self.events_subscribers[event_name]:
            raise EventError(f"Subscriber not subscribed to event '{event_name}'")
        return self.events[event_name]

class Publisher:
    broker: Broker
    events_published: List[str]

    def __init__(self) -> None:
        self.broker = Broker()
        self.events_published = []

    def publish_event(self, event_name: str) -> None:
        self.events_published.append(event_name)
        self.broker.event_add(event_name)

    def unpublish(self, event_name: str) -> None:
        if event_name not in self.events_published:
            raise EventError(f"Event '{event_name}' is not published")
        self.events_published.remove(event_name)
        self.broker.event_remove(event_name)

    def update(self, event_name: str, event_content: Any) -> None:
        if event_name not in self.events_published:
            raise EventError(f"Event '{event_name}' is not published")
        self.broker.update(event_name, event_content)

class Subscriber:
    broker: Broker
    events_subscribed: List[str]

    def __init__(self) -> None:
        self.broker = Broker()
        self.events_subscribed = []

    def subscribe_event(self, event_name: str) -> None:
        if event_name in self.events_subscribed:
            raise EventError(f"Already subscribed to event '{event_name}'")
        self.broker.subscriber_add(event_name, self)
        self.events_subscribed.append(event_name)

    def unsubscribe(self, event_name: str) -> None:
        if event_name not in self.events_subscribed:
            raise EventError(f"Not subscribed to event '{event_name}'")
        self.broker.subscriber_remove(event_name, self)
        self.events_subscribed.remove(event_name)

    def check(self, event_name: str) -> Any:
        if event_name not in self.events_subscribed:
            raise EventError(f"Not subscribed to event '{event_name}'")
        return self.broker.check(event_name, self)

class GenericPublisher:
    def __init__(self, event_names: List[str]):
        self.publisher = Publisher()
        for event_name in event_names:
            self.publisher.publish_event(event_name)

    def update(self, event_name: str, event_content: Any) -> None:
        self.publisher.update(event_name, event_content)

    def unpublish(self, event_name: str) -> None:
        self.publisher.unpublish(event_name)

class GenericSubscriber:
    def __init__(self, event_names: List[str], callback: Callable[[str, Any], None]):
        self.subscriber = Subscriber()
        self.callback = callback
        for event_name in event_names:
            self.subscriber.subscribe_event(event_name)

    def update(self) -> None:
        for event_name in self.subscriber.events_subscribed:
            try:
                event_content = self.subscriber.check(event_name)
                self.callback(event_name, event_content)
            except EventError as e:
                print(f"Error: {e}")

    def unsubscribe(self, event_name: str) -> None:
        self.subscriber.unsubscribe(event_name)

def run_tests():
    def clear_broker():
        Broker().clear()

    def test_basic_pub_sub():
        clear_broker()
        print("\n--- Test: Basic Publish-Subscribe ---")
        publisher = GenericPublisher(["test_basic_event1", "test_basic_event2"])
        subscriber = GenericSubscriber(["test_basic_event1", "test_basic_event2"], lambda name, content: print(f"{name}: {content}"))

        publisher.update("test_basic_event1", "Hello")
        publisher.update("test_basic_event2", "World")
        subscriber.update()

    def test_multiple_subscribers():
        clear_broker()
        print("\n--- Test: Multiple Subscribers ---")
        publisher = GenericPublisher(["test_multiple_event"])
        subscriber1 = GenericSubscriber(["test_multiple_event"], lambda name, content: print(f"Subscriber1 - {name}: {content}"))
        subscriber2 = GenericSubscriber(["test_multiple_event"], lambda name, content: print(f"Subscriber2 - {name}: {content}"))

        publisher.update("test_multiple_event", "Broadcast")
        subscriber1.update()
        subscriber2.update()

    def test_unsubscribe():
        clear_broker()
        print("\n--- Test: Unsubscribe ---")
        publisher = GenericPublisher(["test_unsubscribe_event"])
        subscriber = GenericSubscriber(["test_unsubscribe_event"], lambda name, content: print(f"{name}: {content}"))

        publisher.update("test_unsubscribe_event", "Before unsubscribe")
        subscriber.update()

        subscriber.unsubscribe("test_unsubscribe_event")
        publisher.update("test_unsubscribe_event", "After unsubscribe")
        subscriber.update()

    def test_unpublish():
        clear_broker()
        print("\n--- Test: Unpublish ---")
        publisher = GenericPublisher(["test_unpublish_event"])
        subscriber = GenericSubscriber(["test_unpublish_event"], lambda name, content: print(f"{name}: {content}"))

        publisher.update("test_unpublish_event", "Before unpublish")
        subscriber.update()

        publisher.unpublish("test_unpublish_event")
        try:
            publisher.update("test_unpublish_event", "After unpublish")
        except EventError as e:
            print(f"Error: {e}")
        subscriber.update()

    def test_error_handling():
        clear_broker()
        print("\n--- Test: Error Handling ---")
        publisher = GenericPublisher(["test_error_event"])
        subscriber = GenericSubscriber(["test_error_event"], lambda name, content: print(f"{name}: {content}"))

        try:
            publisher.update("non_existent_event", "This should fail")
        except EventError as e:
            print(f"Error: {e}")

        try:
            subscriber.subscriber.subscribe_event("test_error_event")
        except EventError as e:
            print(f"Error: {e}")

    def test_performance():
        clear_broker()
        print("\n--- Test: Performance ---")
        num_events = 10000
        publisher = GenericPublisher([f"test_perf_event_{i}" for i in range(num_events)])
        subscriber = GenericSubscriber([f"test_perf_event_{i}" for i in range(num_events)], lambda name, content: None)

        start_time = time.time()
        for i in range(num_events):
            publisher.update(f"test_perf_event_{i}", i)
        publish_time = time.time() - start_time

        start_time = time.time()
        subscriber.update()
        subscribe_time = time.time() - start_time

        print(f"Time to publish {num_events} events: {publish_time:.4f} seconds")
        print(f"Time to process {num_events} events: {subscribe_time:.4f} seconds")

    # Run all tests
    test_basic_pub_sub()
    test_multiple_subscribers()
    test_unsubscribe()
    test_unpublish()
    test_error_handling()
    test_performance()

if __name__ == "__main__":
    run_tests()

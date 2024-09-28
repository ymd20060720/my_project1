"""
pub_sub.py - A simple publish-subscribe system with tuple events

This module implements a basic publish-subscribe (pub-sub) pattern, allowing for
decoupled communication between publishers and subscribers through a broker.
Events are now represented as tuples: (event_name, event_content).

Classes:
    Broker: Manages events and subscribers
    Publisher: Publishes events
    Subscriber: Subscribes to and receives events
    InputClass: Example class that publishes events
    OutputClass: Example class that subscribes to events

Usage:
    from pub_sub import Publisher, Subscriber, InputClass, OutputClass

    # Create instances
    input_obj = InputClass()
    output_obj = OutputClass()

    # Publish and receive events
    input_obj.change_x(5)
    output_obj.update()
"""

class Broker:
    """
    Singleton class that manages events and subscribers.

    This class is responsible for maintaining a mapping of events to their subscribers
    and notifying subscribers when events occur.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Broker, cls).__new__(cls)
            cls._instance.events_subscribers_dict = dict()
        return cls._instance

    def event_add(self, event_name):
        """
        Add a new event to the broker.

        Args:
            event_name (str): The name of the event to add.
        """
        if event_name not in self.events_subscribers_dict:
            self.events_subscribers_dict[event_name] = set()

    def subscriber_add(self, event_name, subscriber):
        """
        Add a subscriber to an event.

        Args:
            event_name (str): The name of the event to subscribe to.
            subscriber (Subscriber): The subscriber object.
        """
        if event_name not in self.events_subscribers_dict:
            self.event_add(event_name)
        self.events_subscribers_dict[event_name].add(subscriber)

    def notify_subscriber(self, event):
        """
        Notify all subscribers of an event.

        Args:
            event (tuple): A tuple containing (event_name, event_content).
        """
        event_name, _ = event
        if event_name in self.events_subscribers_dict:
            for subscriber in self.events_subscribers_dict[event_name]:
                subscriber.events_received.append(event)

class Publisher:
    """
    Class responsible for publishing events.

    This class can publish events and notify the broker when events occur.
    """

    def __init__(self):
        self.events_published = []
        self.broker = Broker()

    def make_event(self, event_name, event_content):
        return (event_name, event_content)

    def publish_event(self, event):
        """
        Publish a new event.

        Args:
            event (tuple): A tuple containing (event_name, event_content).
        """
        event_name, _ = event
        self.broker.event_add(event_name)
        self.events_published.append(event)

    def notify_broker(self, event):
        """
        Notify the broker that an event has occurred.

        Args:
            event (tuple): A tuple containing (event_name, event_content).
        """
        self.broker.notify_subscriber(event)

class Subscriber:
    """
    Class responsible for subscribing to and receiving events.

    This class can subscribe to events and check if it has received specific events.
    """

    def __init__(self):
        self.events_subscribed = []
        self.events_received = []
        self.broker = Broker()

    def subscribe_event(self, event_name):
        """
        Subscribe to an event.

        Args:
            event_name (str): The name of the event to subscribe to.
        """
        self.broker.subscriber_add(event_name, self)
        self.events_subscribed.append(event_name)

    def check_events_received(self, event_name):
        """
        Check if a specific event has been received.

        Args:
            event_name (str): The name of the event to check.

        Returns:
            tuple or None: The event tuple if received, None otherwise.
        """
        for event in self.events_received:
            if event[0] == event_name:
                self.events_received.remove(event)
                return event
        return None

class InputClass:
    """
    Example class that demonstrates how to use the Publisher.

    This class publishes an 'x_change' event whenever its x attribute is changed.
    """

    def __init__(self):
        self.publisher = Publisher()
        self.x = 10
        self.publisher.publish_event(('x_change', self.x))

    def change_x(self, new_number):
        """
        Change the value of x and notify subscribers.

        Args:
            new_number (int): The new value for x.
        """
        self.x = new_number
        self.publisher.notify_broker(('x_change', self.x))

class OutputClass:
    """
    Example class that demonstrates how to use the Subscriber.

    This class subscribes to the 'x_change' event and updates its state accordingly.
    """

    def __init__(self):
        self.subscriber = Subscriber()
        self.subscriber.subscribe_event('x_change')

    def update(self):
        """
        Check if the 'x_change' event has been received and print a message.
        """
        event = self.subscriber.check_events_received('x_change')
        if event:
            print(f'x changed to {event[1]}')
        else:
            print('x did not change')

def test():
    """
    Test function to demonstrate the usage of the pub-sub system.
    """
    input_class = InputClass()
    output_class = OutputClass()
    output_class.update()
    
    for i in range(5):
        input_class.change_x(i)
        output_class.update()
    output_class.update()

if __name__ == "__main__":
    test()
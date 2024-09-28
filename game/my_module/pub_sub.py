"""
pub_sub.py - A simple publish-subscribe system

This module implements a basic publish-subscribe (pub-sub) pattern, allowing for
decoupled communication between publishers and subscribers through a broker.

Classes:
    (Broker: Manages events and subscribers)
    Publisher: Publishes events
    Subscriber: Subscribes to and receives events

Usage:
    from pub_sub import Publisher, Subscriber

    #in the class you want to use publisher (has a)
    self.publisher = Publisher()

    self.publisher.publish_event(key:str)
    self.notify_broker(key:str)

    #in the class you want to use subscriber (has a)
    self.subscriber = Subscriber()

    self.subscriber.subscribe_event(key:str)
    self.subscriber.check_events_received()
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

    def event_add(self, event):
        """
        Add a new event to the broker.

        Args:
            event (str): The name of the event to add.
        """
        if event not in self.events_subscribers_dict:
            self.events_subscribers_dict[event] = set()

    def subscriber_add(self, event, subscriber):
        """
        Add a subscriber to an event.

        Args:
            event (str): The name of the event to subscribe to.
            subscriber (Subscriber): The subscriber object.
        """
        if event not in self.events_subscribers_dict:
            self.event_add(event)
        self.events_subscribers_dict[event].add(subscriber)

    def notify_subscriber(self, event):
        """
        Notify all subscribers of an event.

        Args:
            event (str): The name of the event that occurred.
        """
        if event in self.events_subscribers_dict:
            for subscriber in self.events_subscribers_dict[event]:
                subscriber.events_received.append(event)

class Publisher:
    """
    Class responsible for publishing events.

    This class can publish events and notify the broker when events occur.
    """

    def __init__(self):
        self.events_published = []
        self.broker = Broker()

    def publish_event(self, event):
        """
        Publish a new event.

        Args:
            event (str): The name of the event to publish.
        """
        self.broker.event_add(event)
        self.events_published.append(event)

    def notify_broker(self, event):
        """
        Notify the broker that an event has occurred.

        Args:
            event (str): The name of the event that occurred.
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

    def subscribe_event(self, event):
        """
        Subscribe to an event.

        Args:
            event (str): The name of the event to subscribe to.
        """
        self.broker.subscriber_add(event, self)
        self.events_subscribed.append(event)

    def check_events_received(self, event):
        """
        Check if a specific event has been received.

        Args:
            event (str): The name of the event to check.

        Returns:
            bool: True if the event was received, False otherwise.
        """
        if event in self.events_received:
            self.events_received.remove(event)
            return True
        else:
            return False

class InputClass:
    """
    Example class that demonstrates how to use the Publisher.

    This class publishes an 'x_change' event whenever its x attribute is changed.
    """

    def __init__(self):
        self.publisher = Publisher()
        self.x = 10
        self.publisher.publish_event('x_change')

    def change_x(self, new_number):
        """
        Change the value of x and notify subscribers.

        Args:
            new_number (int): The new value for x.
        """
        self.x = new_number
        self.publisher.notify_broker('x_change')

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
        if self.subscriber.check_events_received('x_change'):
            print('x changed')
        else:
            print('x did not change')

def test():
    input_class = InputClass()
    output_class = OutputClass()
    output_class.update()
    
    for i in range(10):
        input_class.change_x(3)
        output_class.update()
    output_class.update()

if __name__ == "__main__":
    test()
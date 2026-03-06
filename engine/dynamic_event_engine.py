import json
import random

class DynamicEventEngine:

    def __init__(self, event_file="events/event_library.json"):
        self.event_file = event_file
        self.events = self.load_events()

    def load_events(self):

        try:
            with open(self.event_file, "r") as f:
                return json.load(f)
        except:
            return []

    def choose_event(self, intensity="medium"):

        possible = [e for e in self.events if e["intensity"] == intensity]

        if not possible:
            possible = self.events

        return random.choice(possible)

    def trigger_event(self):

        event = random.choice(self.events)

        return event
import json
import random


class EventEngine:

    def __init__(self, config):

        # Accept either a file path OR a loaded dictionary
        if isinstance(config, str):
            with open(config, "r", encoding="utf-8") as f:
                self.config = json.load(f)

        elif isinstance(config, dict):
            self.config = config

        else:
            raise ValueError("EventEngine requires a file path or dict config")

        self.events = self.config.get("events", [])


    def choose_event(self):

        weighted_events = []

        for event in self.events:

            base_prob = event.get("base_probability", 0.1)

            weighted_events.append((event, base_prob))

        total = sum(w for _, w in weighted_events)

        if total == 0:
            return None

        r = random.uniform(0, total)

        upto = 0

        for event, weight in weighted_events:

            if upto + weight >= r:
                return event

            upto += weight

        return None


    def generate_event(self):

        event = self.choose_event()

        if not event:
            return None

        description = event.get("description", "Something happens.")

        return {
            "type": event.get("type", "generic"),
            "description": description
        }
import random


class EventEngine:

    def __init__(self, event_rules):
        self.rules = event_rules

    def check_for_event(self):

        probability = self.rules["dynamic_events"]["probability_rules"]

        roll = random.random()

        if roll < probability["major_events"]:
            return "major_event"

        elif roll < probability["moderate_events"]:
            return "moderate_event"

        elif roll < probability["low_intensity_events"]:
            return "minor_event"

        return None
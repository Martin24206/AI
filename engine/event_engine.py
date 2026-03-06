import random


class EventEngine:

    def __init__(self, rules):
        self.rules = rules

    def check_for_event(self):

        chance = self.rules["global_event_chance"]

        if random.random() > chance:
            return None

        categories = self.rules["event_categories"]

        category = random.choice(list(categories.keys()))

        event_type = random.choice(
            categories[category]["possible_events"]
        )

        return {
            "category": category,
            "type": event_type,
            "description": f"A {event_type.replace('_',' ')} occurs."
        }
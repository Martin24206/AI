import random


class NarrativeEngine:

    def __init__(self):

        self.active_arcs = []


    def generate_story_arc(self, characters):

        arc_types = [

            "hidden_secret",
            "rivalry",
            "friendship_test",
            "mysterious_event",
            "unexpected_conflict"
        ]

        arc = {
            "type": random.choice(arc_types),
            "stage": 1,
            "participants": random.sample(list(characters.keys()), 2)
        }

        self.active_arcs.append(arc)

        return arc


    def progress_arc(self):

        for arc in self.active_arcs:

            if random.random() < 0.2:

                arc["stage"] += 1

                return arc

        return None
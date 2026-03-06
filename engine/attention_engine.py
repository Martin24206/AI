import random


class AttentionEngine:

    def __init__(self, characters):
        self.characters = characters


    def detect_event_observers(self, event_type):

        observers = []

        for cid, char in self.characters.items():

            awareness = char.get("scene_awareness", {})

            if event_type == "emotional_shift":
                score = awareness.get("emotional_shift_detection", 0)

            elif event_type == "physical_anomaly":
                score = awareness.get("physical_anomaly_detection", 0)

            elif event_type == "magic":
                score = awareness.get("magical_energy_detection", 0)

            else:
                score = awareness.get("environmental_attention", 0)

            roll = random.random()

            if roll < score:
                observers.append(cid)

        return observers
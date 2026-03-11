import random


class MoodEngine:

    def __init__(self, characters):

        self.moods = {}

        for cid in characters:
            self.moods[cid] = "neutral"

    def update_mood(self, char_id):

        moods = ["neutral", "curious", "happy", "serious", "annoyed"]

        if random.random() < 0.2:
            self.moods[char_id] = random.choice(moods)

    def get_mood(self, char_id):

        return self.moods.get(char_id, "neutral")
import random

class PresenceEngine:

    def __init__(self, characters):
        self.characters = characters

    def generate_presence(self, scene_characters):

        presence_actions = []

        for cid, char in scene_characters.items():

            presence_style = char.get("presence_style", {})
            behavior = char.get("behavior", {})

            baseline = presence_style.get("baseline", "neutral")
            spatial = presence_style.get("spatial_behavior", "still")

            action = None

            if baseline == "lively":
                action = random.choice([
                    "shifts position",
                    "leans closer to the group",
                    "looks between everyone curiously"
                ])

            elif baseline == "quiet":
                action = random.choice([
                    "observes quietly",
                    "remains still beside the group",
                    "watches the situation silently"
                ])

            elif baseline == "calm":
                action = random.choice([
                    "stands steadily",
                    "keeps watch over the group",
                    "quietly studies the surroundings"
                ])

            if action:
                presence_actions.append((cid, action))

        return presence_actions
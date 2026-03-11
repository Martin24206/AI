import random


class PresenceEngine:

    def __init__(self, characters):

        self.characters = characters

    def generate_presence(self, chars):

        actions = []

        for cid, char in chars.items():

            name = char["identity"]["name"]

            body_actions = [
                "leans slightly forward",
                "crosses their arms",
                "glances around thoughtfully",
                "tilts their head",
                "smiles faintly",
                "looks slightly confused"
            ]

            action = random.choice(body_actions)

            actions.append((cid, f"{name} {action}."))

        return actions
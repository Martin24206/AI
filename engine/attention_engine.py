import random


class AttentionEngine:

    def __init__(self, characters):
        self.characters = characters

    def get_attentive_characters(self, event_type, scene, characters=None):

        if characters is None:
            characters = self.characters

        reactors = []

        present_characters = scene.get("characters_present", [])

        for char_id in present_characters:

            char = characters.get(char_id)

            if not char:
                continue

            # Skip Rushia Vessel (admin)
            if char["identity"]["id"] == "admin_external_operator":
                continue

            awareness = char.get("awareness", 0.5)

            # Player dialogue attention
            if event_type == "player_dialogue":

                chance = 0.6 + (awareness * 0.3)

                if random.random() < chance:
                    reactors.append(char_id)

            # Event attention
            elif isinstance(event_type, str):

                chance = 0.4 + (awareness * 0.4)

                if random.random() < chance:
                    reactors.append(char_id)

        return reactors
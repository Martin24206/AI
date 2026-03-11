import random


class AttentionEngine:

    def __init__(self, characters):
        self.characters = characters

    def get_attentive_characters(self, event_type, scene, characters=None):

        if characters is None:
            characters = self.characters

        present = scene.get("characters_present", [])
        last_line = scene.get("last_line", "").lower()

        reactors = []

        for char_id in present:

            char = characters.get(char_id)

            if not char:
                continue

            name = char["identity"]["name"]

            # Skip Rushia Vessel (player)
            if char["identity"]["id"] == "admin_external_operator":
                continue

            awareness = char.get("awareness", 0.5)

            # -----------------------------
            # Name mention detection
            # -----------------------------

            first_name = name.split()[0].lower()

            if first_name in last_line:
                reactors.append(char_id)
                continue

            # -----------------------------
            # Normal attention probability
            # -----------------------------

            if event_type == "player_dialogue":

                chance = 0.25 + awareness * 0.35

            else:

                chance = 0.20 + awareness * 0.30

            if random.random() < chance:
                reactors.append(char_id)

        # -----------------------------
        # Limit simultaneous speakers
        # -----------------------------

        if len(reactors) > 2:
            reactors = random.sample(reactors, 2)

        return reactors
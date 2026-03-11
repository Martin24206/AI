import random


class AttentionEngine:

    def __init__(self, characters):
        """
        Initialize the attention system.

        characters: dictionary loaded by CharacterLoader
        """
        self.characters = characters


    def get_attentive_characters(self, event_type, scene, characters):
        """
        Determine which characters notice an event or player dialogue.

        Returns:
            list[str] : character IDs who noticed the event
        """

        attentive_characters = []

        # Characters present in the current scene
        present_characters = scene.get("characters_present", [])

        for char_id in present_characters:

            char = characters[char_id]

            # Skip the player vessel
            if char["identity"]["id"] == "admin_external_operator":
                continue

            # Base attention chance
            attention_chance = 0.5

            personality = char.get("personality", {})

            # Personality modifiers (safe defaults)
            curiosity = personality.get("curiosity", 0.5)
            awareness = personality.get("awareness", 0.5)
            focus = personality.get("focus", 0.5)

            attention_chance += curiosity * 0.2
            attention_chance += awareness * 0.3
            attention_chance += focus * 0.1

            # Player dialogue is slightly more noticeable
            if event_type == "player_dialogue":
                attention_chance += 0.2

            # Clamp probability
            attention_chance = min(attention_chance, 0.95)

            if random.random() < attention_chance:
                attentive_characters.append(char_id)

        # Guarantee at least one reactor if characters are present
        if not attentive_characters and present_characters:
            fallback = random.choice(present_characters)

            # Avoid choosing the player vessel
            if characters[fallback]["identity"]["id"] != "admin_external_operator":
                attentive_characters.append(fallback)

        return attentive_characters
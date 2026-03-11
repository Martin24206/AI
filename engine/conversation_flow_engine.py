import random


class ConversationFlowEngine:

    def __init__(self, characters):
        self.characters = characters


    def choose_next_speaker(self, conversation_history, scene):
        """
        Decide which character should speak next.
        Returns a character ID.
        """

        present_characters = scene.get("characters_present", [])

        if not present_characters:
            return None

        # If no history yet, choose randomly
        if not conversation_history:
            return random.choice(present_characters)

        last_speaker = conversation_history[-1]["speaker"]

        # Remove the last speaker so they don't immediately speak again
        possible_speakers = []

        for char_id in present_characters:

            char = self.characters[char_id]

            if char["identity"]["name"] == last_speaker:
                continue

            if char["identity"]["id"] == "admin_external_operator":
                continue

            possible_speakers.append(char_id)

        if not possible_speakers:
            return None

        return random.choice(possible_speakers)
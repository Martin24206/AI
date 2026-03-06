import json
import os


class CharacterLoader:

    def __init__(self, character_folder="characters"):
        self.character_folder = character_folder
        self.characters = {}

    def load_characters(self):
        for file in os.listdir(self.character_folder):
            if file.endswith(".json"):
                path = os.path.join(self.character_folder, file)

                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                char_id = data["identity"]["id"]
                self.characters[char_id] = data

        return self.characters
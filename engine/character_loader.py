import os
import json


class CharacterLoader:

    def __init__(self, directory):
        self.directory = directory

    def load_characters(self):

        characters = {}

        for filename in os.listdir(self.directory):

            if not filename.endswith(".json"):
                continue

            filepath = os.path.join(self.directory, filename)

            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)

            char_id = data["identity"]["id"]

            characters[char_id] = data

        return characters
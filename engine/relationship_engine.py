import json
import random

class RelationshipEngine:

    def __init__(self, relationship_file="memory/relationship_memory.json"):
        self.relationship_file = relationship_file
        self.relationships = self.load_relationships()

    def load_relationships(self):

        try:
            with open(self.relationship_file, "r") as f:
                return json.load(f)
        except:
            return {}

    def save_relationships(self):

        with open(self.relationship_file, "w") as f:
            json.dump(self.relationships, f, indent=4)

    def update_relationship(self, char_a, char_b, change):

        if char_a not in self.relationships:
            self.relationships[char_a] = {}

        if char_b not in self.relationships[char_a]:
            self.relationships[char_a][char_b] = 0

        self.relationships[char_a][char_b] += change

        self.save_relationships()

    def get_relationship_level(self, char_a, char_b):

        return self.relationships.get(char_a, {}).get(char_b, 0)

    def influence_dialogue(self, char_a, char_b):

        level = self.get_relationship_level(char_a, char_b)

        if level > 5:
            return "warm"

        elif level < -3:
            return "cold"

        else:
            return "neutral"
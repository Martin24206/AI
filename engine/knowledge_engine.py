class KnowledgeEngine:

    def __init__(self, canon_file):

        import json

        with open(canon_file, "r", encoding="utf-8") as f:
            self.canon = json.load(f)

        self.learned_world_facts = []

    # -------------------------
    # Canon knowledge
    # -------------------------

    def character_knows(self, character_id, fact):

        char_data = self.canon.get("characters", {}).get(character_id, {})

        known_facts = char_data.get("known_facts", [])

        return fact in known_facts

    # -------------------------
    # Learn new information
    # -------------------------

    def teach_world_fact(self, fact):

        if fact not in self.learned_world_facts:
            self.learned_world_facts.append(fact)

    # -------------------------
    # Retrieve knowledge
    # -------------------------

    def get_known_world_facts(self):

        return self.learned_world_facts
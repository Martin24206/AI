import random


class ConversationFlowEngine:

    def __init__(self, characters):

        self.characters = characters
        self.last_speaker = None


    def get_talk_weight(self, character):

        personality = character.get("personality", {})
        traits = personality.get("traits", [])

        weight = 1.0

        if "quiet" in traits:
            weight -= 0.4

        if "observant" in traits:
            weight -= 0.2

        if "playful" in traits:
            weight += 0.4

        return max(weight, 0.1)


    def choose_next_speaker(self, history, scene):

        present = scene["characters_present"]

        candidates = []

        for cid in present:

            char = self.characters[cid]
            name = char["identity"]["name"]

            if name == self.last_speaker:
                continue

            weight = self.get_talk_weight(char)

            candidates.append((cid, weight))

        if not candidates:
            return None

        total = sum(w for _, w in candidates)

        r = random.uniform(0, total)

        upto = 0

        for cid, weight in candidates:

            if upto + weight >= r:
                self.last_speaker = self.characters[cid]["identity"]["name"]
                return cid

            upto += weight

        if not candidates:
             return random.choice(scene["characters_present"])
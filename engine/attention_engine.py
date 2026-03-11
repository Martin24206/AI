import random


class AttentionEngine:

    def __init__(self, characters):
        self.characters = characters


    def attention_score(self, character):

        score = 0.4

        # -----------------
        # Scene awareness
        # -----------------

        scene_awareness = character.get("scene_awareness", {})

        if isinstance(scene_awareness, dict):

            level = scene_awareness.get("perception_level", "medium")

            mapping = {
                "very high": 0.6,
                "high": 0.5,
                "medium": 0.35,
                "low": 0.2
            }

            score += mapping.get(level.lower(), 0.3)

        # -----------------
        # Personality traits
        # -----------------

        personality = character.get("personality", {})
        traits = personality.get("traits", [])

        if "observant" in traits:
            score += 0.3

        if "carefree" in traits:
            score -= 0.1

        return max(0.1, min(score, 0.95))


    def get_attentive_characters(self, event_type, scene, characters):

        observers = []

        present = scene.get("characters_present", [])

        for cid in present:

            char = characters[cid]

            score = self.attention_score(char)

            if random.random() < score:
                observers.append(cid)

        return observers
import random
from engine.attention_engine import AttentionEngine


class SceneManager:

    def __init__(self, characters):

        self.characters = characters
        self.attention_engine = AttentionEngine(characters)

        self.active_scene = {
            "location": None,
            "characters_present": [],
            "recent_events": []
        }


    # ------------------------------
    # Scene Setup
    # ------------------------------

    def set_scene(self, location, characters_present):

        self.active_scene["location"] = location
        self.active_scene["characters_present"] = characters_present
        self.active_scene["recent_events"] = []


    # ------------------------------
    # Event Handling
    # ------------------------------

    def trigger_event(self, event):

        self.active_scene["recent_events"].append(event)

        observers = self.detect_observers(event)

        reactors = self.choose_event_reactors(observers)

        return {
            "event": event,
            "observers": observers,
            "reactors": reactors
        }


    # ------------------------------
    # Attention Detection
    # ------------------------------

    def detect_observers(self, event):

        event_type = event.get("type", "environment")
        intensity = event.get("intensity", 0.5)

        scene_characters = {
            cid: self.characters[cid]
            for cid in self.active_scene["characters_present"]
        }

        temp_attention = AttentionEngine(scene_characters)

        observers = temp_attention.detect_event_observers(event_type)

        if intensity >= 0.8:
            return list(scene_characters.keys())

        return observers


    # ------------------------------
    # Reaction Selection
    # ------------------------------

    def choose_event_reactors(self, observers):

        if observers:
            return observers

        return random.sample(
            self.active_scene["characters_present"],
            min(2, len(self.active_scene["characters_present"]))
        )


    # ------------------------------
    # Dialogue Selection
    # ------------------------------

    def choose_next_speaker(self, history):

        present = self.active_scene["characters_present"]

        if not present:
            return None

        # reply behavior
        if history:

            last_speaker = history[-1]["speaker"]

            # characters often reply to who spoke
            possible = [
                cid for cid in present
                if self.characters[cid]["identity"]["name"] != last_speaker
            ]

            if possible and random.random() < 0.7:
                return random.choice(possible)

        return random.choice(present)
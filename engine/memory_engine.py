import json
import os


class MemoryEngine:

    def __init__(self, memory_folder="memory"):

        self.memory_folder = memory_folder

        self.dialogue_log = []
        self.event_log = []

        # limits (important for long simulations)
        self.max_dialogue_memory = 60
        self.max_event_memory = 40

        os.makedirs(memory_folder, exist_ok=True)

        self.dialogue_file = os.path.join(memory_folder, "dialogue_memory.json")
        self.event_file = os.path.join(memory_folder, "event_memory.json")

        self.load_memory()

    # -------------------------
    # Load memory from disk
    # -------------------------

    def load_memory(self):

        if os.path.exists(self.dialogue_file):

            with open(self.dialogue_file, "r", encoding="utf-8") as f:
                self.dialogue_log = json.load(f)

        if os.path.exists(self.event_file):

            with open(self.event_file, "r", encoding="utf-8") as f:
                self.event_log = json.load(f)

    # -------------------------
    # Save memory to disk
    # -------------------------

    def save_memory(self):

        with open(self.dialogue_file, "w", encoding="utf-8") as f:
            json.dump(self.dialogue_log, f, indent=2)

        with open(self.event_file, "w", encoding="utf-8") as f:
            json.dump(self.event_log, f, indent=2)

    # -------------------------
    # Dialogue memory
    # -------------------------

    def remember_dialogue(self, speaker, line):

        entry = {
            "speaker": speaker,
            "line": line
        }

        self.dialogue_log.append(entry)

        if len(self.dialogue_log) > self.max_dialogue_memory:
            self.summarize_dialogue_memory()

        self.save_memory()

    def recall_recent_dialogue(self, amount=10):

        return self.dialogue_log[-amount:]

    # -------------------------
    # Event memory
    # -------------------------

    def remember_event(self, event):

        entry = {
            "event": event
        }

        self.event_log.append(entry)

        if len(self.event_log) > self.max_event_memory:
            self.event_log.pop(0)

        self.save_memory()

    def recall_recent_events(self, amount=10):

        return self.event_log[-amount:]

    # Compatibility for your main.py
    def recall_events(self):

        return self.recall_recent_events()

    # -------------------------
    # Memory summarization
    # -------------------------

    def summarize_dialogue_memory(self):

        if len(self.dialogue_log) < 20:
            return

        summary = {
            "type": "summary",
            "content": f"{len(self.dialogue_log)} lines of conversation happened earlier."
        }

        self.event_log.append(summary)

        # keep only latest part
        self.dialogue_log = self.dialogue_log[-20:]

    # -------------------------
    # Clear memory (admin tool)
    # -------------------------

    def clear_memory(self):

        self.dialogue_log = []
        self.event_log = []

        self.save_memory()
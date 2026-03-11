class MemoryEngine:

    def __init__(self):

        # long-term event memories
        self.event_memories = []

        # recent dialogue memory
        self.dialogue_memories = []

        # max dialogue memory stored
        self.max_dialogue_memory = 50


    def remember(self, event):

        memory_entry = {
            "type": "event",
            "content": event
        }

        self.event_memories.append(memory_entry)


    def remember_dialogue(self, speaker, line):

        memory_entry = {
            "type": "dialogue",
            "speaker": speaker,
            "line": line
        }

        self.dialogue_memories.append(memory_entry)

        # keep memory size limited
        if len(self.dialogue_memories) > self.max_dialogue_memory:
            self.dialogue_memories.pop(0)


    def recall_recent_dialogue(self, count=5):

        return self.dialogue_memories[-count:]


    def recall_events(self):

        return self.event_memories
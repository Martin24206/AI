class MemoryEngine:

    def __init__(self):
        self.shared_memory = []

    def remember(self, event):

        self.shared_memory.append(event)

    def recall_recent(self, n=5):

        return self.shared_memory[-n:]
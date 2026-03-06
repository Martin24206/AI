import random

class ConversationFlowEngine:

    def __init__(self, characters):
        self.characters = characters

    def choose_next_speaker(self, current_speaker, participants):

        possible = [c for c in participants if c != current_speaker]

        weighted = []

        for cid in possible:

            char = self.characters[cid]

            freq = char.get("behavior", {}).get("speech_frequency", "medium")

            if freq == "high":
                weight = 3
            elif freq == "medium":
                weight = 2
            else:
                weight = 1

            weighted.extend([cid] * weight)

        return random.choice(weighted)

    def generate_conversation_order(self, participants, turns=5):

        order = []

        current = random.choice(participants)

        order.append(current)

        for _ in range(turns - 1):

            next_speaker = self.choose_next_speaker(current, participants)

            order.append(next_speaker)

            current = next_speaker

        return order
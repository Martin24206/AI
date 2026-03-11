import random


class GoalEngine:

    def __init__(self, characters):

        self.goals = {}

        for cid in characters:

            self.goals[cid] = self.generate_goal()

    def generate_goal(self):

        goals = [
            "protect a friend",
            "discover a hidden truth",
            "avoid suspicion",
            "strengthen a friendship",
            "prove themselves",
            "hide a secret"
        ]

        return random.choice(goals)

    def get_goal(self, char_id):

        return self.goals.get(char_id)

    def update_goal(self, char_id):

        if random.random() < 0.1:

            self.goals[char_id] = self.generate_goal()
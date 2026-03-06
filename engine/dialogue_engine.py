class DialogueEngine:

    def __init__(self):
        pass

    def generate_line(self, character, context):

        name = character["identity"]["name"]

        # temporary simple behavior
        return f"{name} reacts to the situation."
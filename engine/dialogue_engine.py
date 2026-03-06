import requests


class DialogueEngine:

    def __init__(self):
        self.url = "http://localhost:11434/api/generate"
        self.model = "llama3"

    def generate_line(self, character, context, scene):

        name = character["identity"]["name"]
        personality = character.get("personality", "neutral")

        location = scene.get("location", "unknown")

        # -------------------------
        # Build conversation history
        # -------------------------

        history_text = ""

        for entry in context[-10:]:  # last 10 lines only
            speaker = entry["speaker"]
            line = entry["line"]

            history_text += f"{speaker}: {line}\n"


        # -------------------------
        # Prompt
        # -------------------------

        prompt = f"""
You are roleplaying as {name} inside a living world simulation.

Location: {location}

Personality:
{personality}

Rushia Vessel is an external admin presence observing the world.
Some characters may notice them, some may ignore them.

Recent conversation:
{history_text}

Rules:
- Speak naturally
- One short sentence
- Stay in character
- React to the conversation
- Do not narrate actions
- Do not describe thoughts
- Do not speak for other characters

{name}:
"""


        try:

            response = requests.post(
                self.url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                }
            )

            data = response.json()

            line = data.get("response", "").strip()

            # prevent long responses
            line = line.split("\n")[0]

            if len(line) > 200:
                line = line[:200]

            return line

        except Exception:
            return f"... ({name} cannot respond)"
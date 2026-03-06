import requests


class DialogueEngine:

    def __init__(self):
        self.url = "http://localhost:11434/api/generate"
        self.model = "qwen2.5:7b"

    def generate_line(self, character, history, scene):

        name = character["identity"]["name"]
        personality = character.get("personality", "neutral")
        location = scene.get("location", "unknown")

        # -------------------------
        # Build conversation history
        # -------------------------

        history_text = ""
        last_speaker = None

        for entry in history[-10:]:  # last 10 lines
            speaker = entry["speaker"]
            line = entry["line"]

            history_text += f"{speaker}: {line}\n"
            last_speaker = speaker

        # -------------------------
        # Special admin awareness
        # -------------------------

        admin_context = ""

        if last_speaker == "Rushia Vessel":
            admin_context = """
The last speaker was Rushia Vessel, an external observer/admin.
Characters who notice them may respond or acknowledge them naturally.
"""

        # -------------------------
        # Prompt
        # -------------------------

        prompt = f"""
You are roleplaying as {name} in a living character world simulation.

Location: {location}

Personality:
{personality}

{admin_context}

Recent conversation:
{history_text}

Rules:
- Speak naturally
- One short sentence
- Stay in character
- Respond to the last speaker if appropriate
- Do not narrate actions
- Do not describe thoughts
- Do not speak for other characters
- Do not explain things like an AI

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

            # prevent weird long output
            line = line.split("\n")[0]

            if len(line) > 200:
                line = line[:200]

            return line

        except Exception:
            return f"... ({name} cannot respond)"
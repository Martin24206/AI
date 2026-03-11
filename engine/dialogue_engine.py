import requests


class DialogueEngine:

    def __init__(self):
        self.url = "http://localhost:11434/api/generate"
        self.model = "qwen2.5:7b"

    def generate_line(
        self,
        character,
        history,
        scene,
        recent_memories=None,
        event_memories=None
    ):

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
        # Memory Context
        # -------------------------

        memory_context = ""

        if recent_memories:
            memory_context += "\nRecent memories:\n"
            for mem in recent_memories[-5:]:
                speaker = mem.get("speaker", "")
                line = mem.get("line", "")
                memory_context += f"{speaker} said earlier: {line}\n"

        if event_memories:
            memory_context += "\nPast events remembered:\n"
            for event in event_memories[-3:]:
                content = event.get("content", "")
                memory_context += f"- {content}\n"

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

{memory_context}

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
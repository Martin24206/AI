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
        # Conversation History
        # -------------------------

        history_text = ""
        last_speaker = None

        for entry in history[-10:]:

            speaker = entry["speaker"]
            line = entry["line"]

            history_text += f"{speaker}: {line}\n"
            last_speaker = speaker

        # -------------------------
        # Memory Context
        # -------------------------

        memory_context = ""

        if recent_memories:

            memory_context += "\nRelevant past conversations:\n"

            for mem in recent_memories[-5:]:

                speaker = mem.get("speaker", "")
                line = mem.get("line", "")

                memory_context += f"{speaker} said: {line}\n"

        if event_memories:

            memory_context += "\nImportant past events:\n"

            for event in event_memories[-3:]:

                content = event.get("content", "")

                memory_context += f"- {content}\n"

        # -------------------------
        # Admin Awareness
        # -------------------------

        admin_context = ""

        if last_speaker == "Rushia Vessel":

            admin_context = """
Rushia Vessel is an external observer/admin interacting with the world.
You may respond to them naturally.
"""

        # -------------------------
        # Prompt
        # -------------------------

        prompt = f"""
You are {name} in a living character world simulation.

Location: {location}

Personality:
{personality}

{admin_context}

{memory_context}

The last speaker was: {last_speaker}

Conversation so far:
{history_text}

If greetings already happened earlier, do not greet again.

Speak naturally as {name}.
Respond to the last speaker if appropriate.

Write ONE short sentence of dialogue.

{name} says:
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

            line = line.split("\n")[0]

            # -------------------------
            # Remove narration artifacts
            # -------------------------

            bad_phrases = [
                "says,",
                "said,",
                "remarked,",
                "replied,",
                "nodding",
                "smiling",
                "looking"
            ]

            for phrase in bad_phrases:

                if phrase in line.lower():

                    parts = line.split('"')

                    if len(parts) >= 2:
                        line = parts[1]

            line = line.strip()

            # limit length
            if len(line) > 160:
                line = line[:160]

            return line

        except Exception:

            return f"... ({name} cannot respond)"
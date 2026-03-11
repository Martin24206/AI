
import requests


class DialogueEngine:

    def __init__(self):

        self.endpoint = "http://localhost:11434/api/generate"
        self.model = "llama3"


    def generate_line(
        self,
        character,
        history,
        scene,
        recent_memories=None,
        event_memories=None,
        mood=None,
        action=None,
        relationship=None,
        world_knowledge=None
    ):

        name = character["identity"]["name"]
        personality = character["personality"]["description"]

        location = scene["location"]

        history_text = ""

        for h in history[-8:]:
            history_text += f'{h["speaker"]}: {h["line"]}\n'


        mood_text = f"Current mood: {mood}" if mood else ""
        action_text = f"Body language: {action}" if action else ""
        relationship_text = f"Tone toward others: {relationship}" if relationship else ""

        knowledge_text = ""

        if world_knowledge:

            knowledge_text = "Known world facts:\n"

            for fact in world_knowledge[-5:]:
                knowledge_text += f"- {fact}\n"


        prompt = f"""
You are {name} inside a living character simulation.

Location: {location}

{mood_text}
{action_text}
{relationship_text}

Personality:
{personality}

{knowledge_text}

Conversation:
{history_text}

Speak naturally as {name}.
Write ONE line of dialogue.

{name}:
"""


        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }

        response = requests.post(self.endpoint, json=payload)

        text = response.json()["response"]

        text = text.replace(f"{name}:", "")
        text = text.replace(f"{name} says:", "")

        return text.strip()
import json

from engine.character_loader import CharacterLoader
from engine.scene_manager import SceneManager
from engine.event_engine import EventEngine
from engine.memory_engine import MemoryEngine
from engine.dialogue_engine import DialogueEngine


# Load characters
loader = CharacterLoader()
characters = loader.load_characters()


# Load world rules
with open("world_system/dynamic_event_engine.json") as f:
    event_rules = json.load(f)


scene = SceneManager(characters, {})
events = EventEngine(event_rules)
memory = MemoryEngine()
dialogue = DialogueEngine()


print("Scene started.\n")

for i in range(10):

    event = events.check_for_event()

    if event:
        print(f"[EVENT TRIGGERED: {event}]")
        memory.remember(event)

    speaker_id = scene.select_next_speaker()
    character = characters[speaker_id]

    line = dialogue.generate_line(character, scene.get_recent_scene())

    scene.record_line(speaker_id, line)

    print(f"{character['identity']['name']}: {line}")
import json

from engine.character_loader import CharacterLoader
from engine.scene_manager import SceneManager
from engine.event_engine import EventEngine
from engine.memory_engine import MemoryEngine
from engine.dialogue_engine import DialogueEngine


# -----------------------------
# Load Characters
# -----------------------------

loader = CharacterLoader("characters/main_cast")
characters = loader.load_characters()


# -----------------------------
# Load Event Rules
# -----------------------------

with open("world_system/dynamic_event_engine.json") as f:
    event_rules = json.load(f)


scene = SceneManager(characters)
events = EventEngine(event_rules)
memory = MemoryEngine()
dialogue = DialogueEngine()


# -----------------------------
# Conversation Memory
# -----------------------------

conversation_history = []


# -----------------------------
# Start Scene
# -----------------------------

scene.set_scene(
    location="school_road",
    characters_present=list(characters.keys())
)

print("Scene started.\n")


# -----------------------------
# Main Simulation Loop
# -----------------------------

while True:

    # -------------------------
    # User Input (Optional)
    # -------------------------

    user_input = input("You (Rushia Vessel, enter to skip): ")

    if user_input.strip() != "":
        conversation_history.append({
            "speaker": "Rushia Vessel",
            "line": user_input
        })

    # -------------------------
    # Event Check
    # -------------------------

    event = events.check_for_event()

    if event:
        print(f"[EVENT TRIGGERED: {event}]")

        memory.remember(event)

        event_result = scene.trigger_event(event)

        for reactor in event_result["reactors"]:
            char = characters[reactor]

            line = dialogue.generate_line(
                char,
                conversation_history,
                scene.active_scene
            )

            print(f'{char["identity"]["name"]}: {line}')

            conversation_history.append({
                "speaker": char["identity"]["name"],
                "line": line
            })

        continue


    # -------------------------
    # Choose Speaker
    # -------------------------

    speaker_id = scene.choose_next_speaker(conversation_history)

    if not speaker_id:
        continue

    character = characters[speaker_id]

    line = dialogue.generate_line(
        character,
        conversation_history,
        scene.active_scene
    )

    print(f'{character["identity"]["name"]}: {line}')

    conversation_history.append({
        "speaker": character["identity"]["name"],
        "line": line
    })
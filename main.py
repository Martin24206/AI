import json
import time

from engine.character_loader import CharacterLoader
from engine.scene_manager import SceneManager
from engine.event_engine import EventEngine
from engine.memory_engine import MemoryEngine
from engine.dialogue_engine import DialogueEngine
from engine.attention_engine import AttentionEngine
from engine.conversation_flow_engine import ConversationFlowEngine
from engine.knowledge_engine import KnowledgeEngine
from engine.mood_engine import MoodEngine
from engine.presence_engine import PresenceEngine
from engine.relationship_engine import RelationshipEngine
from engine.goal_engine import GoalEngine
from engine.narrative_engine import NarrativeEngine

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


# -----------------------------
# Initialize Systems
# -----------------------------

scene = SceneManager(characters)
events = EventEngine(event_rules)
memory = MemoryEngine()

dialogue = DialogueEngine()
attention = AttentionEngine(characters)
flow = ConversationFlowEngine(characters)

knowledge = KnowledgeEngine("world_system/canon_loader.json")
mood = MoodEngine(characters)
presence = PresenceEngine(characters)
relationships = RelationshipEngine()

goals = GoalEngine(characters)
narrative = NarrativeEngine()
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

    user_input = input("You (Rushia Vessel, enter to skip): ")

    # -------------------------
    # Admin Command
    # -------------------------

    if user_input.startswith("/teach"):

        fact = user_input.replace("/teach", "").strip()

        knowledge.teach_world_fact(fact)

        print(f"[WORLD FACT LEARNED: {fact}]")

        continue


    # -------------------------
    # Player Dialogue
    # -------------------------

    if user_input.strip() != "":

        conversation_history.append({
            "speaker": "Rushia Vessel",
            "line": user_input
        })

        memory.remember_dialogue(
            "Rushia Vessel",
            user_input
        )

        reactors = attention.get_attentive_characters(
            event_type="player_dialogue",
            scene=scene.active_scene,
            characters=characters
        )

        for char_id in reactors:

            char = characters[char_id]

            if char["identity"]["id"] == "admin_external_operator":
                continue

            mood.update_mood(char_id)
            current_mood = mood.get_mood(char_id)

            actions = presence.generate_presence({char_id: char})
            action_text = actions[0][1] if actions else ""

            relationship_context = ""

            if conversation_history:

                last_speaker = conversation_history[-1]["speaker"]

                for cid, char_data in characters.items():

                    if char_data["identity"]["name"] == last_speaker:

                        relationship_context = relationships.influence_dialogue(
                            char_id,
                            cid
                        )

            line = dialogue.generate_line(
                char,
                conversation_history,
                scene.active_scene,
                memory.recall_recent_dialogue(),
                memory.recall_recent_events(),
                mood=current_mood,
                action=action_text,
                relationship=relationship_context,
                world_knowledge=knowledge.get_known_world_facts()
            )

            print(f'{char["identity"]["name"]}: {line}')

            conversation_history.append({
                "speaker": char["identity"]["name"],
                "line": line
            })

            memory.remember_dialogue(
                char["identity"]["name"],
                line
            )

        continue


    # -------------------------
    # Event Check
    # -------------------------

    event = events.check_for_event()

    if event:

        print(f"[EVENT TRIGGERED: {event}]")

        memory.remember_event(event)

        continue


    # -------------------------
    # AI Conversation
    # -------------------------

    speaker_id = flow.choose_next_speaker(
        conversation_history,
        scene.active_scene
    )

    if not speaker_id:
        continue

    character = characters[speaker_id]

    if character["identity"]["id"] == "admin_external_operator":
        continue

    mood.update_mood(speaker_id)
    current_mood = mood.get_mood(speaker_id)

    actions = presence.generate_presence({speaker_id: character})
    action_text = actions[0][1] if actions else ""

    line = dialogue.generate_line(
        character,
        conversation_history,
        scene.active_scene,
        memory.recall_recent_dialogue(),
        memory.recall_recent_events(),
        mood=current_mood,
        action=action_text,
        world_knowledge=knowledge.get_known_world_facts()
    )

    print(f'{character["identity"]["name"]}: {line}')

    conversation_history.append({
        "speaker": character["identity"]["name"],
        "line": line
    })

    memory.remember_dialogue(
        character["identity"]["name"],
        line
    )

    time.sleep(1)
"""
setup_dialogflow.py
Automates the creation of Aarogya Saathi's Dialogflow CX Agent,
Entity Types, and Intents using the provided service account JSON key.
"""
import sys
import io
# Force UTF-8 output on Windows to avoid cp1252 errors
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import os
import csv
from google.cloud import dialogflowcx_v3beta1 as dialogflow
from google.api_core.exceptions import AlreadyExists, PermissionDenied

# ── Credentials ────────────────────────────────────────────────────────────────
KEY_PATH = r"e:\BrainOVision_Hackathon\aarogya-saathi-cbkb-e7b6a5333579.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = KEY_PATH

# ── Project Config ─────────────────────────────────────────────────────────────
PROJECT_ID  = "aarogya-saathi-cbkb"
LOCATION    = "global"
AGENT_DISPLAY_NAME = "Aarogya Saathi"
LANGUAGE   = "en"
TIME_ZONE  = "Asia/Kolkata"

# ── Local Data ─────────────────────────────────────────────────────────────────
BASE_DIR     = r"e:\BrainOVision_Hackathon\dialogflow"
ENTITIES_DIR = os.path.join(BASE_DIR, "entities")
INTENTS_DIR  = os.path.join(BASE_DIR, "intents")

# ── Helper: Client Options ─────────────────────────────────────────────────────
def _client_options(location):
    if location != "global":
        return {"api_endpoint": f"{location}-dialogflow.googleapis.com:443"}
    return None


# ── Step 1: Get or Create Agent ────────────────────────────────────────────────
def get_or_create_agent():
    client = dialogflow.AgentsClient(client_options=_client_options(LOCATION))
    parent = f"projects/{PROJECT_ID}/locations/{LOCATION}"

    # Try listing first (may 403 if SA lacks permission)
    try:
        for agent in client.list_agents(request={"parent": parent}):
            if agent.display_name == AGENT_DISPLAY_NAME:
                print(f"[OK] Found existing agent: {agent.name}")
                return agent.name
    except PermissionDenied:
        print("[WARN] Cannot list agents (IAM). Will try create directly.")
    except Exception as e:
        print(f"[WARN] list_agents error: {e}")

    # Try creating
    agent_obj = dialogflow.Agent(
        display_name=AGENT_DISPLAY_NAME,
        default_language_code=LANGUAGE,
        time_zone=TIME_ZONE,
    )
    try:
        created = client.create_agent(
            request=dialogflow.CreateAgentRequest(parent=parent, agent=agent_obj)
        )
        print(f"[OK] Created agent: {created.name}")
        return created.name
    except AlreadyExists:
        # Derive name from the list request ResourceExhausted metadata or pattern.
        # Dialogflow CX always names created resources predictably; if we land
        # here the agent already exists — we just can't read its UUID.  Ask the
        # user to paste it or try get by display name via search.
        print("[WARN] Agent already exists but we lack list permission to read its ID.")
        # Fallback: ask user / check env
        agent_id = os.getenv("DIALOGFLOW_AGENT_ID")
        if agent_id:
            agent_path = f"{parent}/agents/{agent_id}"
            print(f"[OK] Using DIALOGFLOW_AGENT_ID from env: {agent_path}")
            return agent_path
        print("[ERROR] Set the environment variable DIALOGFLOW_AGENT_ID to your agent UUID and re-run.")
        return None
    except Exception as e:
        print(f"[ERROR] create_agent failed: {e}")
        return None


# ── Step 2: Upload Entity Types ────────────────────────────────────────────────
def upload_entities(agent_name):
    client = dialogflow.EntityTypesClient(client_options=_client_options(LOCATION))

    for filename in os.listdir(ENTITIES_DIR):
        if not filename.endswith(".csv"):
            continue

        entity_display_name = filename[:-4]  # strip .csv → 'disease' / 'symptom'
        filepath = os.path.join(ENTITIES_DIR, filename)

        entities = []
        with open(filepath, encoding="utf-8") as f:
            reader = csv.reader(f)
            headers = next(reader, None)  # skip header row
            for row in reader:
                row = [c.strip() for c in row if c.strip()]
                if not row:
                    continue
                value    = row[0]
                synonyms = row[1:] if len(row) > 1 else [value]
                entities.append(
                    dialogflow.EntityType.Entity(value=value, synonyms=synonyms)
                )

        if not entities:
            print(f"[SKIP] No entities found in {filename}")
            continue

        entity_type = dialogflow.EntityType(
            display_name=entity_display_name,
            kind=dialogflow.EntityType.Kind.KIND_MAP,
            entities=entities,
        )
        try:
            created = client.create_entity_type(
                request=dialogflow.CreateEntityTypeRequest(
                    parent=agent_name, entity_type=entity_type
                )
            )
            print(f"[OK] Entity '{entity_display_name}' created → {created.name}")
        except AlreadyExists:
            print(f"[SKIP] Entity '{entity_display_name}' already exists.")
        except Exception as e:
            print(f"[ERROR] Entity '{entity_display_name}': {e}")


# ── Step 3: Upload Intents ─────────────────────────────────────────────────────
def upload_intents(agent_name):
    client = dialogflow.IntentsClient(client_options=_client_options(LOCATION))

    for filename in os.listdir(INTENTS_DIR):
        if not filename.endswith(".txt"):
            continue

        # e.g. 'disease_information.txt' → 'Disease Information'
        intent_display_name = filename[:-4].replace("_", " ").title()
        filepath = os.path.join(INTENTS_DIR, filename)

        training_phrases = []
        with open(filepath, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                part   = dialogflow.Intent.TrainingPhrase.Part(text=line)
                phrase = dialogflow.Intent.TrainingPhrase(
                    parts=[part], repeat_count=1
                )
                training_phrases.append(phrase)

        if not training_phrases:
            print(f"[SKIP] No training phrases in {filename}")
            continue

        intent = dialogflow.Intent(
            display_name=intent_display_name,
            training_phrases=training_phrases,
        )
        try:
            created = client.create_intent(
                request=dialogflow.CreateIntentRequest(
                    parent=agent_name,
                    intent=intent,
                    language_code=LANGUAGE,
                )
            )
            print(f"[OK] Intent '{intent_display_name}' created → {created.name}")
        except AlreadyExists:
            print(f"[SKIP] Intent '{intent_display_name}' already exists.")
        except Exception as e:
            print(f"[ERROR] Intent '{intent_display_name}': {e}")


# ── Main ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("  Aarogya Saathi -- Dialogflow CX Setup")
    print("=" * 60)

    agent_name = get_or_create_agent()
    if not agent_name:
        raise SystemExit("[FATAL] Could not resolve an agent. Exiting.")

    print()
    print("── Uploading Entity Types ──────────────────────────────────")
    upload_entities(agent_name)

    print()
    print("-- Uploading Intents -----------------------------------------------")
    upload_intents(agent_name)

    print()
    print("=" * 60)
    print("[DONE] Dialogflow CX agent setup complete!")
    print(f"       Agent resource name: {agent_name}")
    print()
    print("  Next step: copy the UUID from the agent name and add")
    print("  it to your .env file as:")
    print("    DIALOGFLOW_PROJECT_ID=aarogya-saathi-cbkb")
    print(f"    DIALOGFLOW_LOCATION={LOCATION}")
    print("    DIALOGFLOW_AGENT_ID=<uuid from agent_name>")
    print("=" * 60)

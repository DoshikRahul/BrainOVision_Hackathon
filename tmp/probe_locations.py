import os
from google.cloud import dialogflowcx_v3beta1 as dialogflow
from google.api_core.exceptions import PermissionDenied

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"e:\BrainOVision_Hackathon\aarogya-saathi-cbkb-e7b6a5333579.json"

PROJECT_ID = "aarogya-saathi-cbkb"
LOCATIONS = ["global", "us-central1", "us-east1", "europe-west1", "asia-south1", "asia-northeast1", "asia-southeast1"]

results = {}
for loc in LOCATIONS:
    client_options = None
    if loc != "global":
        client_options = {"api_endpoint": f"{loc}-dialogflow.googleapis.com:443"}
    
    try:
        client = dialogflow.AgentsClient(client_options=client_options)
        parent = f"projects/{PROJECT_ID}/locations/{loc}"
        agents = list(client.list_agents(request={"parent": parent}))
        if agents:
            for a in agents:
                results[loc] = f"FOUND: {a.display_name} -> {a.name}"
        else:
            results[loc] = "EMPTY: no agents"
    except PermissionDenied:
        results[loc] = "403: permission denied (agents.list)"
    except Exception as e:
        results[loc] = f"ERR: {str(e)[:80]}"

for loc, r in results.items():
    print(f"{loc:20s}: {r}")

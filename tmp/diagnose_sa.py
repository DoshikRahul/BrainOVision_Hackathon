"""
Diagnose what IAM roles the SA actually has by trying different operations.
"""
import os
from google.cloud import dialogflowcx_v3beta1 as dialogflow
from google.api_core.exceptions import PermissionDenied, NotFound

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"e:\BrainOVision_Hackathon\aarogya-saathi-cbkb-e7b6a5333579.json"

PROJECT_ID = "aarogya-saathi-cbkb"

# The SA client email has project id "aarogya-saathi-cbkb" — detect intent
# requires an existing agent. Let's try a session ping on us-central1 since 
# that's the most common default region.
LOCATIONS = ["us-central1", "global", "asia-south1"]

for loc in LOCATIONS:
    client_options = None
    if loc != "global":
        client_options = {"api_endpoint": f"{loc}-dialogflow.googleapis.com:443"}

    # Try detect_intent (Dialogflow Client role can do this)
    client = dialogflow.SessionsClient(client_options=client_options)
    # We don't know the agent ID, so we construct a placeholder and see what error we get
    # 404 = agent/session not found (we HAVE permission, just wrong ID)
    # 403 = no permission at all
    for fake_agent_id in ["aarogya-saathi", "default"]:
        session = f"projects/{PROJECT_ID}/locations/{loc}/agents/{fake_agent_id}/sessions/test123"
        req = dialogflow.DetectIntentRequest(
            session=session,
            query_input=dialogflow.QueryInput(
                text=dialogflow.TextInput(text="hello"),
                language_code="en"
            )
        )
        try:
            client.detect_intent(request=req)
            print(f"[OK]  {loc}/{fake_agent_id}: detect_intent SUCCESS (agent found!)")
        except NotFound as e:
            print(f"[404] {loc}/{fake_agent_id}: Not found (SA has permission, wrong agent ID)")
        except PermissionDenied as e:
            print(f"[403] {loc}/{fake_agent_id}: Permission denied")
        except Exception as e:
            msg = str(e)[:100]
            print(f"[ERR] {loc}/{fake_agent_id}: {msg}")

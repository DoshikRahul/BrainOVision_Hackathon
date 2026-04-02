import os
from google.cloud import dialogflowcx_v3beta1 as dialogflow
from google.oauth2 import service_account

# Set the environment variable for credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"e:\BrainOVision_Hackathon\aarogya-saathi-cbkb-e7b6a5333579.json"

def list_agents(project_id, location):
    client_options = None
    if location != "global":
        client_options = {"api_endpoint": f"{location}-dialogflow.googleapis.com:443"}
        
    client = dialogflow.AgentsClient(client_options=client_options)
    
    parent = f"projects/{project_id}/locations/{location}"
    
    print(f"Listing agents in {parent}...")
    try:
        agents = client.list_agents(request={"parent": parent})
        for agent in agents:
            print(f"Agent Name: {agent.display_name}")
            print(f"Agent ID: {agent.name}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Test global location first
    list_agents("aarogya-saathi-cbkb", "global")

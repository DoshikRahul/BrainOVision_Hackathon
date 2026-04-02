from google.cloud import dialogflowcx_v3beta1 as dialogflow
import uuid
import os

# Note: You'll need to set GOOGLE_APPLICATION_CREDENTIALS pointing to the service account
# and configure DIALOGFLOW_PROJECT_ID, DIALOGFLOW_LOCATION, DIALOGFLOW_AGENT_ID

PROJECT_ID = os.getenv("DIALOGFLOW_PROJECT_ID", "aarogya-saathi-cbkb")
LOCATION   = os.getenv("DIALOGFLOW_LOCATION", "global")
AGENT_ID   = os.getenv("DIALOGFLOW_AGENT_ID", "f6b5db02-7a99-45c7-9ff2-3d5a0739241c")

def detect_intent_texts(session_id: str, text: str, language_code: str = "en"):
    """Returns the result of detect intent with texts as inputs."""
    
    session_path = f"projects/{PROJECT_ID}/locations/{LOCATION}/agents/{AGENT_ID}/sessions/{session_id}"
    
    client_options = None
    if LOCATION != "global":
        api_endpoint = f"{LOCATION}-dialogflow.googleapis.com:443"
        client_options = {"api_endpoint": api_endpoint}
    
    session_client = dialogflow.SessionsClient(client_options=client_options)

    text_input = dialogflow.TextInput(text=text)
    query_input = dialogflow.QueryInput(text=text_input, language_code=language_code)
    request = dialogflow.DetectIntentRequest(
        session=session_path, query_input=query_input
    )

    try:
        response = session_client.detect_intent(request=request)
        response_messages = []
        for message in response.query_result.response_messages:
            if message.text:
                response_messages.append({"text": message.text.text[0]})
        return response_messages
    except Exception as e:
        print(f"Error communicating with Dialogflow CX: {e}")
        return [{"text": "Sorry, I am having trouble reaching the chatbot engine right now."}]

# Dialogflow CX Setup

This directory contains the training data for the **Aarogya Saathi** Dialogflow CX Agent.

## Manual Import Instructions

If you do not want to use the automated `setup_dialogflow.py` script (which requires Google Cloud service account keys), you can manually add the intents and entities via the Dialogflow CX Console.

### 1. Create your Agent
1. Go to the [Dialogflow CX Console](https://dialogflow.cloud.google.com/cx/).
2. Click **Create Agent** and fill in the details.

### 2. Add Entities
For entities like `@disease` and `@symptom`:
1. Navigate to **Manage > Entity Types**.
2. Click **Create**.
3. Name it exactly (e.g. `disease`).
4. You can manually copy the CSV rows from `entities/disease.csv` into the console, grouping synonyms together.

### 3. Add Intents
For intents like `Greeting`, `Disease Info`, and `Symptom Checker`:
1. Navigate to **Manage > Intents**.
2. Click **Create**.
3. Copy lines from `intents/greeting.txt` into the training phrases section.
4. Remember to manually highlight words like "dengue" and tag them with your `@disease` entity in the training phrases so the model learns to pick them up!

---
> **Note**: Complete Phase 2 by obtaining your Agent ID, Project ID, and Location, and placing them in your `.env` so `dialogflow_cx_client.py` can connect.

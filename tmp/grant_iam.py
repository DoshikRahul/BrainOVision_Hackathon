"""
grant_iam.py  ─  Grant Dialogflow API Admin role to the SA using IAM API.
The SA must itself have resourcemanager.projects.setIamPolicy permission,
which is granted if it has the Project IAM Admin role on the project.
"""
import os
from google.cloud import resourcemanager_v3
from google.iam.v1 import iam_policy_pb2, policy_pb2
from google.api_core.exceptions import PermissionDenied

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"e:\BrainOVision_Hackathon\aarogya-saathi-cbkb-e7b6a5333579.json"

PROJECT_ID  = "aarogya-saathi-cbkb"
SA_EMAIL    = "aarogya-saathi@aarogya-saathi-cbkb.iam.gserviceaccount.com"
ROLES_NEEDED = [
    "roles/dialogflow.admin",
]

client = resourcemanager_v3.ProjectsClient()
project_name = f"projects/{PROJECT_ID}"

print("Reading current IAM policy …")
try:
    policy = client.get_iam_policy(request={"resource": project_name})
except PermissionDenied as e:
    print(f"[403] Cannot read IAM policy — SA lacks resourcemanager.projects.getIamPolicy: {e}")
    raise SystemExit(1)

member = f"serviceAccount:{SA_EMAIL}"
added_any = False

for role in ROLES_NEEDED:
    # Check if binding already exists
    already = False
    for binding in policy.bindings:
        if binding.role == role and member in binding.members:
            print(f"[SKIP] {role} already granted to {member}")
            already = True
            break
    if not already:
        policy.bindings.append(policy_pb2.Binding(role=role, members=[member]))
        print(f"[ADD] {role} → {member}")
        added_any = True

if added_any:
    print("Writing updated IAM policy …")
    try:
        updated = client.set_iam_policy(
            request={"resource": project_name, "policy": policy}
        )
        print("[OK] IAM policy updated successfully.")
    except PermissionDenied as e:
        print(f"[403] Cannot write IAM policy — SA lacks resourcemanager.projects.setIamPolicy: {e}")
        raise SystemExit(1)
else:
    print("[OK] No changes needed.")

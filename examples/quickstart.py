import requests
import json

# Example: Test behavioral consistency measurement
consistency_data = {
    "agent_id": "test_agent",
    "prompt": "Analyze quarterly revenue trends",
    "responses": [
        "Revenue increased 15% this quarter due to strong product sales",
        "Quarterly revenue grew by 15% driven by product performance", 
        "15% revenue growth this quarter from improved product sales"
    ]
}

# Send request to CERT API
response = requests.post(
    "http://localhost:8000/measure/consistency",
    json=consistency_data
)

print("Consistency Analysis:")
print(json.dumps(response.json(), indent=2))
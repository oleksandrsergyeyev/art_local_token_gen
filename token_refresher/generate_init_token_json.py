import requests
import json
import time
import os

# Prompt user to paste the TEMP_TOKEN_1 (non-refreshable)
INIT_TOKEN = input("Paste your non-refreshable: ").strip()
CREATE_URL = "https://ara-artifactory.volvocars.biz/access/api/v1/tokens"

headers = {
    "Authorization": f"Bearer {INIT_TOKEN}",
    "Content-Type": "application/x-www-form-urlencoded"
}

data = {
    "scope": "applied-permissions/user",
    "refreshable": "true",
    "description": "Initial refreshable token",
    "expires_in": 14400  # 4 hours
}

print("Requesting refreshable token...")
response = requests.post(CREATE_URL, headers=headers, data=data)

if response.status_code == 200:
    token_response = response.json()
    expires_at = int(time.time() + token_response["expires_in"])

    tokens = {
        "access_token": token_response["access_token"],
        "refresh_token": token_response["refresh_token"],
        "expires_at": expires_at
    }

    os.makedirs("token_refresher", exist_ok=True)
    with open("token_refresher/init_tokens.json", "w") as f:
        json.dump(tokens, f, indent=4)

    print("Refreshable token saved to token_refresher/init_tokens.json")
    print("Expires at:", expires_at)
else:
    print("Failed to generate refreshable token:", response.status_code)
    print(response.text)

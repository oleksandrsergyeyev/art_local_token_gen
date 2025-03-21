import requests
import json
import time
import os
from dotenv import load_dotenv, set_key

# Load existing .env
load_dotenv(dotenv_path=".env")

# Constants
TOKEN_URL = "https://ara-artifactory.volvocars.biz/access/api/v1/tokens"
TOKENS_FILE = os.path.join(os.path.dirname(__file__), "init_tokens.json")
ENV_FILE = os.path.join(os.path.dirname(__file__), "..", ".env")
REFRESH_MARGIN = 300  # seconds before expiry to refresh (5 minutes)

# Load saved tokens from file
def load_tokens():
    if not os.path.exists(TOKENS_FILE):
        return None
    with open(TOKENS_FILE, "r") as f:
        return json.load(f)

# Save tokens to file and .env
def save_tokens(token_data):
    # Save JSON token file
    with open(TOKENS_FILE, "w") as f:
        json.dump(token_data, f, indent=4)

    # Ensure .env file exists
    if not os.path.exists(ENV_FILE):
        with open(ENV_FILE, "w") as f:
            f.write("")

    # Save both tokens
    set_key(ENV_FILE, "ARTIFACTORY_TOKEN", token_data["access_token"])
    set_key(ENV_FILE, "ARTIFACTORY_REFRESH_TOKEN", token_data["refresh_token"])
    print("Access and refresh tokens saved to tokens.json and .env")


# Refresh token using Artifactory API
def refresh_token(access_token, refresh_token):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }

    response = requests.post(TOKEN_URL, headers=headers, data=data)
    if response.status_code == 201:
        token_data = response.json()
        return {
            "access_token": token_data["access_token"],
            "refresh_token": token_data["refresh_token"],
            "expires_at": time.time() + token_data["expires_in"]
        }
    else:
        print("Failed to refresh token:", response.status_code, response.text)
        return None

# Main logic
def main():
    tokens = load_tokens()
    if not tokens:
        print("No tokens found. Run the initial setup to generate a refreshable token.")
        return

    time_remaining = tokens["expires_at"] - time.time()
    print(f"Time until token expiry: {int(time_remaining)} seconds")

    if time_remaining < REFRESH_MARGIN:
        print("Token is about to expire. Refreshing...")
        new_tokens = refresh_token(tokens["access_token"], tokens["refresh_token"])
        if new_tokens:
            save_tokens(new_tokens)
    else:
        print("Token still valid. No need to refresh.")
        # 👍 Write .env anyway in case it's missing
        save_tokens(tokens)


if __name__ == "__main__":
    main()

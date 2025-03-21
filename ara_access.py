import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

class ArtifactoryClient:
    BASE_URL = "https://ara-artifactory.volvocars.biz/artifactory"

    def __init__(self, repo: str):
        self.repo = repo
        self.token = os.getenv("ARTIFACTORY_TOKEN")
        if not self.token:
            raise ValueError("ARTIFACTORY_TOKEN not found in environment. Run token_refresher.py first.")

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json"
        }

    def get_artifact_metadata(self):
        url = f"{self.BASE_URL}/api/storage/{self.repo}"
        response = requests.get(url, headers=self._headers())
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get metadata: {response.status_code} {response.text}")

    def list_artifacts(self):
        url = f"{self.BASE_URL}/api/storage/{self.repo}?list"
        response = requests.get(url, headers=self._headers())
        if response.status_code == 200:
            return response.json().get("files", [])
        else:
            raise Exception(f"Failed to list artifacts: {response.status_code} {response.text}")


if __name__=="__main__":
    client = ArtifactoryClient("ARTBC-SUM-LTS")
    print(json.dumps(client.get_artifact_metadata(), indent=2))

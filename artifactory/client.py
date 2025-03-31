import os

import requests
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

    def find_artifacts_by_properties(self, properties: dict, path_contains: str = None):
        """
        Find artifacts in the repository that match all given properties.
        :param properties: dict of property_key: property_value
        :return: list of matching artifact results
        """
        url = f"{self.BASE_URL}/api/search/aql"

        # Build the AQL object with repo and type
        base_conditions = [
            f'"repo": "{self.repo}"',
            '"type": "file"'
        ]

        if path_contains:
            base_conditions.append(f'"path": {{"$match": "*{path_contains}*"}}')

        # Append @property entries
        base_conditions += [f'"@{k}": "{v}"' for k, v in properties.items()]
        aql_query = f"items.find({{{', '.join(base_conditions)}}})"

        response = requests.post(url, data=aql_query, headers={
            **self._headers(),
            "Content-Type": "text/plain"
        })

        if response.status_code == 200:
            results = response.json().get("results", [])
            filtered = [m for m in results if m["path"].endswith("SWLM/xcp_disabled/vbf")]
            return filtered
        else:
            raise Exception(f"Failed to search by properties: {response.status_code} {response.text}")

    def download_artifact(self, path: str, name: str, dest_folder: str = "."):
        """
        Downloads an artifact from the repository.

        :param path: Artifact's folder path in the repo (e.g. 'SWLM/xcp_disabled/vbf')
        :param name: Artifact filename (e.g. 'abc.vbf')
        :param dest_folder: Local directory to save the file
        """
        url = f"{self.BASE_URL}/{self.repo}/{path}/{name}"
        local_path = os.path.join(dest_folder, name)

        response = requests.get(url, headers=self._headers(), stream=True)
        if response.status_code == 200:
            with open(local_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"✅ Downloaded: {local_path}")
        else:
            raise Exception(f"❌ Failed to download: {response.status_code} {response.text}")

import argparse
from artifactory.client import ArtifactoryClient


def main():
    parser = argparse.ArgumentParser(description="Search and download an artifact from Artifactory.")
    parser.add_argument("--repo", required=True, help="Artifactory repository name")
    parser.add_argument("--version", required=True, help="baseline.sw.version property")
    parser.add_argument("--type", required=True, help="baseline.sw.type property")
    parser.add_argument("--path", required=False, help="Path filter (e.g., SWLM/xcp_disabled/vbf)")
    parser.add_argument("--out", default=".", help="Destination folder to save the downloaded file")

    args = parser.parse_args()

    props = {
        "baseline.sw.version": args.version,
        "baseline.sw.type": args.type
    }

    client = ArtifactoryClient(args.repo)
    results = client.find_artifacts_by_properties(props, path_contains=args.path)

    if results:
        artifact = results[0]
        client.download_artifact(artifact["path"], artifact["name"], args.out)
    else:
        print("No matching artifacts found.")

if __name__ == "__main__":
    main()

import argparse
import os
import re
import subprocess
from datetime import datetime
from pathlib import Path

from pyvulnerabilitylookup import PyVulnerabilityLookup

from nucleivuln import config

# Constants
REPO_PATH = config.nuclei_git_repository
CVE_DIR = "cves"  # Directory to check for CVE YAML files
CVE_PATTERN_YAML = re.compile(
    r"CVE-\d{4}-\d{4,7}\.yaml"
)  # Pattern for YAML file with CVE identifiants
CVE_PATTERN = re.compile(r"CVE-\d{4}-\d{4,7}")  # Pattern for CVE identifiants


def git_pull():
    """Pull the latest changes from the Git repository."""
    try:
        subprocess.run(["git", "pull"], cwd=REPO_PATH, check=True, text=True)
        print("Git repository updated successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to update Git repository: {e}")
        return False
    return True


def get_new_commits():
    """Get new commits since the last pull."""
    try:
        result = subprocess.run(
            ["git", "log", "--since='4 day ago'", "--name-status"],
            cwd=REPO_PATH,
            check=True,
            text=True,
            capture_output=True,
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Failed to get new commits: {e}")
        return None


def check_for_new_yaml_files(commit_logs):
    """Check for new YAML files in the CVE directory."""
    new_files = []
    for line in commit_logs.splitlines():
        if line.startswith("A\t"):  # Files added in the commit
            file_path = line.split("\t")[1]
            if CVE_DIR in file_path and CVE_PATTERN_YAML.match(Path(file_path).name):
                new_files.append(file_path)
    return new_files


def find_all_cve_yaml_files_with_dates():
    """Search the repository for all CVE YAML files and their creation dates."""
    cve_files_with_dates = []
    try:
        for root, _, files in os.walk(REPO_PATH):
            for file in files:
                if file.endswith(".yaml") and CVE_PATTERN_YAML.match(file):
                    file_path = os.path.relpath(os.path.join(root, file), REPO_PATH)
                    if CVE_DIR in file_path:
                        vuln_id = file.split("/")[-1].replace(".yaml", "")
                        creation_date = get_file_creation_date(file_path)
                        cve_files_with_dates.append((file_path, vuln_id, creation_date))
    except Exception as e:
        print(f"Error searching for CVE YAML files: {e}")
    return cve_files_with_dates


def get_file_creation_date(file_path):
    """Get the creation date of a file from Git as a UTC-aware datetime object."""
    try:
        result = subprocess.run(
            ["git", "log", "--diff-filter=A", "--format=%aD", "--", file_path],
            cwd=REPO_PATH,
            check=True,
            text=True,
            capture_output=True,
        )
        creation_date_raw = result.stdout.strip()
        if creation_date_raw:
            # Parse the RFC2822 date and convert it to a UTC-aware datetime object
            creation_date = datetime.strptime(
                creation_date_raw, "%a, %d %b %Y %H:%M:%S %z"
            )
            return creation_date
        return None
    except subprocess.CalledProcessError as e:
        print(f"Failed to get creation date for {file_path}: {e}")
        return None


def push_sighting_to_vulnerability_lookup(
    nuclei_template, vulnerability, creation_date
):
    """Create a sighting from an incoming status and push it to the Vulnerability Lookup instance."""
    print("Pushing sighting to Vulnerability Lookup...")
    vuln_lookup = PyVulnerabilityLookup(
        config.vulnerability_lookup_base_url, token=config.vulnerability_auth_token
    )

    # Create the sighting
    sighting = {
        "type": config.sighthing_type,
        "source": f"https://github.com/projectdiscovery/nuclei-templates/tree/main/{nuclei_template}",
        "vulnerability": vulnerability,
        "creation_timestamp": creation_date,
    }

    # Post the JSON to Vulnerability Lookup
    try:
        r = vuln_lookup.create_sighting(sighting=sighting)
        if "message" in r:
            print(r["message"])
    except Exception as e:
        print(
            f"Error when sending POST request to the Vulnerability Lookup server:\n{e}"
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="NucleiVuln",
        description="Find new Nuclei templates related to a vulnerability in a Git repository.",
    )
    parser.add_argument(
        "--init",
        action="store_true",
        help="Find Nuclei templates even if no new commits were detected.",
    )

    arguments = parser.parse_args()

    if not git_pull():
        return

    commit_logs = get_new_commits()
    if commit_logs and not arguments.init:
        new_cve_files = check_for_new_yaml_files(commit_logs)
        if new_cve_files:
            print("New CVE YAML files detected:")
            for file in new_cve_files:
                vuln_id = file.split("/")[-1].replace(".yaml", "")
                creation_date = get_file_creation_date(file)
                print(f"NEW - {file} (Created on: {creation_date})")
                push_sighting_to_vulnerability_lookup(file, vuln_id, creation_date)
        else:
            print("No new CVE YAML files found.")
    elif arguments.init:
        print("No new commits detected. Searching the repository for CVE YAML files...")
        cve_files_with_dates = find_all_cve_yaml_files_with_dates()
        if cve_files_with_dates:
            print("CVE YAML files found in the repository:")
            for file, vuln_id, creation_date in cve_files_with_dates:
                print(f"NEW - {file} (Created on: {creation_date})")
                push_sighting_to_vulnerability_lookup(file, vuln_id, creation_date)
        else:
            print("No CVE YAML files found in the repository.")


if __name__ == "__main__":
    # Point of entry in execution mode
    main()

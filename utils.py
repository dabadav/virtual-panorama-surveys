# Load libraries
import os
import json # Load JSON filetype
import yaml # Load Yaml filetype
import fnmatch # Pattern matching
import re # Regular expressions

def load_yaml(file_path):
    with open(file_path) as f:
        try:
            mapping = yaml.safe_load(f)
            return mapping
        except yaml.YAMLError as exc:
            print(exc)
            return None

def load_json(file_path):
    """Safe load json file"""
    with open(file_path, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in file: {file_path}")
            print(e)
            return None

def match_files(data_dir, pattern):
    """Given directory find matching files"""
    files = [
        os.path.join(data_dir, filename)
        for filename in os.listdir(data_dir)
        if fnmatch.fnmatch(filename, pattern)
    ]
    return files

def load_json_files(data_dir, pattern):
    """Loads JSON files from a directory matching a filename pattern.

    Args:
        data_dir: Path to the directory containing JSON files.
        pattern: Filename pattern to match (e.g., 'data_*.json').

    Returns:
        A list of dictionaries, where each dictionary represents a matched JSON file.
    """
    
    # List all files in folder
    json_files = match_files(data_dir, pattern)

    # List of python objects
    data = [load_json(file_path) for file_path in json_files if file_path]

    return data

def extract_id(filename):
    """Extracts the numeric ID from the filename."""
    match = re.search(r'_(\d+)\.json$', filename)
    return match.group(1) if match else None

def extract_id_files(data_dir, pattern="Log_Survey_BB_*.json"):
    """
    Extracts numeric IDs from filenames matching a given pattern.

    Args:
        data_dir (str): Path to the directory containing files.
        pattern (str): Filename pattern to match (default: 'Log_Survey_BB_*.json').

    Returns:
        list: A list of extracted numeric IDs as strings.
    """

    # List all matching files
    files = match_files(data_dir, pattern)

    # Extract IDs and filter out None values
    ids = [extract_id(file) for file in files]

    return ids



#################
# Miscellaneous #
#################

import os
import webbrowser
from datetime import datetime
from urllib.request import pathname2url

def clean_duplicated_json(data_dir , pattern):
    files_info = []

    for file in match_files(data_dir, pattern):
        json_data = load_json(file)
        if len(json_data) > 40:
            file_id = extract_id(file)
            creation_time = datetime.fromtimestamp(os.path.getctime(file)).strftime("%Y-%m-%d %H:%M:%S")
            files_info.append((file_id, creation_time))
            
            # Open in browser
            file_url = 'file://' + pathname2url(os.path.abspath(file))
            webbrowser.open(file_url)

            # Delete the file
            os.remove(file)

    print("Finished processing and deleting matching files.")
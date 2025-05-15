# Load libraries
import fnmatch  # Pattern matching
import json  # Load JSON filetype
import os
import re  # Regular expressions

import yaml  # Load Yaml filetype


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
    with open(file_path, "r") as f:
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
    match = re.search(r"_(\d+)\.json$", filename)
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
from pathlib import Path
from urllib.request import pathname2url

import pandas as pd
from IPython.display import HTML, display


def clean_duplicated_json(data_dir, pattern):
    files_info = []

    for file in match_files(data_dir, pattern):
        json_data = load_json(file)
        if len(json_data) > 40:
            file_id = extract_id(file)
            creation_time = datetime.fromtimestamp(os.path.getctime(file)).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            files_info.append((file_id, creation_time))

            # Open in browser
            file_url = "file://" + pathname2url(os.path.abspath(file))
            webbrowser.open(file_url)

            # Delete the file
            os.remove(file)

    print("Finished processing and deleting matching files.")


import os
import re

import pandas as pd


def remove_json_files_with_test_value_from_index(
    df: pd.DataFrame, directory: str, exact_match: bool = False
):
    """
    Removes JSON files from a directory whose filenames contain IDs present
    in the DataFrame index, where the corresponding row contains 'Test'
    in any column.

    Parameters:
        df (pd.DataFrame): The DataFrame (IDs must be in the index).
        directory (str): Path to the directory containing JSON files.
        exact_match (bool): Whether to match exact value "Test" or allow partial.
    """
    # Step 1: Identify rows where any column contains "Test"
    if exact_match:
        mask = df.isin(["Test"])
    else:
        mask = df.astype(str).apply(
            lambda row: row.str.contains("Test", case=False, na=False), axis=1
        )

    matching_ids = df.index[mask.any(axis=1)].astype(str).tolist()

    # Step 2: Delete matching files
    for filename in os.listdir(directory):
        if not filename.endswith(".json"):
            continue
        for file_id in matching_ids:
            if re.search(rf"{re.escape(file_id)}", filename):
                file_path = os.path.join(directory, filename)
                try:
                    os.remove(file_path)
                    print(f"Removed: {file_path}")
                except Exception as e:
                    print(f"Failed to remove {file_path}: {e}")
                break  # Avoid multiple deletions for same file


#################
#    Reports    #
#################


def generate_columnwise_unique_report(
    df: pd.DataFrame, output_path: str = "unique_values_columnwise.html"
) -> str:
    # Collect unique values per column
    unique_values = {col: df[col].dropna().unique().tolist() for col in df.columns}

    # Start HTML
    html = """
    <html>
    <head>
        <style>
            body { font-family: Arial; padding: 20px; }
            table { border-collapse: collapse; }
            td, th { border: 1px solid #ddd; padding: 8px; vertical-align: top; text-align: left; }
            th { background-color: #f2f2f2; }
            button { margin: 10px 0; padding: 6px 10px; background-color: #4CAF50; color: white; border: none; cursor: pointer; }
            button:hover { background-color: #45a049; }
            pre { background: #f8f8f8; padding: 10px; border: 1px solid #ccc; }
        </style>
        <script>
            function copyText(id) {
                var text = document.getElementById(id).innerText;
                navigator.clipboard.writeText(text).then(function() {
                    alert("Copied to clipboard!");
                }, function(err) {
                    alert("Failed to copy text: ", err);
                });
            }
        </script>
    </head>
    <body>
        <h1>Unique Values Per Column</h1>
        <table>
            <tr><th>Column</th><th>Unique Values</th><th>Copy</th></tr>
    """

    for i, (col, values) in enumerate(unique_values.items()):
        text_block = "\n".join(str(v) for v in values)
        pre_id = f"pre_{i}"
        html += f"""
            <tr>
                <td><b>{col}</b></td>
                <td><pre id="{pre_id}">{text_block}</pre></td>
                <td><button onclick="copyText('{pre_id}')">Copy</button></td>
            </tr>
        """

    html += """
        </table>
    </body>
    </html>
    """

    # Write to file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    return output_path


def render_mapping_dict_to_html(
    mapping: dict,
    title: str = "Mapping Overview",
    output_path: str = "mapping_report.html",
):
    html = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: Arial, sans-serif; padding: 20px; }}
            table {{ border-collapse: collapse; }}
            th, td {{ border: 1px solid #ccc; padding: 8px; text-align: left; vertical-align: top; }}
            th {{ background-color: #f2f2f2; }}
            code {{ white-space: pre-wrap; word-break: break-word; }}
        </style>
    </head>
    <body>
        <h1>{title}</h1>
        <table>
            <tr><th>Original Value</th><th>Mapped Value</th></tr>
    """

    for key, val in mapping.items():
        if isinstance(val, list):
            val_display = "<ul>" + "".join(f"<li>{v}</li>" for v in val) + "</ul>"
        else:
            val_display = f"<code>{val}</code>"
        html += f"<tr><td><code>{key}</code></td><td>{val_display}</td></tr>"

    html += """
        </table>
    </body>
    </html>
    """

    Path(output_path).write_text(html, encoding="utf-8")
    print(f"{output_path}")

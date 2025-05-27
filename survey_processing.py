# %%
import sys
from pathlib import Path
import pandas as pd

sys.path.append("..")
from utils import extract_id_files, load_json_files, load_yaml

# %%
########### Load and Process
data_dir = Path("../data/LogsBergenBelsen")
pattern = "Log_Survey*.json"  # Survey files pattern
output_directory = Path("data/")
output_filename = "Log_Survey.csv"

# Load JSONs into Pandas df
survey = load_json_files(data_dir, pattern)
visitor_ids = extract_id_files(data_dir, pattern)
survey_tables = [pd.json_normalize(s, sep="_") for s in survey]
df_survey = pd.DataFrame(
    {f"df_{i}": df["answer"] for i, df in enumerate(survey_tables)}
)

df_survey.columns = visitor_ids
questions = pd.read_csv("english_questions.csv")['question']
df_survey.index = questions  # English questions
# Save
df_survey = df_survey.T

# Rename columns
mapping_questions = load_yaml("mapping_questions.yaml")["mapping_questions"]
df_survey.columns = df_survey.columns.map(mapping_questions)
df_survey.to_csv(output_directory / output_filename)

# %%
########### Report unique elements per column
from utils import (
    generate_columnwise_unique_report,
    load_yaml,
    render_mapping_dict_to_html,
)

mapping_response = load_yaml("mapping_response.yaml")["mapping_response"]
# generate_columnwise_unique_report(df_survey, output_path="reports/unique_values.html")
# render_mapping_dict_to_html(mapping_response, output_path="reports/mapping_report.html")

# %%
########### Normalize and Translate
mapping_response = load_yaml("mapping_response.yaml")["mapping_response"]
df_survey_translated = df_survey.replace(mapping_response)
df_survey_translated.to_csv(output_directory / "Log_Survey_Translated.csv")

# generate_columnwise_unique_report(
    # df_survey_translated, output_path="reports/unique_values_translated.html"
# )

# %%
########## Remove Non answered - No survey
df_unique = df_survey_translated[~df_survey_translated.duplicated(keep=False)]
df_unique.to_csv(output_directory / "Log_Survey_Processed.csv", index=False)

# %%
########## Convert strings to list
from utils import str_to_list

df_unique = pd.read_csv("data/Log_Survey_Processed.csv", index_col=0)

str_to_list_columns = ['visit_purpose', 'personal_connection_details', 'known_persecuted_groups_open', 'technologies_used']
for col in str_to_list_columns:
    df_unique[col] = df_unique[col].apply(str_to_list)

df_unique.to_parquet("data/Log_Survey.parquet", index=False)
# %%

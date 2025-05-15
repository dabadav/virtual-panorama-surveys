# %%
from pathlib import Path
import pandas as pd
import sys
sys.path.append('..')
from utils import load_json_files, extract_id_files, match_files, load_json, load_yaml

# %%
data_dir = Path("../data/Bergen-Belsen-Full-Data/LogsBergenBelsen")
pattern = 'Log_Survey*.json'  # Survey files pattern
output_directory = Path('data/')
output_filename = 'Log_Survey.csv'

# Load JSONs into Pandas df
survey = load_json_files(data_dir, pattern)
visitor_ids = extract_id_files(data_dir, pattern)
survey_tables = [pd.json_normalize(s, sep='_') for s in survey]
df_survey = pd.DataFrame({f"df_{i}": df["answer"] for i, df in enumerate(survey_tables)})
df_survey.columns = visitor_ids
df_survey.index = survey_tables[100]['question'] # English questions

# Save 
df_survey.T.to_csv(output_directory / output_filename)

# %%
df_survey = df_survey.T

# Mapping dicts
mapping_questions = load_yaml('mapping_questions.yaml')['mapping_questions']
mapping_country = load_yaml('mapping_country.yaml')['mapping_country']

# Normalization
df_survey.columns = df_survey.columns.map(mapping_questions)

df_survey['nationality'] = df_survey['nationality'].map(mapping_country)
df_survey = df_survey[df_survey['nationality'] != 'Testing']
# Translation
# %%

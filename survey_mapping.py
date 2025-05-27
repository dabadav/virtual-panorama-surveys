# %%
import pandas as pd

# df_survey = pd.read_parquet("data/Log_Survey.parquet")
df_survey = pd.read_csv("data/Log_Survey_Processed.csv", index_col=0)

# %%
from utils import visitor_profile

# Map visitors to static profiles using mapping
## Student - visit_type
## Personal Involvement - personal_connection
## Researcher - visit_purpose,educational_level
## Tourist - no personal_connection
df_profile = visitor_profile(df_survey)
df_profile.to_csv("data/Log_Survey_Persona.csv")

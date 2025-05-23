# %%
import pandas as pd
# df_survey = pd.read_csv("data/Log_Survey_Processed.csv", index_col=0)
df_survey = pd.read_parquet("data/Log_Survey_List.parquet")

# %%
# example = 'Jews__Homosexuals__Political opponents__Sinti and Roma'
def str_to_list(string):
    if pd.isna(string):
        return []
    return string.split(sep='__')

str_to_list_columns = ['visit_purpose', 'personal_connection_details', 'known_persecuted_groups_open', 'technologies_used']

for col in str_to_list_columns:
    df_survey[col] = df_survey[col].apply(str_to_list)


df_survey.to_parquet("data/Log_Survey_List.parquet", index=False)
# df_survey = pd.read_csv("data/Log_Survey_List.csv", index_col=0)
# string to list functi

# %% 
selected_columns = [
    'nationality', 'gender_identity', 'age', 
    'education_level',
    'visit_type', 'visit_purpose', 
    'religious',
    'visited_memorial_before', 'personal_connection_nazi_history',
    'personal_connection_details',
    'knowledge_ww2',
    'known_persecuted_groups_open',
    'technologies_used', 'videogame_frequency'
]
df_survey[selected_columns].to_csv("data/Log_Profile.csv")
# %%
from ydata_profiling import ProfileReport

profile = ProfileReport(
    df_survey, title="VisualPanorama - Survey Results", explorative=True, minimal=False
)
profile.to_file("panel6_survey_data_parquet.html")
# %%

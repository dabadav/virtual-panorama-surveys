# %%
import pandas as pd
# df_survey = pd.read_csv("data/Log_Survey_Processed.csv", index_col=0)
df_survey = pd.read_parquet("data/Log_Survey.parquet")

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

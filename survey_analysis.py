# %%
import pandas as pd

# %%
df_survey = pd.read_csv("data/Log_Survey_Translated.csv", index_col=0)
# %%

from ydata_profiling import ProfileReport

profile = ProfileReport(
    df_survey, title="VisualPanorama - Survey Results", explorative=True, minimal=False
)
profile.to_file("interactive_survey_report_full.html")

# %%

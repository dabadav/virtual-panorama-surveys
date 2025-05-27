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
df_profile.to_csv("data/Log_Survey_Persona.csv", index=False)

# %%

# df['profile']

import seaborn as sns
import matplotlib.pyplot as plt
df_profile.to_csv("data/Log_Survey_Persona.csv", index=False)

# Create pie chart
data = 
labels = ['A', 'B', 'C', 'D']
sns.set_style("darkgrid")
plt.pie(data, labels=labels)

# Add title
plt.title("Distribution of Data")

# Show plot
plt.show()
# df[df['profile'] == 'Tourist'][['age', 'education_level', 'visit_type', 'visit_purpose', 'personal_connection_nazi_history', 'profile']]
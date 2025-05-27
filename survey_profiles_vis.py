# %%
from pathlib import Path

import dash
import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio
from dash import dcc, html
from plotly.colors import qualitative
from utils import str_to_list

# Sample DataFrame (replace with your real data)
data = pd.read_csv("data/Log_Survey_Persona.csv", index_col=0)
columns = [
    "nationality",
    "gender_identity",
    "age",
    "education_level",
    "visit_type",
    "visit_purpose",
    "religious",
    "visited_memorial_before",
    "personal_connection_nazi_history",
    # "personal_connection_details",
    "known_persecuted_groups_open",
    "knowledge_ww2",
    "technologies_used",
    "profile",
]
df = data[columns]

# Extract question columns and profiles
question_columns = [col for col in df.columns if col != "profile"]
profiles = df["profile"].unique().tolist()

str_to_list_columns = [
    "visit_purpose",
    # "personal_connection_details",
    "known_persecuted_groups_open",
    "technologies_used",
]

for col in str_to_list_columns:
    df[col] = df[col].apply(str_to_list)


# %%

# Ensure the 'profile' column exists
assert "profile" in df.columns, "Missing 'profile' column."

# Identify questions (exclude 'profile')
question_columns = [col for col in df.columns if col != "profile"]
profiles = df["profile"].unique().tolist()

# Assign consistent colors to profiles
color_map = {profile: color for profile, color in zip(profiles, qualitative.Plotly)}


def export_all_plots_combined_html(
    output_file="reports/profile_distribution_report.html",
):
    html_blocks = []

    # --- Summary block ---
    total_visitors = len(df)
    profile_counts = df["profile"].value_counts().to_dict()

    summary_html = f"""
    <div style="margin-bottom: 30px;">
        <h2>Survey Overview</h2>
        <p><strong>Total Visitors:</strong> {total_visitors}</p>
        <ul>
            {''.join(f'<li><strong>{profile}</strong>: {count} visitors</li>' for profile, count in profile_counts.items())}
        </ul>
    </div>
    """

    # --- Generate charts ---
    for question in question_columns:
        graph_component = create_percentage_distribution_plot(question)
        fig = graph_component.figure
        html_fragment = pio.to_html(fig, include_plotlyjs=False, full_html=False)
        html_blocks.append(f"<div style='margin-bottom:40px;'>{html_fragment}</div>")

    # --- Combine all into full HTML document ---
    full_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Demographic Response Distributions</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
            }}
            h1 {{
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <h1>Per-Profile Response Distributions (All Questions)</h1>
        {summary_html}
        {"".join(html_blocks)}
    </body>
    </html>
    """

    # Write to file
    Path(output_file).write_text(full_html, encoding="utf-8")
    print(f"Combined interactive HTML report saved to: {output_file}")


# Function to create one chart per question using % distribution within profile
def create_percentage_distribution_plot(question):
    # Step 1: Prepare a working copy of the relevant data
    col_data = df[["profile", question]].copy()

    # Step 2: Handle list-type values: explode them if needed
    # If any value in the column is a list, explode them
    if col_data[question].apply(lambda x: isinstance(x, list)).any():
        col_data = col_data.explode(question)

    # Step 3: Drop missing values (optional, but safe)
    col_data = col_data.dropna(subset=[question])

    # Step 4: Count responses per profile and option
    counts = col_data.groupby(["profile", question]).size().reset_index(name="count")

    # Step 5: Normalize within profile
    total_per_profile = counts.groupby("profile")["count"].transform("sum")
    counts["percentage"] = counts["count"] / total_per_profile * 100

    # Step 6: All unique options (ensure consistent x-axis)
    all_options = sorted(col_data[question].dropna().unique().tolist())

    # Step 7: Create traces per profile
    bars = []
    for profile in profiles:
        profile_counts = counts[counts["profile"] == profile].set_index(question)
        values = [
            profile_counts.loc[opt]["percentage"] if opt in profile_counts.index else 0
            for opt in all_options
        ]
        bars.append(
            go.Bar(
                x=all_options,
                y=values,
                name=profile,
                marker_color=color_map[profile],
                showlegend=(question == question_columns[0]),
            )
        )

    return dcc.Graph(
        figure=go.Figure(
            data=bars,
            layout=go.Layout(
                title=f"Response Distribution to '{question}' (by Profile)",
                xaxis_title="Answer Option",
                yaxis_title="Percentage within Profile",
                barmode="group",
                height=450,
            ),
        )
    )


# Dash app layout
app = dash.Dash(__name__)
app.title = "Profile-Adjusted Survey Visualizer"

app.layout = html.Div(
    [
        html.H1("Per-Profile Response Distributions", style={"textAlign": "center"}),
        html.Div([create_percentage_distribution_plot(q) for q in question_columns]),
    ]
)


if __name__ == "__main__":
    # Export all plots to a single HTML file
    export_all_plots_combined_html("reports/profile_distribution_report.html")
    # app.run(debug=True)

# %%

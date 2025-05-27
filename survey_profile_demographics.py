# %%
import ast
import os
import textwrap

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from utils import str_to_list

df_survey = pd.read_csv("data/Log_Survey_Persona.csv", index_col=0)

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
    "personal_connection_details",
    # "known_persecuted_groups_open",
    "knowledge_ww2",
    "technologies_used",
    "profile",
]

df_survey_persona = df_survey[columns]
print(df_survey_persona["profile"].unique())

str_to_list_columns = [
    "visit_purpose",
    "personal_connection_details",
    # "known_persecuted_groups_open",
    "technologies_used",
]
for col in str_to_list_columns:
    df_survey_persona[col] = df_survey_persona[col].apply(str_to_list)


def safely_parse_list_string(val):
    if isinstance(val, str) and val.startswith("[") and val.endswith("]"):
        try:
            return ast.literal_eval(val)
        except:
            return [val]
    return [val]  # wrap single values


def preprocess_list_column(df, column):
    """
    Converts stringified lists to actual lists and explodes them into multiple rows.
    """
    df = df.copy()
    df[column] = df[column].apply(safely_parse_list_string)
    return df.explode(column)


def safely_parse_list_string(val):
    if isinstance(val, str) and val.startswith("[") and val.endswith("]"):
        try:
            return ast.literal_eval(val)
        except:
            return []
    elif isinstance(val, list):
        return val
    elif pd.isna(val):
        return []
    else:
        return [val]


# %%
def plot_clean_demographics(
    df,
    persona_column,
    persona_value,
    color="#3366FF",
    bar_height=0.5,
    width=10,
    label_limit=60,
):
    """
    Clean bar chart of persona demographics with correct parsing of list-like strings.
    """
    subset = df[df[persona_column] == persona_value].copy()
    demographic_columns = [col for col in df.columns if col != persona_column]

    for col in demographic_columns:
        # Flatten individual list items
        subset[col] = subset[col].apply(safely_parse_list_string)
        exploded = subset.explode(col)
        exploded = exploded[~exploded[col].isin(["", [], None, np.nan])]

        values = exploded[col].dropna()
        if (
            values.dtype == "object"
            or values.dtype.name == "category"
            or values.nunique() < 50
        ):
            value_counts = values.value_counts(normalize=True).sort_values() * 100
            categories = value_counts.index.tolist()
            percentages = value_counts.values
            n = len(categories)
            height = max(2, n * (bar_height + 0.4))
            y_pos = np.arange(n)

            def truncate(label):
                return (
                    (label[:label_limit] + "…") if len(label) > label_limit else label
                )

            labels = [truncate(c) for c in categories]

            fig, ax = plt.subplots(figsize=(width, height))
            ax.barh(y_pos, percentages, color=color, height=bar_height)

            for i, pct in enumerate(percentages):
                label_x = pct - 1 if pct > 10 else pct + 1
                align = "right" if pct > 10 else "left"
                ax.text(
                    label_x,
                    y_pos[i],
                    f"{int(pct)}",
                    va="center",
                    ha=align,
                    color="white" if pct > 10 else color,
                    fontweight="bold",
                )

            for i, label in enumerate(labels):
                ax.text(-1, y_pos[i], label, va="center", ha="right", fontsize=10)

            ax.set_yticks([])
            ax.set_xlim(0, 100)
            ax.set_xlabel("")
            ax.set_title(
                f"{col.replace('_', ' ').capitalize()} Distribution for {persona_value}"
            )
            ax.invert_yaxis()
            ax.grid(axis="x", linestyle="--", alpha=0.3)
            plt.box(False)
            plt.tight_layout()
            plt.show()


# plot_clean_demographics(df_survey_persona, "profile", "Tourist", color="#3366FF")


# %%


def plot_demographics(
    df,
    persona_column,
    persona_value,
    color="#3366FF",
    bar_height=0.4,
    width=12,
    label_limit=40,
    max_categories=20,
    padding_per_subplot=1.2,
    save_path=None,
):
    """
    Plot demographics in subplots, each with proportional height based on number of categories.
    Bar thickness is consistent, plot height is adaptive.
    """
    subset = df[df[persona_column] == persona_value].copy()
    demographic_columns = [col for col in df.columns if col != persona_column]

    processed_data = []
    bar_counts = []

    for col in demographic_columns:
        subset[col] = subset[col].apply(safely_parse_list_string)
        exploded = subset.explode(col)
        exploded = exploded[~exploded[col].isin(["", [], None, np.nan])]
        values = exploded[col].dropna()

        if values.empty or values.nunique() > 50:
            continue

        value_counts = (
            values.value_counts(normalize=True).sort_values(ascending=True)[
                :max_categories
            ]
            * 100
        )
        processed_data.append((col.replace("_", " ").capitalize(), value_counts))
        bar_counts.append(len(value_counts))

    if not processed_data:
        print("No valid demographics to display.")
        return

    # Convert bar counts to height ratios
    height_ratios = [
        max(1, int(c * bar_height + padding_per_subplot)) for c in bar_counts
    ]
    total_height = sum(height_ratios)

    fig, axes = plt.subplots(
        nrows=len(processed_data),
        figsize=(width, total_height),
        gridspec_kw={"height_ratios": height_ratios},
        constrained_layout=True,
    )

    if len(processed_data) == 1:
        axes = [axes]

    for ax, (col_name, val_series) in zip(axes, processed_data):
        categories = val_series.index.tolist()
        percentages = val_series.values
        y_pos = np.arange(len(categories))

        labels = [
            (
                str(label)[:label_limit] + "…"
                if len(str(label)) > label_limit
                else str(label)
            )
            for label in categories
        ]

        ax.barh(y_pos, percentages, color=color, height=bar_height)

        for i, pct in enumerate(percentages):
            align = "right" if pct > 10 else "left"
            label_x = pct - 1 if pct > 10 else pct + 1
            ax.text(
                label_x,
                y_pos[i],
                f"{int(pct)}",
                va="center",
                ha=align,
                color="white" if pct > 10 else color,
                fontweight="bold",
                fontsize=9,
            )

        ax.set_yticks(y_pos)
        ax.set_yticklabels(labels, fontsize=9)
        ax.invert_yaxis()
        ax.set_xlim(0, 100)
        ax.set_xlabel("Percentage")
        ax.set_title(col_name, fontsize=11)
        ax.grid(axis="x", linestyle="--", alpha=0.3)
        ax.tick_params(axis="x", labelsize=9)

    fig.suptitle(
        f"Demographic Distributions for {persona_value}", fontsize=14, fontweight="bold"
    )
    if save_path:
        fig.savefig(save_path, dpi=300)
        print(f"Saved: {save_path}")
    plt.close(fig)


# Apply to all profiles
def plot_all_profiles(df, profile_column, profiles, output_dir, color_map):
    for profile in profiles:
        color = color_map.get(profile, "#3366FF")
        filename = f"{profile.replace(' ', '_')}_demographics.png"
        save_path = os.path.join(output_dir, filename)
        plot_demographics(df, profile_column, profile, color=color, save_path=save_path)


profile_colors = {
    "Tourist": "#3366FF",  # Blue (calm, passive visitor)
    "Personal Involvement": "#FF6B6B",  # Red-orange (emotional/active connection)
    "Student": "#28B463",  # Green (learning, youth)
    "Researcher": "#9B59B6",  # Purple (inquiry, academia)
}


plot_all_profiles(
    df_survey_persona,
    "profile",
    ["Tourist", "Personal Involvement", "Student", "Researcher"],
    "figures",
    profile_colors,
)

# %%

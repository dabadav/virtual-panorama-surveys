# %%
from jinja2 import Template

import yaml

def load_personas_from_yaml(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        personas = yaml.safe_load(f)
    return personas

personas = load_personas_from_yaml("personas.yaml")

# HTML Template with improved iteration
template_str = """
<!DOCTYPE html>
<html>
<head>
    <title>Persona Survey Mapping Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 2em; background: #f4f6f9; }
        .container { display: flex; flex-wrap: wrap; gap: 30px; justify-content: flex-start; }
        .persona {
            background: white;
            border: 1px solid #ccc;
            border-radius: 8px;
            width: 600px;
            padding: 16px 20px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.08);
        }
        .persona h2 {
            font-size: 1.2em;
            color: #2c3e50;
            margin-top: 0;
            margin-bottom: 1em;
        }
        table {
            width: 100%;
            border-spacing: 0;
        }
        td {
            padding: 6px 0;
            vertical-align: top;
        }
        .label {
            font-weight: bold;
            width: 45%;
            color: #444;
        }
        .value {
            width: 55%;
        }
        .pill {
            display: inline-block;
            background-color: #e0ecf8;
            color: #2c3e50;
            padding: 4px 8px;
            margin: 2px 4px 2px 0;
            font-size: 0.85em;
            border-radius: 10px;
        }
        .survey-label {
            font-style: italic;
            color: #1a73e8;
            font-size: 0.85em;
            display: inline-block;
        }
        .tr-tight td {
            padding-top: 5px;
            padding-bottom: 5px;
        }
        h1 {
            text-align: center;
            margin-bottom: 1em;
            color: #333;
        }
        tbody.row-group {
            border-top: 2px solid #ccc;
            margin-top: 8px;
        }
        tbody.row-group:first-of-type {
            border-top: none;
        }
        tr.tr-tight td {
            padding-top: 2px;
            padding-bottom: 2px;
        }
    </style>
</head>
<body>
    <h1>Mapping Survey Respondents to User Personas</h1>
    <div class="container">
    {% for p in personas %}
        <div class="persona">
            <h2>{{ p.name }}</h2>
            <table>
                <tbody class="row-group">
                    <tr>
                        <td class="label">Age</td>
                        <td class="value">{{ p.age_group[0] }}</td>
                    </tr>
                    {% for mapping in p.age_group[1] %}
                    <tr class="tr-tight">
                        <td class="label"><span class="survey-label">{{ mapping[0] }}</span></td>
                        <td class="value">
                            {% for val in mapping[1] %}
                                <span class="pill">{{ val }}</span>
                            {% endfor %}
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>

                <tbody class="row-group">
                    <tr>
                        <td class="label">Engagement</td>
                        <td class="value">{{ p.engagement[0] }}</td>
                    </tr>
                    {% for mapping in p.engagement[1] %}
                    <tr class="tr-tight">
                        <td class="label"><span class="survey-label">{{ mapping[0] }}</span></td>
                        <td class="value">
                            {% for val in mapping[1] %}
                                <span class="pill">{{ val }}</span>
                            {% endfor %}
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>

                <tbody class="row-group">
                    <tr>
                        <td class="label">Content Preference</td>
                        <td class="value">{{ p.content[0] }}</td>
                    </tr>
                    {% for mapping in p.content[1] %}
                    <tr class="tr-tight">
                        <td class="label"><span class="survey-label">{{ mapping[0] }}</span></td>
                        <td class="value">
                            {% for val in mapping[1] %}
                                <span class="pill">{{ val }}</span>
                            {% endfor %}
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>

                <tbody class="row-group">
                    <tr>
                        <td class="label">Goals</td>
                        <td class="value">{{ p.goals[0] }}</td>
                    </tr>
                    {% for mapping in p.goals[1] %}
                    <tr class="tr-tight">
                        <td class="label"><span class="survey-label">{{ mapping[0] }}</span></td>
                        <td class="value">
                            {% for val in mapping[1] %}
                                <span class="pill">{{ val }}</span>
                            {% endfor %}
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    {% endfor %}
    </div>
</body>
</html>
"""


# Render template
template = Template(template_str)
html_output = template.render(personas=personas)

# Save HTML to file
file_path = "reports/persona_mapping.html"
with open(file_path, "w", encoding="utf-8") as f:
    f.write(html_output)

file_path

# %%
from utils import combine_html

combine_html([
    ("reports/persona_mapping.html", "Persona Mapping"),
    ("reports/UniqueAnswers_perQuestion_Translated.html", "Survey Answers")
])
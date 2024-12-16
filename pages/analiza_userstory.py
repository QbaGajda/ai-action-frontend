import os
import streamlit as st
import pandas as pd
import openai
from atlassian.jira import Jira
from dotenv import load_dotenv
import seaborn as sns

from model.Models import APIClient

load_dotenv()

st.set_page_config(page_title="PowerFarm 24 Agent", page_icon="🧊", layout="wide", initial_sidebar_state="auto")


title_template = """
<div style="background-color:tomato;padding:10px;border-radius:10px">
<h1 style="color:white;text-align:center;">PowerFarm 24 Agent</h1>
</div>
"""

st.markdown(title_template, unsafe_allow_html=True)

st.sidebar.image("mir.jpg", use_container_width=True)


api_client = APIClient("http://localhost:8000")

def write_string_to_file(filename, string):
    with open(filename, 'w') as file:
        file.write(string)


def classify_jira_issue(description):
    good_practices = """
            Writing User Stories
        During Sprint Grooming, groups of features / requirements, or Epics, are broken down into user stories by the Product Owner. Then Sprint Planning is used to estimate the level of effort to complete a user story through tasking by the Scrum Team.
        The user story is a short, simple description of a feature or function written from the perspective of the end user:
        As a [ type of user ], I want [ some goal, function ] so that [ some reason ].
        An example:
        As a Leasing Specialist, I want the ability to upload an SF-81 document so that I can attach it to my lease file.
        When writing a user story, it requires key content:
        Description, or summary of the feature or requirement that meets the business need
        Acceptance criteria, or the actions necessary to call the user story “done,” in other words, meet the established Definition of Done (DoD)
        And any other items as identified by the team (e.g. Epic, Label, etc.) and within their tool of choice (e.g. JIRA, Rally, etc.),
            User story independence is ensured when the delivery increment has been fully decomposed; this allows for the appropriate tasking, estimation, sizing, and testability of the effort. The Product Owner negotiates the prioritization of the functionality with the Scrum Team against user needs, while the value of the user story drives its priority.
        Further, testability of the user story is captured in the acceptance criteria; it should denote the “The Who” (user), “The What” (capability), and “The Why” (outcome) of the increment. For additional detail on writing user stories, check out our User Story Examples, or review Defining When a Requirement is Complete on defining acceptance criteria.
        """
    system = "You are tester assistant. You task is to help tester analyse quality of JIRA issue description"
    prompt = (f"Analyse JIRA issue description.Classify as Low, Medium, High. "
              f"If description os empty give Low classification. Base your analysis on this good practice. "
              f"Good practice:\n {good_practices} "
              f"Expected format of feedback is only classification: Low, Medium, High \n ##### {description}")
    response = api_client.generate_text(system+"\n"+prompt,max_tokens=2000,temperature=0.8)

    return response


def get_description_feedback(description):
    good_practices = """
            Writing User Stories
        During Sprint Grooming, groups of features / requirements, or Epics, are broken down into user stories by the Product Owner. Then Sprint Planning is used to estimate the level of effort to complete a user story through tasking by the Scrum Team.
        The user story is a short, simple description of a feature or function written from the perspective of the end user:
        As a [ type of user ], I want [ some goal, function ] so that [ some reason ].
        An example:
        As a Leasing Specialist, I want the ability to upload an SF-81 document so that I can attach it to my lease file.
        When writing a user story, it requires key content:
        Description, or summary of the feature or requirement that meets the business need
        Acceptance criteria, or the actions necessary to call the user story “done,” in other words, meet the established Definition of Done (DoD)
        And any other items as identified by the team (e.g. Epic, Label, etc.) and within their tool of choice (e.g. JIRA, Rally, etc.),
            User story independence is ensured when the delivery increment has been fully decomposed; this allows for the appropriate tasking, estimation, sizing, and testability of the effort. The Product Owner negotiates the prioritization of the functionality with the Scrum Team against user needs, while the value of the user story drives its priority.
        Further, testability of the user story is captured in the acceptance criteria; it should denote the “The Who” (user), “The What” (capability), and “The Why” (outcome) of the increment. For additional detail on writing user stories, check out our User Story Examples, or review Defining When a Requirement is Complete on defining acceptance criteria.
        """
    system = "You are text assistant. You task is to help  analyse quality of JIRA issue description. Answer only in english."
    prompt = (f"Analyse JIRA issue description and give short feedback in few words."
              f"If description os empty give information about lack of description. "
              f"Base your analysis on this good practice. "
              f"Good practice: {good_practices}.\n "
              f"Expected format of feedback is explanation what is lack in description  \n "
              f"##### {description}")

    response = api_client.generate_text(system+"\n"+prompt,max_tokens=2000,temperature=0.8)

    return response




token = os.getenv("JIRA_API_TOKEN")
jira = Jira(url="https://makeitright.atlassian.net/", username="jakub.gajda@makeitright.pl", password=token, cloud=True)

st.title("JIRA issue classification")

list_of_projects = jira.get_all_projects()
list_of_projects_names = []
for name in list_of_projects:
    list_of_projects_names.append(name['name'])
project_name = st.multiselect("Wybierz projekt", list_of_projects_names,max_selections=1)

project_key = list_of_projects[list_of_projects_names.index(project_name[0])]['key']

st.write("Wybrany projekt: ", project_key)

get_all_reporters = jira.get_all_project_issues(project_key)
list_of_reporters_distinct = []
for reporter in get_all_reporters:
    list_of_reporters_distinct.append(reporter["fields"]["reporter"]["displayName"])

reporter = st.multiselect("Wybierz użytkownika", set(list_of_reporters_distinct),max_selections=1)

check = st.button("Sprawdź")



if check:
    table = pd.DataFrame(columns=["JIRA ID", "Classification", "Explanation","User"])
    list_of_jira_id_scrapped = jira.get_all_project_issues(project_key, fields=['key'])
    list_of_jira_ids = [issue['key'] for issue in list_of_jira_id_scrapped]
    with st.spinner("Trwa analiza ..."):
        for i, issue in enumerate(list_of_jira_ids):
            table.loc[i] = [issue, classify_jira_issue(jira.issue(issue)['fields']['description']),
                            str(get_description_feedback(jira.issue(issue)['fields']['description'])), jira.issue(issue)["fields"]["reporter"]["displayName"] in reporter]
        st.dataframe(table)




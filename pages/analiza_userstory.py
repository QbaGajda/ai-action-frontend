import os
import streamlit as st
import pandas as pd
import openai
from atlassian.jira import Jira
from dotenv import load_dotenv
import seaborn as sns



load_dotenv()


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
    kod_gotowy = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are tester assistant. You task is to help tester analyse quality of JIRA issue description"
            },
            {
                "role": "user",
                "content": "Analyse JIRA issue description.Classify as Low, Medium, High."
                           "If description os empty give Low classification. "
                           "Base your analysis on this good practice. Good practice:\n "
                           + good_practices + "Expected format of feedback is only classification: Low, Medium, High \n ##### " + str(
                    description)
            }
        ],
        temperature=0.8,
        max_tokens=2000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    kodzik = kod_gotowy.choices[0].message.content
    return kodzik


def get_code_feedback(description):
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

    kod_gotowy = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are text assistant. You task is to help  analyse quality of JIRA issue description. Answer only in english."
            },
            {
                "role": "user",
                "content": "Analyse JIRA issue description and give short feedback in few words"
                           "If description os empty give information about lack of description. "
                           "Base your analysis on this good practice. Good practice:\n "
                           + good_practices + "Expected format of feedback is explanation what is lack in description  \n ##### " + str(
                    description)
            }
        ],
        temperature=0.8,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    kodzik = kod_gotowy.choices[0].message.content
    return kodzik


token = os.getenv("JIRA_API_TOKEN")
jira = Jira(url="https://makeitright.atlassian.net/", username="jakub.gajda@makeitright.pl", password=token, cloud=True)

st.title("JIRA issue classification")
projekt = st.text_input("Podaj projekt JIRA")

sprawdz = st.button("Sprawdź")

if sprawdz:
    table = pd.DataFrame(columns=["JIRA ID", "Classification", "Explanation"])
    list_of_jira_id_scrapped = jira.get_all_project_issues(projekt, fields=['key'])
    list_of_jira_ids = [issue['key'] for issue in list_of_jira_id_scrapped]
    with st.spinner("Trwa analiza ..."):
        for i, issue in enumerate(list_of_jira_ids):
            table.loc[i] = [issue, classify_jira_issue(jira.issue(issue)['fields']['description']),
                            str(get_code_feedback(jira.issue(issue)['fields']['description']))]
        st.table(table)
        st.bar_chart(table["Classification"].value_counts())
        st.area_chart(table["Classification"].value_counts())

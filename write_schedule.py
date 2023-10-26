import pandas as pd
import numpy as np


data_sett = {
    "PM": ["Артем", "Артем", "Артем", "Иван", "Тимур"],
    "Timeslot": ["18:00-18:30", "18:30-19:00", "19:00-19:30", "12:00-12:30", "14:00-14:30"],
    "Level": ["Junior", "Junior", "Beginner", "Beginner+", "Beginner+"],
    "Students": ["Матвей, Дмитрий, Виктор", "Иван, Василий, Сахар", "Артем, Артемий, Артен", "М, М2, М3", "человек3, человек2, человек1"],
    "Trello": ["https://trello.com/b/gyAquy6P/4-новички-2000-2020-виктор-wishkin-viktorshish-дмитрий-dmitrykiselevmoscow-kdv150275-матвей-киселев-matvey2566-id699813203", "https://trello.com/b/gyAquy6P/4-новички-2000-2020-виктор-wishkin-viktorshish-дмитрий-dmitrykiselevmoscow-kdv150275-матвей-киселев-matvey2566-id699813203", "https://trello.com/b/gyAquy6P/4-новички-2000-2020-виктор-wishkin-viktorshish-дмитрий-dmitrykiselevmoscow-kdv150275-матвей-киселев-matvey2566-id699813203", "https://trello.com/b/gyAquy6P/4-новички-2000-2020-виктор-wishkin-viktorshish-дмитрий-dmitrykiselevmoscow-kdv150275-матвей-киселев-matvey2566-id699813203", "https://trello.com/b/gyAquy6P/4-новички-2000-2020-виктор-wishkin-viktorshish-дмитрий-dmitrykiselevmoscow-kdv150275-матвей-киселев-matvey2566-id699813203"]
}
data_set_nd = {
    "Student": ["Викторц", "Димитрий", "ААрт", "Student", "std123"],
    "Level": ["Beginner", "Beginner", "Junior", "Junior", "Beginner+"],
    "Status": ["Waiting", "waiting", "waiting", "started", "missing"],
    "Interval-reqested": [np.nan, np.nan, np.nan, np.nan, np.nan]
}

data_jsonn = {"teams": [
    {"PM": "Артем", "Timeslot": "18:00-18:30", "Level": "Junior", "Students": ["Матвей", "Дмитрий", "Виктор"], "Trello": "https://trello.com/b/gyAquy6P/4-новички-2000-2020-виктор-wishkin-viktorshish-дмитрий-dmitrykiselevmoscow-kdv150275-матвей-киселев-matvey2566-id699813203"},
    {"PM": "Артем", "Timeslot": "18:30-19:00", "Level": "Junior", "Students": ["Иван", "Василий", "Сахар"], "Trello": "https://trello.com/b/gyAquy6P/4-новички-2000-2020-виктор-wishkin-viktorshish-дмитрий-dmitrykiselevmoscow-kdv150275-матвей-киселев-matvey2566-id699813203"},
    {"PM": "Артем", "Timeslot": "19:00-19:30", "Level": "Beginner", "Students": ["Артем", "Артемий", "Артен"], "Trello": "https://trello.com/b/gyAquy6P/4-новички-2000-2020-виктор-wishkin-viktorshish-дмитрий-dmitrykiselevmoscow-kdv150275-матвей-киселев-matvey2566-id699813203"},
    {"PM": "Иван", "Timeslot": "12:00-12:30", "Level": "Beginner+", "Students": ["M", "M2", "M3"], "Trello": "https://trello.com/b/gyAquy6P/4-новички-2000-2020-виктор-wishkin-viktorshish-дмитрий-dmitrykiselevmoscow-kdv150275-матвей-киселев-matvey2566-id699813203"},
    {"PM": "Тимур", "Timeslot": "14:00-14:30", "Level": "Beginner+", "Students": ["человек1", "человек2", "человек3"], "Trello": "https://trello.com/b/gyAquy6P/4-новички-2000-2020-виктор-wishkin-viktorshish-дмитрий-dmitrykiselevmoscow-kdv150275-матвей-киселев-matvey2566-id699813203"},
]}

data_jsonn_nd = {"neuds": [
    {"Student": "Викторц", "Level": "Beginner", "Status": "Waiting", "Interval-requested": np.nan},
    {"Student": "Димитрий", "Level": "Beginner", "Status": "Waiting", "Interval-requested": np.nan},
    {"Student": "ААрт", "Level": "Junior", "Status": "Waiting", "Interval-requested": np.nan},
    {"Student": "Student", "Level": "Junior", "Status": "started", "Interval-requested": np.nan},
    {"Student": "std", "Level": "Beginner+", "Status": "missing", "Interval-requested": np.nan},
]}


def format_data(data_json):
    data_set = {
        "PM": [], "Timeslot": [], "Level": [], "Students": [], "Trello": []
    }
    for team in data_json["teams"]:
        data_set["PM"].append(team["PM"])
        data_set["Timeslot"].append(team["Timeslot"])
        data_set["Level"].append(team["Level"])
        students = ""
        for std in team["Students"][:len(team["Students"])-1]: students += std + ", "
        students += team["Students"][-1]
        data_set["Students"].append(students)
        data_set["Trello"].append(team["Trello"])
    return data_set


def format_data_neuds(data_json):
    data_set = {
        "Student": [], "Level": [], "Status": [], "Interval-requested": []
    }
    for student in data_json["neuds"]:
        data_set["Student"].append(student["Student"])
        data_set["Level"].append(student["Level"])
        data_set["Status"].append(student["Status"])
        data_set["Interval-requested"].append(student["Interval-requested"])
    return data_set


# Converting into dataframe
df = pd.DataFrame(format_data(data_jsonn))
df_nd = pd.DataFrame(format_data_neuds(data_jsonn_nd))

# Writing the data into the excel sheet
writer_obj = pd.ExcelWriter('Write.xlsx', engine='xlsxwriter')

df.to_excel(writer_obj, sheet_name='Teams')
df_nd.to_excel(writer_obj, sheet_name='"Неудачники"')

writer_obj.save()
print('Please check out the Write.xlsx file.')

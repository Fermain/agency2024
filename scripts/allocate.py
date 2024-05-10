import pandas as pd
import argparse

# Argument parsing
parser = argparse.ArgumentParser(description="Allocate teams and roles based on signup data.")
parser.add_argument("input_path", help="Path to the input CSV file containing the signup data")
parser.add_argument("output_path", help="Path to save the output CSV file with assigned teams and roles")
args = parser.parse_args()

# Load the original signup data from the input CSV
signup_data = pd.read_csv(args.input_path, delimiter=';')

# Define role quotas
desired_quotas = {
    'Scrum Master': 3,
    'Designer': 3,
    'Quality Assurance': 3,
    'Developer': 16
}

# Initialize dictionaries to hold assignments
assigned_students = {
    'Scrum Master': [],
    'Designer': [],
    'Quality Assurance': [],
    'Developer': []
}

# Sort students by their preferences for each role, with 10 being the highest
roles = ['Scrum Master', 'Designer', 'Quality Assurance', 'Developer']
sorted_students = {}

for role in roles:
    sorted_students[role] = signup_data.sort_values(by=[role], ascending=False)

# Helper function to allocate students to a role based on sorted preferences
def allocate_students(role, quota):
    for _, student in sorted_students[role].iterrows():
        student_id = student['ID']
        if len(assigned_students[role]) < quota and not any(student_id in v for v in assigned_students.values()):
            assigned_students[role].append(student_id)

# Allocate students to each role in order of priority
allocate_students('Scrum Master', desired_quotas['Scrum Master'])
allocate_students('Designer', desired_quotas['Designer'])
allocate_students('Quality Assurance', desired_quotas['Quality Assurance'])
allocate_students('Developer', desired_quotas['Developer'])

# Organize the assignments into teams
design_team = {
    'Scrum Master': assigned_students['Scrum Master'][0],
    'Designers': assigned_students['Designer']
}
qa_team = {
    'Scrum Master': assigned_students['Scrum Master'][1],
    'Quality Assurance': assigned_students['Quality Assurance']
}
development_team = {
    'Scrum Master': assigned_students['Scrum Master'][2],
    'Developers': assigned_students['Developer']
}

# Initialize empty lists to hold the new columns
team_column = []
role_column = []

# Define a function to determine the team and role for a student
def determine_team_role(student_id):
    if student_id == design_team['Scrum Master']:
        return 'Design', 'Scrum Master'
    elif student_id in design_team['Designers']:
        return 'Design', 'Designer'
    elif student_id == qa_team['Scrum Master']:
        return 'QA', 'Scrum Master'
    elif student_id in qa_team['Quality Assurance']:
        return 'QA', 'QA Engineer'
    elif student_id == development_team['Scrum Master']:
        return 'Development', 'Scrum Master'
    elif student_id in development_team['Developers']:
        return 'Development', 'Developer'
    else:
        return 'Unassigned', 'Unassigned'

# Populate the new columns based on student IDs
for _, row in signup_data.iterrows():
    team, role = determine_team_role(row['ID'])
    team_column.append(team)
    role_column.append(role)

# Add the new columns to the original DataFrame
signup_data['Team'] = team_column
signup_data['Team Role'] = role_column

# Save the updated DataFrame to the output CSV file
signup_data.to_csv(args.output_path, index=False)

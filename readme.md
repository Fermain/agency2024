# Sorting Hat

The **Sorting Hat** package helps form balanced teams for project work while considering students' preferences for specific roles. It ensures adherence to predefined team structures and adds students to the appropriate GitHub teams.

## Features

1. **Team Allocation**: Assigns students to teams based on their preferences and role requirements.
2. **Data Mapping**: Merges real student data with anonymous allocations for the final team assignment.
3. **GitHub Team Management**: Automatically adds students to the appropriate GitHub teams.

## Prerequisites

- Python 3.x
- GitHub CLI (with necessary permissions)
- A GitHub organization and teams set up

## Package Structure

- `scripts/allocate.py`: Assigns teams and roles based on student preferences.
- `scripts/map.py`: Maps anonymous student data to real student data.
- `scripts/assign.sh`: Adds students to GitHub teams.
- `run.sh`: Orchestrates the entire process.

## Usage

### Running the Allocation and Mapping Process

1. Prepare the student data and anonymous signup files.
2. Run `run.sh` with the appropriate arguments:

   ```bash
   ./run.sh org_name ./data/anon_signup.csv ./data/student_data.csv

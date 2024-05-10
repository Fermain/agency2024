import pandas as pd
import argparse

# Argument parsing
parser = argparse.ArgumentParser(description="Map team assignments to student information.")
parser.add_argument("assignments_path", help="Path to the CSV file with team assignments")
parser.add_argument("info_path", help="Path to the CSV file containing student information")
parser.add_argument("output_path", help="Path to save the merged output CSV file")
args = parser.parse_args()

# Load the assignments and student info CSV files
assignments_df = pd.read_csv(args.assignments_path)

# Load the info CSV with the correct delimiter
info_df = pd.read_csv(args.info_path)

# Ensure info_df has the expected columns by renaming them
info_df.columns = info_df.columns.str.strip()  # Strip any whitespace from headers

# Rename columns to standard names based on positions
info_df = info_df.rename(columns={
    info_df.columns[0]: 'ID', 
    info_df.columns[4]: 'Name', 
    info_df.columns[3]: 'Email', 
    info_df.columns[6]: 'GitHub'
})

# Extract only the relevant columns
info_df = info_df[['ID', 'Name', 'Email', 'GitHub']]

# Merge the assignments with the info data based on the ID
merged_df = pd.merge(assignments_df, info_df, on='ID', how='left')

# Place 'Name', 'Email', and 'GitHub' columns at positions 2, 3, and 4 respectively
cols = list(merged_df.columns)
# Remove the three columns and re-insert them at desired positions
cols.insert(1, cols.pop(cols.index('Name')))
cols.insert(2, cols.pop(cols.index('Email')))
cols.insert(3, cols.pop(cols.index('GitHub')))
# Reorder DataFrame
merged_df = merged_df[cols]

# Save the merged DataFrame to the output CSV
merged_df.to_csv(args.output_path, index=False)

print(f"Output saved to {args.output_path}")

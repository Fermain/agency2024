#!/bin/bash

# Ensure the correct number of arguments are provided
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 org_name anon_csv_path student_data_csv_path"
    exit 1
fi

# Organization name and input file paths
ORG_NAME=$1
ANON_CSV=$2
STUDENT_DATA_CSV=$3

# Verify that input files exist
if [ ! -f "$ANON_CSV" ]; then
    echo "Error: $ANON_CSV not found!"
    exit 1
fi

if [ ! -f "$STUDENT_DATA_CSV" ]; then
    echo "Error: $STUDENT_DATA_CSV not found!"
    exit 1
fi

# Output directory and file paths
OUTPUT_DIR="./output"
ALLOCATED_CSV="$OUTPUT_DIR/allocated.csv"
FINAL_CSV="$OUTPUT_DIR/final_team_assignments.csv"

# Create the output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Run allocate.py to assign teams and roles
echo "Running allocate.py..."
python scripts/allocate.py "$ANON_CSV" "$ALLOCATED_CSV"
if [ $? -ne 0 ]; then
    echo "Error running allocate.py"
    exit 1
fi

# Run map.py to add real student data
echo "Running map.py..."
python scripts/map.py "$ALLOCATED_CSV" "$STUDENT_DATA_CSV" "$FINAL_CSV"
if [ $? -ne 0 ]; then
    echo "Error running map.py"
    exit 1
fi

# Run assign.sh to add users to GitHub teams
echo "Running assign.sh..."
./scripts/assign.sh "$ORG_NAME" "final_team_assignments_edited.csv"
if [ $? -ne 0 ]; then
    echo "Error running assign.sh"
    exit 1
fi

rm -f "$ALLOCATED_CSV"

echo "All processes completed successfully."

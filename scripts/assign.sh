#!/bin/bash

# Check if the correct number of arguments are provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 org_name path_to_csv_file"
    exit 1
fi

# Organization name
ORG_NAME=$1

# CSV file path
CSV_FILE=$2

# Function to add user to a GitHub team
add_to_team() {
    local USERNAME=$1
    local TEAM=$2
    gh api --method PUT -H "Accept: application/vnd.github.v3+json" "/orgs/$ORG_NAME/teams/$TEAM/memberships/$USERNAME" -f role=member
}

# Read the CSV file line by line, skipping the header
# This will break if the structure of the form changes!!
# This should be procedural, by reading the headers
tail -n +2 "$CSV_FILE" | while IFS=';' read -r ID Name Email GitHub ScrumMaster QualityAssurance Designer Developer Team TeamRole; do
    # Trim leading/trailing whitespace
    Team=$(echo $Team | xargs)
    GitHub=$(echo $GitHub | xargs)

    # Determine the team name based on Team
    case $Team in
        Designers)
            TEAM_NAME="designers"
            ;;
        QA)
            TEAM_NAME="qa"
            ;;
        Developers)
            TEAM_NAME="developers"
            ;;
        *)
            echo "Unknown team: $Team for user $GitHub"
            continue
            ;;
    esac

    # Add user to the team
    echo "Adding $GitHub to $TEAM_NAME team"
    add_to_team "$GitHub" "$TEAM_NAME"
done

echo "All users processed."

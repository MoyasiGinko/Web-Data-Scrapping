import http.client
import json
import pandas as pd
import time  # Import time module to introduce delays

# Establish connection
conn = http.client.HTTPSConnection("v3.football.api-sports.io")

# Headers for the API request
headers = {
    'x-rapidapi-host': "v3.football.api-sports.io",
    'x-rapidapi-key': "5adead23bff31f104fa7f23dc0b1f8f2"
}

# Read the team IDs from the 'countries.xlsx' file
countries_df = pd.read_excel("./countries.xlsx")

# Verify that the necessary columns are present
required_columns = ['team_id']
for column in required_columns:
    if column not in countries_df.columns:
        print(f"Error: Missing '{column}' column in the countries.xlsx file.")
        exit()

# Extract team IDs
team_ids = countries_df['team_id'].tolist()

# Time interval between API calls (in seconds)
time_interval = 7  # Adjust to comply with API rate limits

# List to store all processed data
all_teams_data = []

# Iterate through each team ID
for team_id in team_ids:
    try:
        # Make the API request to get players for the team
        conn.request("GET", f"/players/squads?team={team_id}", headers=headers)

        # Get the response
        res = conn.getresponse()

        # If the response status is not 200, handle the error
        if res.status != 200:
            print(f"Error: Received status code {res.status} for team ID {team_id}")
            continue

        # Read and decode JSON data
        data = res.read()
        decoded_data = json.loads(data)

        # Extract 'response' data
        squads = decoded_data.get("response", [])

        # Process and extract data for each team and its players
        for squad_entry in squads:
            team_info = squad_entry.get("team", {})
            players = squad_entry.get("players", [])

            # Extract team details
            team_data = {
                "Team ID": team_info.get("id"),
                "Team Name": team_info.get("name"),
                "Team Logo": team_info.get("logo")
            }

            # Extract player details
            for player in players:
                player_data = {
                    "Player ID": player.get("id"),
                    "Player Name": player.get("name"),
                    "Age": player.get("age"),
                    "Number": player.get("number"),
                    "Position": player.get("position"),
                    "Photo": player.get("photo")
                }

                # Combine team and player data
                all_teams_data.append({**team_data, **player_data})

        # Add a delay after each API call
        time.sleep(time_interval)

    except Exception as e:
        print(f"Error processing team ID '{team_id}': {e}")
        continue

# Convert processed data to a DataFrame
df = pd.DataFrame(all_teams_data)

# Save the data to an Excel file
xlsx_filename = "teams_and_players.xlsx"
df.to_excel(xlsx_filename, index=False)
print(f"Data saved to {xlsx_filename}")

import http.client
import json
import pandas as pd

# Establish connection
conn = http.client.HTTPSConnection("v3.football.api-sports.io")

# Headers for the API request
headers = {
    'x-rapidapi-host': "v3.football.api-sports.io",
    'x-rapidapi-key': "d6b815adf9b03617d0bc56bb0f634783"
}

# Make the API request to get all teams (You can adjust this for specific leagues/teams)
conn.request("GET", "/teams?country=bangladesh", headers=headers)

# Get the response
res = conn.getresponse()
if res.status != 200:
    print(f"Error: Received status code {res.status}")
    exit()

# Read and decode JSON data
data = res.read()
decoded_data = json.loads(data)

print(decoded_data)

# Extract 'response' data
teams = decoded_data.get("response", [])

# Check if data exists
if not teams:
    print("No data found in the response.")
    exit()

# Process data
processed_teams = []
for team_entry in teams:
    team_info = team_entry.get("team", {})
    venue_info = team_entry.get("venue", {})

    # Append all team and venue data
    processed_teams.append({
        "Team ID": team_info.get("id"),
        "Team Name": team_info.get("name"),
        "Team Code": team_info.get("code"),
        "Team Country": team_info.get("country"),
        "Founded Year": team_info.get("founded"),
        "Is National Team": team_info.get("national"),
        "Team Logo": team_info.get("logo"),
        "Venue ID": venue_info.get("id"),
        "Venue Name": venue_info.get("name"),
        "Venue Address": venue_info.get("address"),
        "Venue City": venue_info.get("city"),
        "Venue Capacity": venue_info.get("capacity"),
        "Venue Surface": venue_info.get("surface"),
        "Venue Image": venue_info.get("image"),
    })

# Convert processed data to a DataFrame
df = pd.DataFrame(processed_teams)

# Save to Excel file
xlsx_filename = "teams.xlsx"
df.to_excel(xlsx_filename, index=False)
print(f"Data saved to {xlsx_filename}")

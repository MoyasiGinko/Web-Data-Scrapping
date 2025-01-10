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

# Make the API request to get all leagues
conn.request("GET", "/leagues", headers=headers)

# Get the response
res = conn.getresponse()
if res.status != 200:
    print(f"Error: Received status code {res.status}")
    exit()

# Read and decode JSON data
data = res.read()
decoded_data = json.loads(data)

# Extract 'response' data
leagues = decoded_data.get("response", [])

# Check if data exists
if not leagues:
    print("No data found in the response.")
    exit()

# Process data, one entry per league
processed_leagues = []
for league_entry in leagues:
    league_info = league_entry.get("league", {})
    country_info = league_entry.get("country", {})

    # Append the league data only once
    processed_leagues.append({
        "League ID": league_info.get("id"),
        "League Name": league_info.get("name"),
        "League Type": league_info.get("type"),
        "League Logo": league_info.get("logo"),
        "Country Name": country_info.get("name"),
        "Country Code": country_info.get("code"),
        "Country Flag": country_info.get("flag"),
    })

# Convert processed data to a DataFrame
df = pd.DataFrame(processed_leagues)

# Save to Excel file
xlsx_filename = "leagues.xlsx"
df.to_excel(xlsx_filename, index=False)
print(f"Data saved to {xlsx_filename}")

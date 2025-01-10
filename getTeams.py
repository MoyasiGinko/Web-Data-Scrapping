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

# Read the countries from the 'countries.xlsx' file
countries_df = pd.read_excel("./countries.xlsx")

# Verify that the necessary columns are present
required_columns = ['name', 'code', 'flag']
for column in required_columns:
    if column not in countries_df.columns:
        print(f"Error: Missing '{column}' column in the countries.xlsx file.")
        exit()

# Filter out countries with an empty or missing code
countries_df_filtered = countries_df[countries_df['code'].notna() & (countries_df['code'] != '')]

# Get the list of countries to process
countries = countries_df_filtered['name'].tolist()

# Initialize list to hold all processed team data
all_teams_data = []

# Time interval between API calls (in seconds)
time_interval = 7  # 60 seconds divided by 9 calls = ~6.67 seconds per call

# Iterate through each country
for country in countries:
    try:
        # Make the API request to get teams in the country
        conn.request("GET", f"/teams?search={country}", headers=headers)

        # Get the response
        res = conn.getresponse()

        # If the response status is not 200, handle the error
        if res.status != 200:
            print(f"Error: Received status code {res.status} for {country}")
            continue

        # Read and decode JSON data
        data = res.read()
        decoded_data = json.loads(data)

        # Extract 'response' data
        teams = decoded_data.get("response", [])

        # Check if teams data exists for the country
        if not teams:
            print(f"No teams found for {country}.")
            continue

        # Process and extract data for each team
        for team_entry in teams:
            team_info = team_entry.get("team", {})
            venue_info = team_entry.get("venue", {})

            # Append team and venue data to the list
            all_teams_data.append({
                "Country": country,
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

        # Add a delay after each API call (6.67 seconds between calls)
        time.sleep(time_interval)

    except Exception as e:
        print(f"Error processing country '{country}': {e}")
        continue

# Convert processed data to a DataFrame
df = pd.DataFrame(all_teams_data)

# Save the data to an Excel file
xlsx_filename = "teams_by_country.xlsx"
df.to_excel(xlsx_filename, index=False)
print(f"Data saved to {xlsx_filename}")

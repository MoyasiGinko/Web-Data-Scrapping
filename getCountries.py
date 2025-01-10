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

# Make the API request
conn.request("GET", "/teams/countries", headers=headers)

# Get the response
res = conn.getresponse()
if res.status != 200:
    print(f"Error: Received status code {res.status}")
    exit()

# Read and decode JSON data
data = res.read()
decoded_data = json.loads(data)

# Extract 'response' data
countries = decoded_data.get("response", [])

# Check if data exists
if not countries:
    print("No data found in the response.")
    exit()

# Convert the list of countries to a DataFrame
df = pd.DataFrame(countries)

# Save to CSV file
csv_filename = "countries.csv"
df.to_csv(csv_filename, index=False)
print(f"Data saved to {csv_filename}")

# Save to Excel file
xlsx_filename = "countries.xlsx"
df.to_excel(xlsx_filename, index=False)
print(f"Data saved to {xlsx_filename}")

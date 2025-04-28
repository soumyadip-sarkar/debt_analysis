import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# Wikipedia URL
url = "https://en.wikipedia.org/wiki/Classification_of_Indian_cities"

# Request page content
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Find the HRA classification table
hra_table = soup.find('table', {'class': 'wikitable'})

# Extract all rows from the table
rows = hra_table.find_all('tr')

# Initialize variable to hold Tier-2 cities (Y classification)
tier2_cities = []

# Loop through rows to find the 'Y' classification row
for row in rows:
    cells = row.find_all('td')
    if cells:
        if cells[0].text.strip() == 'Y':
            # Found the 'Y' classification row — get cities from second column
            cities_text = cells[1].get_text(separator=",").strip()
            # Split, strip, and remove empty strings
            tier2_cities = [city.strip() for city in cities_text.split(",") if city.strip()]
            break

# Convert to DataFrame
tier2_df = pd.DataFrame(tier2_cities, columns=["City"])

# Remove unwanted rows
tier2_df = tier2_df[~tier2_df['City'].isin(['and', '.'])]

# Show DataFrame
print(tier2_df)

# Save to CSV
tier2_df.to_csv("data/tier2_cities.csv", index=False)

print("Clean Tier-2 (Y classification) cities list saved")


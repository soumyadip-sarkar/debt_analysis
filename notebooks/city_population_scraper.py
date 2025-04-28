import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
import os

# Fetch the website content
url = "https://en.wikipedia.org/wiki/List_of_cities_in_India_by_population"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# Find all tables with class 'wikitable'
tables = soup.find_all("table", {"class": "wikitable"})

# Read both tables separately
df1 = pd.read_html(StringIO(str(tables[0])))[0]
df2 = pd.read_html(StringIO(str(tables[1])))[0]

# Clean columns for both DataFrames
df1.columns = [col.strip() for col in df1.columns]
df2.columns = [col.strip() for col in df2.columns]

# Remove unwanted columns
df1 = df1.drop(columns=[col for col in df1.columns if '2001' in col or 'Reference' in col or 'Unnamed' in col], errors='ignore')
df2 = df2.drop(columns=[col for col in df2.columns if '2001' in col or 'Reference' in col or 'Unnamed' in col], errors='ignore')

# Standardize column names
df1.rename(columns={'Population (2011)[3]': 'Population (2011)',
                    'State or union territory': 'State'}, inplace=True)
df2.rename(columns={'Population (2011)[5]': 'Population (2011)',
                    'State or union territory': 'State'}, inplace=True)

# Remove footnotes from 'City' and 'Population' columns in both
def clean_text(s):
    return str(s).replace('―', '').replace('–', '-').replace('—', '-').replace('−', '-').replace('?', '').strip()

df1['City'] = df1['City'].str.replace(r'\[.*?\]', '', regex=True).apply(clean_text)
df2['City'] = df2['City'].str.replace(r'\[.*?\]', '', regex=True).apply(clean_text)

df1['Population (2011)'] = df1['Population (2011)'].astype(str).str.replace(r'[^0-9]', '', regex=True)
df2['Population (2011)'] = df2['Population (2011)'].astype(str).str.replace(r'[^0-9]', '', regex=True)

# Convert to numeric
df1['Population (2011)'] = pd.to_numeric(df1['Population (2011)'], errors='coerce').astype('Int64')
df2['Population (2011)'] = pd.to_numeric(df2['Population (2011)'], errors='coerce').astype('Int64')

# Concatenate both cleaned DataFrames
combined_df = pd.concat([df1, df2], ignore_index=True)

# Remove empty cities
combined_df = combined_df[combined_df['City'].notnull() & (combined_df['City'] != '')]

# Drop duplicate cities (keep first occurrence)
combined_df = combined_df.drop_duplicates(subset='City')

# Reset index
combined_df.reset_index(drop=True, inplace=True)

# Project Population for 2024 using 4.5% annual growth rate
growth_rate = 0.045
years = 2024 - 2011
combined_df['Population (2024 Estimate)'] = (combined_df['Population (2011)'] * ((1 + growth_rate) ** years)).round(0).astype('Int64')

# Add Working Population using Worker Population Ratio (WPR)
wpr = 0.40  # 40% average for urban India
combined_df['Working Population (2024 Estimate)'] = (combined_df['Population (2024 Estimate)'] * wpr).round(0).astype('Int64')

# Save to CSV
os.makedirs("data/cleaned", exist_ok=True)
combined_df.to_csv("data/cleaned/all_indian_cities_population_cleaned.csv", index=False)

# Preview final DataFrame
print(combined_df.head(20))

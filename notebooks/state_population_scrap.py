import pdfplumber
import pandas as pd
import re

# Step 1: Define paths
pdf_path = "../data/Aadhaar_Saturation_Report_31102024.pdf"
master_states_path = "../data/all_scheduled_commercial_banks.csv"
output_path = "../data/state_population_workingpopulation_final_clean.csv"

# Step 2: Extract Data
data = []

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        lines = text.split("\n")
        for line in lines:
            if re.match(r"^\d+\s", line):
                match = re.match(r"^\d+\s+(.+?)\s+([\d,]+)\s+[\d,]+\s+\d+(\.\d+)?%", line)
                if match:
                    state = match.group(1).replace("**", "").strip()
                    population = int(match.group(2).replace(",", "").strip())
                    data.append((state, population))

# Step 3: Create DataFrame
df = pd.DataFrame(data, columns=["State", "Population_2024"])

# Step 4: Preview the dataset
print("\n📋 Preview of extracted data:")
print(df.head(10))

# Step 5: Fix State Names If They Have Numbers
# (Move last number from state name to become prefix of population)
def fix_state_name_and_population(row):
    parts = row['State'].split()
    if parts[-1].isdigit():
        wrong_number = parts[-1]
        correct_state = " ".join(parts[:-1])
        correct_population = int(str(wrong_number) + str(row['Population_2024']))
        return pd.Series([correct_state, correct_population])
    else:
        return pd.Series([row['State'], row['Population_2024']])

df[['State', 'Population_2024']] = df.apply(fix_state_name_and_population, axis=1)

# Step 6: Preview after fixing
print("\n📋 Preview after fixing state names and populations:")
print(df.head(36))

# Step 7: Load Master State List
master_df = pd.read_csv(master_states_path)

# Check which states are in your extracted DataFrame but not in master
master_states = set(master_df['State'].str.strip().unique())
extracted_states = set(df['State'].str.strip().unique())

missing_in_master = extracted_states - master_states
print("\n❌ ERROR: Some extracted state names do not match the master list:")
for state in missing_in_master:
    print(f" - {state}")
print("\nFix the issues manually")

# Step 8: Calculate Working Population
df["Working_Population"] = (df["Population_2024"] * 0.4).astype(int)

# Step 9: Save the cleaned CSV
df.to_csv(output_path, index=False)
print(f"\n✅ Final clean CSV saved at: {output_path}")

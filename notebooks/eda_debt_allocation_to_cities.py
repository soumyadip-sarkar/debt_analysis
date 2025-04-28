import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load the debt allocation data
file_path = os.path.join("data", "cleaned", "debt_allocation_to_cities.csv")
df = pd.read_csv(file_path)

# Preview the first 10 rows
print(df.head(10))

# Check data info
print(df.info())

# Sort data by borrowing amount in descending order
top_20_cities = df.sort_values(by='City Total Amount Outstanding ( ₹ Crores)', ascending=False).head(20)

# Set plot style
plt.style.use('seaborn-v0_8-darkgrid')

# Create horizontal barplot
plt.figure(figsize=(12, 8))
sns.barplot(
    x='City Total Amount Outstanding ( ₹ Crores)', 
    y='City', 
    data=top_20_cities, 
    palette='viridis'
)

# Set titles and labels
plt.title("Top 20 Indian Cities by Borrowing Amount (₹)", fontsize=16)
plt.xlabel("Borrowing Amount (₹ Crores)", fontsize=12)
plt.ylabel("City", fontsize=12)

# Display the plot
plt.tight_layout()
plt.show()

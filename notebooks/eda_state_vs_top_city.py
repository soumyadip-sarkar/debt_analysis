import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
cities_df = pd.read_csv("data/cleaned/debt_allocation_to_cities.csv")
state_df = pd.read_csv("data/all_scheduled_commercial_banks.csv")

# Find top city per state
top_city_per_state = cities_df.loc[cities_df.groupby('State')['City Total Amount Outstanding ( ₹ Crores)'].idxmax()]

# Merge with total state borrowing data
merged_df = pd.merge(state_df, top_city_per_state, on='State')

# Sort by total borrowing for clearer visualization
merged_df = merged_df.sort_values(by='Total Amount Outstanding ( ₹ Crores)', ascending=False)

# Set plot style
plt.style.use('seaborn-v0_8-darkgrid')

# Set figure size
plt.figure(figsize=(14, 8))

# Barplot for total state borrowing
sns.barplot(
    x='Total Amount Outstanding ( ₹ Crores)', 
    y='State', 
    data=merged_df, 
    color='skyblue', 
    label='Total State Borrowing'
)

# Barplot for top city borrowing
sns.barplot(
    x='City Total Amount Outstanding ( ₹ Crores)', 
    y='State', 
    data=merged_df, 
    color='salmon', 
    label='Top City Borrowing'
)

# Add labels and title
plt.xlabel("Outstanding Amount (₹ Crores)", fontsize=12)
plt.ylabel("State", fontsize=12)
plt.title("State Outstanding Amount vs Top City Outstanding Amount", fontsize=16)
plt.legend()

# Tidy layout and show
plt.tight_layout()
plt.show()

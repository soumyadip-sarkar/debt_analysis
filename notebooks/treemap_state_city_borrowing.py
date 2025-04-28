import pandas as pd
import plotly.express as px
import webbrowser
import os

# Load the data
df = pd.read_csv("data/cleaned/debt_allocation_to_cities.csv")

# Create treemap: State -> City
fig = px.treemap(
    df,
    path=['State', 'City'],
    values='City Total Amount Outstanding ( ₹ Crores)',
    title='State-wise and City-wise Borrowing Distribution'
)

# Save to HTML
output_path = os.path.join(os.getcwd(), "treemap_output.html")
fig.write_html(output_path)

# Automatically open in default browser
webbrowser.open(f"file://{output_path}")

print("✅ Treemap generated and opened successfully.")

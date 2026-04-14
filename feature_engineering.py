import pandas as pd
import numpy as np

# Load the dataset
df = pd.read_csv('final_data.csv')

# Feature Engineering

# 1. Risk Categories based on risk_score
def categorize_risk(score):
    if score <= 0.3:
        return 'Low'
    elif score <= 0.7:
        return 'Medium'
    else:
        return 'High'

df['Risk_Category'] = df['risk_score'].apply(categorize_risk)

# 2. Transaction Bins based on Amount
# Using quantiles for bins
df['Amount_Bin'] = pd.qcut(df['Amount'], q=4, labels=['Very Low', 'Low', 'High', 'Very High'])

# 3. Time-based patterns
# Convert Time to hours (assuming Time is in seconds)
df['Hour'] = (df['Time'] // 3600) % 24

# Time of day categories
def time_of_day(hour):
    if 6 <= hour < 12:
        return 'Morning'
    elif 12 <= hour < 18:
        return 'Afternoon'
    elif 18 <= hour < 22:
        return 'Evening'
    else:
        return 'Night'

df['Time_of_Day'] = df['Hour'].apply(time_of_day)

# 4. Amount scaled (log transform for skewed data)
df['Amount_Log'] = np.log1p(df['Amount'])

# Save the enhanced dataset
df.to_csv('enhanced_data.csv', index=False)

print("Feature Engineering Complete. New columns added:")
print("- Risk_Category")
print("- Amount_Bin")
print("- Hour")
print("- Time_of_Day")
print("- Amount_Log")

print("\nRisk Category Distribution:")
print(df['Risk_Category'].value_counts())

print("\nAmount Bin Distribution:")
print(df['Amount_Bin'].value_counts())

print("\nTime of Day Distribution:")
print(df['Time_of_Day'].value_counts())
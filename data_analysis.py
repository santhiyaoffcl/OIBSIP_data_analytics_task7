import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv('final_data.csv')

# Display basic info
print("Dataset Shape:", df.shape)
print("\nColumns:", df.columns.tolist())
print("\nData Types:\n", df.dtypes)
print("\nFirst 5 rows:\n", df.head())
print("\nSummary Statistics:\n", df.describe())

# Check for missing values
print("\nMissing Values:\n", df.isnull().sum())

# Check for duplicates
print("\nDuplicate Rows:", df.duplicated().sum())

# Class distribution
print("\nClass Distribution:\n", df['Class'].value_counts())

# Risk score distribution
print("\nRisk Score Stats:\n", df['risk_score'].describe())

# Prediction distribution
print("\nPrediction Distribution:\n", df['prediction'].value_counts())

# EDA Visualizations
plt.figure(figsize=(15, 10))

# 1. Class Distribution Pie Chart
plt.subplot(2, 3, 1)
df['Class'].value_counts().plot.pie(autopct='%1.1f%%', colors=['blue', 'red'])
plt.title('Fraud vs Normal Transactions')
plt.ylabel('')

# 2. Amount Distribution Histogram
plt.subplot(2, 3, 2)
sns.histplot(data=df, x='Amount', hue='Class', bins=50, alpha=0.7)
plt.title('Amount Distribution by Class')
plt.xlim(0, 1000)  # Limit for better visibility

# 3. Risk Score Distribution
plt.subplot(2, 3, 3)
sns.histplot(data=df, x='risk_score', hue='Class', bins=50, alpha=0.7)
plt.title('Risk Score Distribution by Class')

# 4. Transactions Over Time (Hourly)
df['Hour'] = (df['Time'] // 3600) % 24
plt.subplot(2, 3, 4)
sns.lineplot(data=df.groupby(['Hour', 'Class']).size().reset_index(name='Count'),
             x='Hour', y='Count', hue='Class')
plt.title('Transactions Over Time by Class')

# 5. Box Plot of Amount by Class
plt.subplot(2, 3, 5)
sns.boxplot(data=df, x='Class', y='Amount')
plt.title('Amount Box Plot by Class')
plt.ylim(0, 500)  # Limit for outliers

# 6. Correlation Heatmap (selected features)
plt.subplot(2, 3, 6)
corr_features = ['Amount', 'Time', 'Class', 'risk_score']
sns.heatmap(df[corr_features].corr(), annot=True, cmap='coolwarm')
plt.title('Correlation Heatmap')

plt.tight_layout()
plt.savefig('eda_visualizations.png', dpi=300, bbox_inches='tight')
plt.show()

print("\nEDA visualizations saved as 'eda_visualizations.png'")
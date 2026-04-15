
# Fraud_Detection_Analysis_dashboard

# Fraud Detection & Risk Analytics System - Streamlit Dashboard
file:///C:/Users/S%20santhiya/Videos/Captures/Recording%202026-04-15%20215117.mp4


## Overview
This is a complete, production-level interactive dashboard for fraud detection analytics, built with Python and Streamlit. It replaces Power BI with a web-based, interactive alternative suitable for final-year project demonstrations.

## Features
- **KPI Metrics**: Total transactions, fraud count, fraud percentage, total amount, high-risk transactions
- **Interactive Visualizations**: Pie charts, line charts, bar charts, histograms using Plotly
- **Data Table**: Highlighted high-risk transactions
- **Sidebar Filters**: Risk category, time of day, amount bin, risk score range
- **Automatic Insights**: AI-generated key findings based on filtered data
- **Professional UI**: Clean design with color-coded fraud indicators

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Virtual environment (recommended)

### Step 1: Install Dependencies
```bash
# Activate virtual environment (if using)
& d:\fraud_detection_analysis\.venv\Scripts\Activate.ps1

# Install required packages
pip install -r requirements.txt
```

### Step 2: Run the Dashboard
```bash
streamlit run dashboard.py
```

### Step 3: Access the Dashboard
- Open your web browser
- Navigate to `http://localhost:8501` (default Streamlit port)
- The dashboard will load automatically

## Project Structure
```
fraud_detection_analysis/
├── dashboard.py              # Main Streamlit application
├── enhanced_data.csv        # Processed dataset with features
├── requirements.txt          # Python dependencies
├── data_analysis.py         # EDA script
├── feature_engineering.py   # Feature creation script
├── eda_visualizations.png   # Static plots
└── README.md                # This file
```

## Usage Guide

### Navigation
1. **Sidebar Filters**: Use dropdowns and sliders to filter data dynamically
2. **KPI Cards**: View summary metrics at the top
3. **Visualizations**: Interactive charts update based on filters
4. **Data Table**: Scroll through transaction details (first 100 rows)
5. **Insights**: Read AI-generated insights below the table

### Color Coding
- 🔵 Blue: Normal transactions
- 🔴 Red: Fraudulent transactions
- 🟢 Green: Low risk
- 🟠 Orange: Medium risk
- 🔴 Red: High risk

### Performance Tips
- Dashboard loads data once and caches it for performance
- Filters apply instantly to all visualizations
- For large datasets, consider pagination in the data table

## Technical Details

### Libraries Used
- **Streamlit**: Web app framework
- **Plotly**: Interactive visualizations
- **Pandas**: Data manipulation
- **NumPy**: Numerical operations

### Data Requirements
The dashboard expects `enhanced_data.csv` with these columns:
- Amount, Time, Class, risk_score, prediction
- Risk_Category, Amount_Bin, Hour, Time_of_Day, Amount_Log

### Customization
- Modify `dashboard.py` for additional features
- Update color schemes in the CSS section
- Add new visualizations using Plotly functions

## Troubleshooting

### Common Issues
1. **"Module not found"**: Run `pip install -r requirements.txt`
2. **Port already in use**: Streamlit will suggest an alternative port
3. **Data not loading**: Ensure `enhanced_data.csv` is in the same directory
4. **Plots not rendering**: Check browser compatibility (Chrome recommended)

### Performance
- For datasets >100K rows, consider data sampling
- Use `@st.cache_data` for expensive operations

## Academic Notes
This dashboard demonstrates:
- Data visualization best practices
- Interactive web app development
- Real-time filtering and analytics
- Professional UI/UX design
- Production-ready code structure

Perfect for final-year project presentations and viva examinations.

## Support
For issues or enhancements, check the code comments in `dashboard.py` for detailed explanations.


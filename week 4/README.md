# Superstore Data Analysis

A Jupyter Notebook for exploratory data analysis (EDA) and basic statistical analysis of superstore sales data.

## Overview

This notebook performs a comprehensive analysis of sample superstore data, including data exploration, visualization, and statistical calculations. It helps identify sales patterns across product categories and the relationship between sales and profit metrics.

## Features

- **Data Loading & Inspection**: Reads CSV data and displays basic information about the dataset
- **Data Quality Checks**: Identifies missing values and data types
- **Descriptive Statistics**: Calculates mean sales and trimmed mean values
- **Category Analysis**: Aggregates sales by product category
- **Visualizations**:
  - Bar chart showing total sales by category
  - Histogram of sales distribution
  - Scatter plot showing the relationship between sales and profit
- **Train-Test Split**: Splits data for machine learning preparation (80/20 split)

## Requirements

- Python 3.7+
- pandas
- numpy
- matplotlib
- seaborn
- scikit-learn
- scipy

## Installation

Install required dependencies:

```bash
pip install pandas numpy matplotlib seaborn scikit-learn scipy
```

## Data

The notebook expects a CSV file at `/SampleSuperstore.csv` containing superstore sales data with at least the following columns:

- `Sales`: Sales amount
- `Profit`: Profit amount
- `Category`: Product category

## Usage

1. Ensure `SampleSuperstore.csv` is in the correct location
2. Open the notebook in Jupyter Lab or Jupyter Notebook:
   ```bash
   jupyter notebook superstore.ipynb
   ```
3. Run all cells sequentially to perform the analysis

## Notebook Structure

| Cell | Description |
|------|-------------|
| 0-1 | Import required libraries |
| 2-4 | Load data and display head and info |
| 5 | Check for missing values |
| 6 | Calculate average sales |
| 7 | Aggregate sales by category |
| 8 | Create bar chart of sales by category |
| 9 | Create histogram of sales distribution |
| 10 | Create scatter plot of sales vs profit |
| 11-12 | Train-test split (80/20) and display row counts |
| 13 | Calculate trimmed mean of sales |

## Key Outputs

- **Data Summary**: Dimensions, data types, and missing values
- **Average Sales**: Mean sales across all transactions
- **Sales by Category**: Total sales aggregated by product category
- **Visualizations**: Charts showing sales patterns and relationships
- **Train/Test Sets**: Data split for model development

## Notes

- The random seed (42) in the train-test split ensures reproducible results
- All visualizations use matplotlib and seaborn for consistency
- The analysis uses a 20% test set size, leaving 80% for training

## Future Enhancements

Potential extensions to this analysis:
- More advanced machine learning models for sales prediction
- Time series analysis if dates are available
- Regional or segment-based analysis
- Profit margin calculations and optimization
- Outlier detection and handling

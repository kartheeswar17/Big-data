# Superstore Sales Analysis

A comprehensive data analysis project exploring sales trends, profit patterns, and relationships within a superstore dataset. This notebook performs exploratory data analysis (EDA) with visualizations and statistical insights.

## 📊 Project Overview

This project analyzes the **SampleSuperstore** dataset to uncover key business insights including:
- Sales and profit distributions across categories
- Relationships between sales, profit, and discount rates
- Statistical summaries and data quality checks
- Correlation analysis between numerical variables

## 📁 Dataset

**File:** `SampleSuperstore_data.csv`

**Data Source:** Google Drive (configured for Google Colab)

**Key Columns:**
- `Sales`: Sales revenue
- `Profit`: Profit generated
- `Discount`: Discount rate applied
- `Category`: Product category
- Other transactional attributes

**Data Info:**
- No missing values detected
- Mix of numerical and categorical data
- Ready for analysis and modeling

## 🔧 Setup & Installation

### Prerequisites
- Python 3.x
- Jupyter Notebook or Google Colab
- Required libraries (see below)

### Required Libraries
```bash
pip install pandas numpy matplotlib seaborn scikit-learn scipy
```

Or install all at once:
```bash
pip install -r requirements.txt
```

### For Google Colab Users
The notebook is configured to run on Google Colab with Google Drive integration. Simply mount your Google Drive in the first cell and ensure the dataset path is correct:

```python
from google.colab import drive
drive.mount('/content/drive')
```

## 📖 Usage

1. **Launch the notebook:**
   - Open `superstore.ipynb` in Jupyter Notebook or Google Colab
   
2. **Run cells sequentially:**
   - Import libraries
   - Mount Google Drive (if using Colab)
   - Load the dataset
   - Explore data and generate visualizations

3. **View outputs:**
   - Summary statistics
   - Data quality checks
   - Visualizations and plots

## 📊 Key Analyses

### 1. **Data Exploration**
   - Dataset shape and structure
   - Data types and missing values check
   - Basic statistics (mean, count, etc.)

### 2. **Descriptive Statistics**
   - Average sales calculation
   - Sales aggregation by category
   - Profit and sales mean calculations

### 3. **Visualizations**
   - **Sales by Category:** Bar chart showing total sales per product category
   - **Sales Distribution:** Histogram of sales values
   - **Profit Distribution:** Histogram with KDE and box plot
   - **Sales Distribution:** Histogram with KDE and box plot
   - **Sales vs. Profit:** Scatter plot showing relationship
   - **Discount vs. Profit:** Scatter plot with profit-based hue
   - **Discount Impact:** Bar chart of average profit by discount bins

### 4. **Statistical Analysis**
   - Train-test split (80-20)
   - Trimmed mean calculations
   - Correlation heatmap of numerical features

### 5. **Key Insights**
   - Discount impact on profitability
   - Sales-profit relationship
   - Category-wise sales performance
   - Distribution patterns in sales and profit

## 📈 Data Pipeline

```
Load Data → Explore Structure → Check Quality → 
Basic Stats → Visualizations → Correlations → Insights
```

## 🎯 Key Findings

- **Sales Distribution:** Sales follow a specific distribution pattern across the dataset
- **Profit Variability:** Significant variability in profit across transactions
- **Discount Effect:** Analysis of how discounts impact profit margins
- **Category Performance:** Different categories show varying sales performance
- **Correlations:** Numerical features show relationships worthy of investigation

## 📊 Visualizations Generated

1. Sales by Category (Bar Chart)
2. Sales Distribution (Histogram)
3. Profit vs. Sales (Scatter Plot)
4. Profit Distribution (Histogram + KDE)
5. Profit Box Plot
6. Sales Distribution (Histogram + KDE)
7. Sales Box Plot
8. Discount vs. Profit (Scatter Plot with color gradient)
9. Average Profit by Discount Bin (Bar Chart)
10. Correlation Heatmap (All numerical features)

## 💻 Code Structure

- **Cell 0-2:** Library imports
- **Cell 1:** Google Drive mounting (Colab only)
- **Cell 3:** Data loading from CSV
- **Cells 4-7:** Exploratory data analysis
- **Cells 8-9:** Category-wise sales analysis
- **Cells 10-18:** Distribution analysis and visualization
- **Cell 19:** Discount-profit relationship analysis
- **Cell 20:** Discount binning and profit analysis
- **Cell 21:** Correlation matrix and heatmap

## 🔍 Technologies Used

| Technology | Purpose |
|------------|---------|
| **Pandas** | Data manipulation and analysis |
| **NumPy** | Numerical computations |
| **Matplotlib** | Data visualization |
| **Seaborn** | Statistical visualizations |
| **Scikit-learn** | Machine learning utilities (train-test split) |
| **SciPy** | Statistical functions (trimmed mean) |

## 📝 Notes

- The notebook is optimized for **Google Colab** environment
- Adjust data path if running locally
- All visualizations use standard matplotlib and seaborn styling
- Missing value handling: No missing values in the dataset
- Data types are automatically inferred from CSV

## 🚀 Future Enhancements

Potential extensions to this analysis:
- Predictive modeling for sales or profit forecasting
- Customer segmentation analysis
- Time-series analysis if dates are available
- Regional/geographical analysis if location data exists
- Advanced statistical testing (correlation significance)
- Machine learning classification or regression models

## 📧 Questions & Support

For questions or issues with this analysis:
- Check data paths in the code
- Ensure all libraries are installed
- Verify Google Drive access (if using Colab)
- Review output for anomalies or errors

## 📄 License

This project uses publicly available sample data for educational purposes.

---

**Last Updated:** August 2024  
**Status:** Complete - EDA Phase ✅

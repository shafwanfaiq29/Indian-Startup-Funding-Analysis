# Indian Startup Funding Analysis

## Project Overview

This project analyzes Indian startup funding data from 2015 to early 2020. The objective of this project is to explore funding patterns across time, cities, industries, investment types, investors, and startups that received repeated funding.

The analysis focuses on exploratory data analysis, data cleaning, visualization, and business insight generation using Python.

## Objectives

The main objectives of this project are:

1. Analyze startup funding trends over time.
2. Identify the most dominant cities in the Indian startup ecosystem.
3. Discover which industries received the most funding.
4. Analyze the most frequent and highest-value investment types.
5. Identify the most active investors.
6. Find startups that received repeated funding.
7. Analyze the impact of outliers on total funding.

## Dataset Description

The dataset contains funding information of Indian startups, including:

- Funding date
- Startup name
- Industry vertical
- Sub-vertical
- City location
- Investor name
- Investment type
- Amount in USD

The dataset originally contains 3,044 records.

## Tools and Libraries

The tools and libraries used in this project are:

- Python
- Pandas
- NumPy
- Matplotlib
- Google Colab

## Data Cleaning Process

Several data cleaning steps were performed before analysis:

- Standardized column names.
- Cleaned inconsistent date formats.
- Converted funding amount from text format into numeric format.
- Standardized city names, such as `Bangalore` into `Bengaluru` and `Gurgaon` into `Gurugram`.
- Standardized investment type categories.
- Grouped messy industry labels into broader industry categories.
- Cleaned investor name variations.
- Cleaned startup name variations.
- Detected and analyzed outliers using the IQR method.

## Exploratory Data Analysis

The analysis includes:

- Funding trend by year
- Funding trend by month
- Funding distribution by city
- Funding distribution by industry
- Funding distribution by investment type
- Investor activity analysis
- Repeat-funded startup analysis
- City and industry relationship analysis
- Outlier impact analysis

## Key Findings

Based on the exploratory data analysis, the main findings are:

1. **Bengaluru** is the most dominant startup funding hub, both by number of funding deals and total funding amount.
2. **E-commerce** is the leading industry by both number of funding deals and total funding.
3. **Seed Funding** is the most frequent investment type.
4. **Private Equity** contributes the largest total funding amount.
5. **Sequoia Capital** is the most active investor by frequency.
6. **SoftBank** is associated with the highest total funding value.
7. **Ola** received the highest number of repeated funding rounds.
8. **Flipkart** received the largest total funding among repeat-funded startups.
9. Outliers contribute around **85.12%** of total funding, showing that a small number of large deals heavily influence the overall funding landscape.

## Summary of Main Findings

| Aspect | Result |
|---|---|
| Year with most funding deals | 2016 |
| Year with highest total funding | 2017 |
| Month with most funding deals | June |
| Month with highest total funding | August |
| City with most funding deals | Bengaluru |
| City with highest total funding | Bengaluru |
| Industry with most funding deals | E-commerce |
| Industry with highest total funding | E-commerce |
| Most frequent investment type | Seed Funding |
| Investment type with highest total funding | Private Equity |
| Startup with most repeated funding | Ola |
| Repeat-funded startup with highest total funding | Flipkart |
| Most active investor | Sequoia Capital |
| Investor with highest associated total funding | SoftBank |
| Outlier contribution to total funding | 85.12% |

## Important Notes

There are several limitations in this analysis:

- Around 31.9% of the funding amount values are missing or invalid.
- Some city, industry, investor, and startup names were inconsistent and required standardization.
- Investor funding value represents the total value of deals involving the investor, not the exact individual contribution of each investor.
- Total funding analysis is highly affected by outliers.
- The year 2020 only contains data up to January, so it should not be compared directly with full-year data.

## Conclusion

The Indian startup funding ecosystem in this dataset is highly concentrated around Bengaluru, E-commerce, and large-scale Private Equity deals. While Seed Funding appears most frequently, most of the total funding value comes from larger investment rounds.

The analysis also shows that outliers play a major role in shaping total funding trends. Therefore, funding insights should be interpreted carefully by comparing both frequency-based and amount-based perspectives.

## Project Files

- `Indian_Startup_Funding_EDA.ipynb` — main analysis notebook
- `startup_funding_cleaned.csv` — cleaned dataset
- `summary_metrics.csv` — summary metrics from the analysis
- `main_findings.csv` — key findings table

## Dashboard 

## Author

Muh. Shafwan Faiq R.

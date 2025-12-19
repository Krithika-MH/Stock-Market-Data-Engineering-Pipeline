# FamPay Data Engineering Assessment

## Author
M Krithika

---

## Overview

This repository contains a complete and correct solution to the **FamPay Data Engineering Assessment**.

The objective of this project is to transform two years of daily stock price data into clean monthly summaries and compute commonly used technical indicators for multiple stock symbols. The solution is designed with correctness, readability, and modularity in mind, following good data engineering practices.

The entire pipeline is implemented in Python using the pandas library.

---

## Problem Statement

Given daily stock price data for the last two years for **10 stock tickers**, the task is to:

- Aggregate daily stock data into monthly summaries  
- Compute monthly OHLC values  
- Calculate technical indicators such as Simple Moving Averages and Exponential Moving Averages  
- Store the processed results in separate output files for each ticker  

---

## Solution Approach

The solution performs the following steps in sequence:

1. Load and preprocess the daily stock price data  
2. Resample the data to monthly frequency using **month-end dates**  
3. Compute monthly OHLC values:
   - **Open**: First trading day open price of the month  
   - **High**: Maximum price within the month  
   - **Low**: Minimum price within the month  
   - **Close**: Last trading day close price of the month  
4. Calculate technical indicators based on **monthly closing prices**:
   - SMA 10  
   - SMA 20  
   - EMA 10  
   - EMA 20  
5. Ensure exactly **24 months of data per ticker**  
6. Partition the final dataset by ticker  
7. Write the results to individual CSV files  
8. Validate output structure and row counts  

---

## Project Structure

```text
fampay-assessment/
├── main.py
├── stock_data.csv
├── output/
│   ├── result_AAPL.csv
│   ├── result_AMD.csv
│   ├── result_AMZN.csv
│   ├── result_AVGO.csv
│   ├── result_CSCO.csv
│   ├── result_MSFT.csv
│   ├── result_NFLX.csv
│   ├── result_PEP.csv
│   ├── result_TMUS.csv
│   └── result_TSLA.csv
├── README.md
└── requirements.txt
```
---

## Requirements

- Python 3.8 or higher  
- pandas  

---

## Installation

Install the required dependency using pip:

pip install pandas


Or install from the requirements file:

pip install -r requirements.txt


---

## Dataset

Download the dataset from the following GitHub repository:

https://github.com/sandeep-tt/tt-intern-dataset

Save the file as `stock_data.csv` in the project root directory.


### Tickers Included

AAPL, AMD, AMZN, AVGO, CSCO, MSFT, NFLX, PEP, TMUS, TSLA

---

## Output Data Schema

Each output file contains **monthly aggregated data** with the following columns:


### Column Descriptions

- **date**: Month-end date  
- **open**: First trading day open price of the month  
- **high**: Highest price during the month  
- **low**: Lowest price during the month  
- **close**: Last trading day close price of the month  
- **sma_10**: 10-month simple moving average of closing price  
- **sma_20**: 20-month simple moving average of closing price  
- **ema_10**: 10-month exponential moving average of closing price  
- **ema_20**: 20-month exponential moving average of closing price  

Each ticker output contains **exactly 24 rows**, representing two years of monthly data.

---

## Running the Script

Execute the main processing script using:

python main.py


The script will:

- Load and preprocess the dataset  
- Generate monthly OHLC summaries  
- Compute technical indicators  
- Save results to the `output` directory  
- Print a validation report to the console  

---





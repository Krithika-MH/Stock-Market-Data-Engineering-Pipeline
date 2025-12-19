FamPay Data Engineering Assessment
Overview

This project is a solution to the FamPay Data Engineering assessment. The objective is to transform two years of daily stock price data into monthly summaries and compute common technical indicators for multiple stock symbols.

The solution is implemented using Python and pandas, with a focus on correctness, clarity, and modular design.

Problem Statement

Given daily stock price data for the last two years for 10 stock tickers, the task is to:

Aggregate daily data into monthly summaries

Compute OHLC values for each month

Calculate technical indicators including Simple Moving Averages and Exponential Moving Averages

Store the processed results in separate output files for each ticker

Solution Approach

The solution performs the following steps:

Load and preprocess the daily stock price data

Resample the data to monthly frequency using month end dates

Compute monthly OHLC values

Open: first trading day open price of the month

High: maximum price within the month

Low: minimum price within the month

Close: last trading day close price of the month

Volume: total traded volume for the month

Calculate technical indicators based on monthly closing prices

SMA 10

SMA 20

EMA 10

EMA 20

Partition the final dataset by ticker and write results to CSV files

Validate output structure and row counts

Project Structure
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

Requirements

Python 3.8 or higher

pandas

Installation

Install the required dependencies using pip:

pip install pandas


Or using the requirements file:

pip install -r requirements.txt

Dataset

Download the dataset from the following repository:

https://github.com/sandeep-tt/tt-intern-dataset

Save the file as stock_data.csv in the project root directory.

You can also download it using:

wget -O stock_data.csv https://raw.githubusercontent.com/sandeep-tt/tt-intern-dataset/main/stock_data.csv

Input Data Schema
date,volume,open,high,low,close,adjclose,ticker


Tickers included:

AAPL, AMD, AMZN, AVGO, CSCO, MSFT, NFLX, PEP, TMUS, TSLA

Output Data Schema

Each output file contains monthly aggregated data with the following columns:

date,open,high,low,close,volume,sma_10,sma_20,ema_10,ema_20


Column descriptions:

date: month end date

open: first trading day open price of the month

high: highest price during the month

low: lowest price during the month

close: last trading day close price of the month

volume: total traded volume during the month

sma_10: 10 month simple moving average of close price

sma_20: 20 month simple moving average of close price

ema_10: 10 month exponential moving average of close price

ema_20: 20 month exponential moving average of close price

Each ticker output contains exactly 24 rows representing two years of monthly data.

Running the Script

Execute the main processing script using:

python main.py


The script will:

Load and process the dataset

Generate monthly summaries

Compute technical indicators

Save results to the output directory

Print a validation report to the console
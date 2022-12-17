# Quantitive Momentum Investing
## Description
The purpose of this program is to analyze the historical data of user given tickers and return a ```.xlsx``` with the *top* 50 tickers with the highest momentum. 
Futhermore, the program gives the user an optional prompt to calculate the number of shares to buy for each ticker in order to achieve an equal weight portfolio based on their portfolio amount.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Notes](#notes)

## Usage
The program preforms this functionality in six steps:
  1) Prompt the user for the ```.csv``` containg the tickers to analyze
  2) Utilize the ```yfinance``` library to collect ticker data from Yahoo! Finance, and calculate each tickers price returns from 1 year ago, 6 months ago, 3 months ago, and 1 month ago
  3) Calculate each tickers return percentile for each time period
  4) Calculate each tickers high quality momentumn score based on their percentiles
  5) Select the *top* 50 tickers
  6) Calculate the number of shares to buy for the top 50 tickers

## Installation
In order to install and run this program succesfully, please follow the steps below; *please ensure you have Python3 installed.*

  1) Download the project onto your local computer [with this link](https://github.com/EdisonYCA/quantitive-momentum-investing/archive/refs/heads/main.zip)
  2) Unzip the file into a desired location
  3) Open the file location in your local terminal
  4) Run the following command: ```pip3 install -r requirements.txt```; this will install the project required dependencies
  5) Run the program with the following command: ```python quantitive_momentum_investing.py```
  6) If you would like to use a sample CSV file to test the program, you may enter ```sp_500_stocks.csv``` for the file prompt
  7) Open the output file specified to view results

## Notes
the file ```quantitive_momentum_investing.py``` contains the source code for this project. If you would like to contribute to any changes for program enhancement, feel free to create a pull request.
  



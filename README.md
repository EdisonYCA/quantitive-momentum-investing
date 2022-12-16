# Quantitive Momentum Investing
## Description
The purpose of this program is to analyze the historical data of user given tickers and return a ```.xlsx``` with the *top* 50 tickers with the highest momentum scores. 
Futhermore, the program gives the user an optional prompt to calculate the number of shares to buy for each ticker in order to achieve an equal weight portfolio based on their portfolio amount.
## Functionality
The program generates the momentum scores in 6 steps. 

  1) Prompt the user for the ```.csv``` containg the tickers to analyze
  2) Utilize the ```yfinance``` library to collect ticker data from Yahoo! Finance, and calculate each tickers price returns from 1 year ago, 6 months ago, 3 months ago, and 1 month ago
  3) Calculate each tickers return percentile for each time period
  4) Calculate each tickers high quality momentumn score based on their percentiles
  5) Select the *top* 50 tickers
  6) Calculate the number of shares to buy for the top 50 tickers

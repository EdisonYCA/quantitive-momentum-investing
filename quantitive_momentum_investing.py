# Import dependecies
from datetime import date
from dateutil.relativedelta import relativedelta
import os
import pandas as pd
import yfinance as yf


def main():
    # Get CSV File containing tickers
    tickers = pd.read_csv(get_file())

    # Split tickers into list of 100 and create batch query calls for lower-latency responses
    tickers_split = list(split_list(tickers["Ticker"], 100))
    tickers_split_strings = []  # split tickers from pd object to strings
    for stock in range(0, len(tickers_split)):
        tickers_split_strings.append(' '.join(tickers_split[stock]))

    # Create pandas dataframe
    columns = ["Stock",
               "Stock Price",
               "Number of Shares to Buy",
               "One-Year Price Return",
               "One-Year Return Percentile",
               "Six-Month Price Return",
               "Six-Month Return Percentile",
               "Three-Month Price Return",
               "Three-Month Return Percentile",
               "One-Month Price Return",
               "One-Month Return Percentile",
               "HQM Score"]

    dataframe = pd.DataFrame(columns=columns)

    # Create 1yd, 6m, 3m, and 1m datetime objects
    today = date.today()

    yesterday = today - relativedelta(days=1)
    yesterday = yesterday.strftime("%Y-%m-%d")

    one_year_ago = today - relativedelta(years=1)
    one_year_ago = one_year_ago.strftime("%Y-%m-%d")

    six_months_ago = today - relativedelta(months=6)
    six_months_ago = six_months_ago.strftime("%Y-%m-%d")

    three_months_ago = today - relativedelta(months=3)
    three_months_ago = three_months_ago.strftime("%Y-%m-%d")
    
    one_month_ago = today - relativedelta(months=1)
    one_month_ago = one_month_ago.strftime("%Y-%m-%d")

    dates = [one_year_ago, six_months_ago,
             three_months_ago, one_month_ago]

    # Calculating price returns
    for ticker_str in tickers_split_strings[:1]:
        # Scrape data on batch strings
        data = yf.download(ticker_str, start=one_year_ago,
                           end=today, group_by='ticker')

        # Gather latest price for each time period
        for ticker in ticker_str.split(' '):
            for time_period in dates:
                latestPrice = data[ticker]['Open'][yesterday]
                # Price returns calculations
                if time_period == one_year_ago:
                    # Price Return = (Today Starting Price / Previous Period Ending Price - 1) * 100
                    one_year_price = data[ticker]['Close'][one_year_ago]
                    # one_year_price_return = (latestPrice / one_year_price - 1) * 100
                    print(f"Ticker: {ticker}, One Year Price: {one_year_price}, Yesterdays Price: {latestPrice}")
                elif time_period == six_months_ago:
                    six_month_price = data[ticker]['Close'][six_months_ago]
                    six_month_price_return = (latestPrice / six_month_price - 1) * 100
                    # print(f"Ticker: {ticker}, Six Month Price Return: {six_month_price_return}%")
                elif time_period == three_months_ago:
                    three_month_price = data[ticker]['Close'][three_months_ago]
                    # three_month_price_return = (latestPrice / three_months_ago - 1) * 100
                    print(f"Ticker: {ticker}, Three Month Price: {three_month_price}%")
                else:
                    one_month_price = data[ticker]['Close'][one_month_ago]
                    # one_month_price_return = (latestPrice / one_month_ago - 1) * 100
                    print(f"Ticker: {ticker}, One Month Price: {one_month_price}%")

        # Calculate percentiles
        # Calculate HQM
        # Select Top 50 Stocks
        # Ask user to if they want to include EQUAL WIEGHT Option
        # Format Output


def get_file():
    """Prompt the user for a csv file containing a list of stocks
    and validate the file exists in the current directory"""
    while True:
        file_name = input("Enter the name of your csv file: ")
        if os.path.isfile(file_name):
            print("File opened successfully\n")
            return file_name
        else:
            print(
                "This file does not exist. Please confirm the file is in this directory and try again.")


def split_list(lst, n):
    """Splits a list into sublists of n length"""
    for i in range(0, len(lst), n):
        yield lst[i: i+n]


if __name__ == "__main__":
    main()

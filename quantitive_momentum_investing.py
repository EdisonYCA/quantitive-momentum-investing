from datetime import date
from dateutil.relativedelta import relativedelta
import os
import pandas as pd
import yfinance as yf
from scipy.stats import percentileofscore as percentile
import warnings
warnings.filterwarnings('ignore', category=RuntimeWarning)
from statistics import mean
import xlsxwriter
import math


def main():
    # Get and verify CSV File containing tickers
    tickers = pd.read_csv(get_file())
    verify_csv(tickers)

    # Split tickers into list of 1000 and create batch query call
    tickers_split = list(split_list(tickers["Ticker"], 1000))
    tickers_split_strings = []  # split tickers from panda objects to strings
    for stock in range(0, len(tickers_split)):
        tickers_split_strings.append(' '.join(tickers_split[stock]))

    # Create pandas dataframe
    columns = ["Stock",
               "Stock Price",
               "One-Year Price Return",
               "One-Year Return Percentile",
               "Six-Month Price Return",
               "Six-Month Return Percentile",
               "Three-Month Price Return",
               "Three-Month Return Percentile",
               "One-Month Price Return",
               "One-Month Return Percentile",
               "HQM Score",
               "Number of Shares to Buy"]

    dataframe = pd.DataFrame(columns=columns)

    # Create and format 1yd, 6m, 3m, and 1m datetime objects
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
    for ticker_str in tickers_split_strings:
        # Scrape data using batch calls
        data = yf.download(ticker_str, start=one_year_ago,
                           end=today, group_by='ticker')
        
        # split batch string into single tickers
        for ticker in ticker_str.split(' '):
            for time_period in dates:  # Gather price returns of ticker for each time period
                latest_price = round(data[ticker]['Close'][yesterday], 2)

                # Price Return = (Today Starting Price / Previous Period Ending Price - 1)
                if time_period == one_year_ago:
                    one_year_price = data[ticker]['Close'][one_year_ago]
                    one_year_price_return = round((latest_price / one_year_price - 1), 2)

                elif time_period == six_months_ago:
                    six_month_price = data[ticker]['Close'][six_months_ago]
                    six_month_price_return = round((latest_price / six_month_price - 1), 2)

                elif time_period == three_months_ago:
                    three_month_price = data[ticker]['Close'][three_months_ago]
                    three_month_price_return = round((latest_price / three_month_price - 1), 2)
                    
                else:
                    one_month_price = data[ticker]['Close'][one_month_ago]
                    one_month_price_return = round((latest_price / one_month_price - 1), 2)

            # append each price return to pandas dataframe
            row = pd.DataFrame([  # new row of data
                ticker, 
                latest_price,
                one_year_price_return,
                "N/A",
                six_month_price_return,
                "N/A",
                three_month_price_return,
                "N/A",
                one_month_price_return,
                "N/A",
                "N/A",
                "N/A"
            ], index=columns).T
            dataframe = pd.concat((dataframe, row), ignore_index=True)
        
        # fill any price return value that is NaN
        for return_periods in columns[2:10:2]:
            dataframe.fillna(dataframe[return_periods], inplace=True)

        # Calculate return percentiles
        time_periods = ["One-Year", "Six-Month", "Three-Month", "One-Month"]
        for i in range(0, len(dataframe.index)):  # for every ticker
            for time_period in time_periods:  # calculate return percentile at each time period
                column_to_compare = dataframe[f"{time_period} Price Return"]
                score_to_calculate = dataframe.loc[i, f"{time_period} Price Return"]
                dataframe.loc[i, f"{time_period} Return Percentile"] = percentile(column_to_compare, score_to_calculate) / 100

        # Calculate High Quality Momentumn (HQM) scores
        for i in range(0, len(dataframe.index)):  # for every ticker
            percentiles = []
            for time_period in time_periods:  # calculate return percentile at each time period
                percentiles.append(dataframe.loc[i, f"{time_period} Return Percentile"])
            dataframe.loc[i, "HQM Score"] = mean(percentiles)

        # Select top 50 stocks with respect to HQM score
        dataframe.sort_values('HQM Score', ascending=False, inplace=True)
        dataframe = dataframe[:50]
        dataframe.reset_index(inplace=True, drop=True)

        # Calculate number of shares to buy
        portfolio_amount = get_portfolio_input()
        position_size = portfolio_amount / len(dataframe.index)  # amount user should invest in each stock

        for i in range(0, len(dataframe.index)):
            dataframe.loc[i, 'Number of Shares to Buy'] = math.floor(position_size / dataframe.loc[i, "Stock Price"])   

        # Format output
        format_excel_output(dataframe)


def get_file():
    """Prompt the user for a csv file containing a list of stocks
    and validate the file exists in the current directory"""
    while True:
        file_name = input("Enter the name of your csv file (enter '0' to quit): ")
        if file_name == "0":
            print("Ending program...")
            exit()

        if os.path.isfile(file_name):
            print("File opened successfully\n")
            return file_name

        else:
            print("This file does not exist. Please confirm the file is in this directory \
            and try again.")


def verify_csv(tickers):
    """Verify that the user enters a csv file contain at-least two tickers"""
    if len(list(tickers["Ticker"])) < 2:
        print("CSV file must contain at-least 2 tickers.\nEnding program...")
        exit()
    

def split_list(lst, n):
    """Splits a list into sublists of n length"""
    for i in range(0, len(lst), n):
        yield lst[i: i+n]


def format_excel_output(dataframe):
    """saves and formats dataframe into an Excel file"""
    writer = pd.ExcelWriter('Momentum Strategy.xlsx', engine='xlsxwriter')
    dataframe.to_excel(writer, 'Momentum Strategy', index=False)

    background_color = '#ffffff'
    font_color = '#000000'

    string_format = writer.book.add_format(  # format for strings
        {
            'font_color': font_color,
            'bg_color': background_color,
            'border': 1
        }
    )

    dollar_format = writer.book.add_format(  # format for currency
        {
            'num_format': '$0.00',
            'font_color': font_color,
            'bg_color': background_color,
            'border': 1
        }
    )

    integer_format = writer.book.add_format(  # format for integers
        {
            'num_format': '0',
            'font_color': font_color,
            'bg_color': background_color,
            'border': 1
        }
    )

    percent_format = writer.book.add_format(  # format for percentages
        {
            'num_format': "0.0%",
            'font_color': font_color,
            'bg_color': background_color,
            'border': 1
        }
    )

    columns_formats = {  # format for column names
       'A': ["Stock", string_format],
       'B': ["Stock Price", dollar_format],
       'C': ["One-Year Price Return", percent_format],
       'D': ["One-Year Return Percentile", percent_format],
       'E': ["Six-Month Price Return", percent_format],
       'F': ["Six-Month Return Percentile", percent_format],
       'G': ["Three-Month Price Return", percent_format],
       'H': ["Three-Month Return Percentile", percent_format],
       'I': ["One-Month Price Return", percent_format],
       'J': ["One-Month Return Percentile", percent_format],
       'K': ["HQM Score", percent_format],
       'L': ["Number of Shares to Buy", integer_format]
    }

    for column in columns_formats.keys():
        writer.sheets['Momentum Strategy'].set_column(f'{column}:{column}', 30, columns_formats[column][1])
        writer.sheets['Momentum Strategy'].write(f'{column}1', columns_formats[column][0], columns_formats[column][1])
    writer.close()

    print("Output has been place in: 'Momentum Strategy.xlsx'")


def get_portfolio_input():
    """Get the amount of a users portfolio"""
    while True:
        try:
            portfolio_amount = float(input("Enter the value of your portfolio (enter a '0' to skip this step): "))
            if type(portfolio_amount) == float:
                return portfolio_amount
        except ValueError:
            print("\nPortfolio amount must be a decimal.")


if __name__ == "__main__":
    main()

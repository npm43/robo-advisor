# this is the "app/robo_advisor.py" file

import csv
import json
import os
from dotenv import load_dotenv
from datetime import datetime
import requests

load_dotenv() #> loads contents of the .env file into the script's environment

#utility function to convert float or integer
#help from Professor Rossetti screencast
def to_usd(my_price):
    return"${0:,.2f}".format(my_price)

#
#INFO OUTPUTS
#

api_key = os.environ.get("ALPHAVANTAGE_API_KEY")  #"demo"
symbol = input("Please input the stock symbol you would like to analyze:")  #"MSFT"

#Work with Anthony Redfern to create validation system
if len(symbol)>1:
    pass
if len(symbol)<=5:
    pass
else:
    print("You have not entered a valid symbol. Please try again with a symbol such as AAPL.")
    exit()

symbol_digits = False

for symbols in symbol:
    if symbols.isdigit():
        symbol_digits = True

if symbol_digits == False:
    pass
else:
    print("You have not entered a valid symbol, as you have used a digit. Please try again with a symbol such as AAPL.")
    exit()

request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"

#used modified date code from Shopping Cart Project
current_time = datetime.now()
dt_string = current_time.strftime("%m/%d/%Y %H:%M:%S")

response = requests.get(request_url)

parsed_response = json.loads(response.text)

# help through Anthony Redfern from https://stackoverflow.com/questions/24898797/check-if-key-exists-and-iterate-the-json-array-using-python
try:
    last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]
except:
    print("Sorry, there is no trading data for that stock symbol.")
    exit()

last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

tsd = parsed_response["Time Series (Daily)"]

dates = list(tsd.keys())    #TODO: assumes first day is on top, but consider sorting to ensure that the latest day is first

latest_day = dates[0]   # "2021-03-08"

latest_close = tsd[latest_day]["4. close"] #> 227.3900

#maximum of all the high prices
#high_price = [10, 20, 30, 5]
#recent_high = max(high_prices)

high_prices = []
low_prices = []

for date in dates:
    high_price = tsd[date]["2. high"]
    low_price = tsd[date]["3. low"]
    high_prices.append(float(high_price))
    low_prices.append(float(low_price))

recent_high = max(high_prices)
recent_low = min(low_prices)

#
#INFO OUTPUTS
#
a = float(latest_close)
b = float(recent_low)

if a <= (1.15 * b):
    recommendation = "BUY!"
    recommendation_reason = "You should buy now because the stock's price has plenty of potential to rise."
else:
    recommendation = "DO NOT BUY!"
    recommendation_reason = "You should not buy now because the stock's price has limited potential to rise."

#csv_file_path = "data/prices.csv" # a relative filepath
csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")

csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]

with open(csv_file_path, "w") as csv_file: # "w" means "open the file for writing"
    writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
    writer.writeheader() # uses fieldnames set above
    for date in dates:
        daily_prices = tsd[date]
        writer.writerow({
            "timestamp": date,
            "open": daily_prices["1. open"],
            "high": daily_prices["2. high"],
            "low": daily_prices["3. low"],
            "close": daily_prices["4. close"],
            "volume": daily_prices["5. volume"]
        })



print("-------------------------")
print(f"SELECTED SYMBOL: {symbol}")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print(f"REQUEST AT: {dt_string}")
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE:{to_usd(float(latest_close))}")
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print(f"RECENT LOW: {to_usd(float(recent_low))}")
print("-------------------------")
print(f"RECOMMENDATION: {recommendation}")
print(f"RECOMMENDATION REASON: {recommendation_reason}")
print("-------------------------")
print(f"WRITING DATA TO CSV: {csv_file_path}...")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")
import requests
from twilio.rest import Client
STOCK_NAME = "RIOT"
COMPANY_NAME = "Riot Platforms, Inc."

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
ACCOUNT_SID = "AC7db72bf5922e490f0aa286a83a50b259"
TWILIO_AUTH_TOKEN = "f6340395f2188e6cc7d9f0bfffcf5c14"
stocks_api_key = "W0P3KKL8UZ5TC88H"
news_api_key = "649564e56f0247e8ab6f57af810aa907"
stocks_api_params = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK_NAME,
    "apikey": stocks_api_key,
}

response = requests.get(STOCK_ENDPOINT,params=stocks_api_params)
data = response.json()["Time Series (Daily)"]

#Get yesterday's closing stock price
data_list = [value for (key, value) in data.items()]
data_yesterday_price = data_list[0]["4. close"]

#Get the day before yesterday's closing stock price
data_date_before_price = data_list[1]["4. close"]
#Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp
price_change = (float(data_yesterday_price) - float(data_date_before_price))
up_down=None
if price_change > 0:
    up_down = "🔺"
else:
    up_down = "🔻"
print(price_change)

#Percentage difference in price between closing price yesterday and closing price the day before yesterday.
price_change_percentage = round(abs(price_change)/float(data_date_before_price) * 100,2)

if price_change_percentage > 5:
    # Get news from newsapi
    news_api_params = {
        "apiKey": news_api_key,
        "q": COMPANY_NAME,
    }
    response = requests.get(NEWS_ENDPOINT, params=news_api_params)
    news_articles = response.json()["articles"][:3]
    #Create a formatted list from news api
    formatted_articles = [f"{STOCK_NAME} {up_down}{price_change_percentage}%\nHeadline: {articles['title']}.\n Brief: {articles['description']}" for articles in news_articles]




#Send message via Twilio.
    client = Client(ACCOUNT_SID,TWILIO_AUTH_TOKEN)
    for article in formatted_articles:
            message = client.messages.create(
                body=article,
                from_="+18338785965",
                to="+18582269391",
            )



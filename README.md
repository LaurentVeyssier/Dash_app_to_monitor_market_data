# Dash_app_to_monitor_market_data
Dash app  pulling various financial-related information based on an input ticker code


This app was initially designed by [Eric Kleppen](https://github.com/bendgame) and was fully described in his detailed [medium article](https://medium.com/swlh/how-to-create-a-dashboard-to-dominate-the-stock-market-using-python-and-dash-c35a12108c93).
The original code from the author can be found on github [here](https://github.com/bendgame/MediumFinance).

I had to rewrite the financial report module which was no longer functional, likely due to recent changes in [marketwatch](https://www.marketwatch.com/) layout.
I also introduced a few smaller modifications to manage API credentials and remediate unnecessary errors on dashboard start-up.

I find the app interesting as it provides with a set of examples of app architecture, functionalities and callbacks, displays in Dash. It is a nice source of ideas for future projects.

# What does the App do ?

The app takes a ticker as an input and returns various financial information displayed by an interactive dashboard. Concretly, when a ticker is entered, the dashboard pulls data from Yahoo! Finance and Market Watch to produce information about the company’s financials and price history. Below is the information displayed:
- summary of financial infomation related to the company
- latest KPIs on company share price trading
- company's share price development over various timeframe and graphs
- Twitter Order Flow live feed
- Reddit Wallstreetbets tweet live feed. The group “r/Wallstreetbets” (aka WSB) is a longstanding subreddit channel where over 3.5 million Reddit users discuss highly speculative trading ideas and strategies.

# Requirements
The app requires a twitter and a reddit accounts (both free). The accounts will allow you to obtain credentials to access both services' APIs. Your credentials should be logged into the `config.py` file.
The App also uses:
- Dash and plotly
- yfinance (to collect data from yahoo.finance)
- praw (to connect to the Reddit API)
- sqlite3 (to buffer tweets)

# Output
The app is a little slow and you should allow sufficient time for the dashboard to pop up and then populate once a ticker has been input.
Running the app from the terminal (`python index.py`) will automatically trigger the browser to open and display the dashboard.

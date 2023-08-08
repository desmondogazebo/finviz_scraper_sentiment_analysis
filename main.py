# Import libraries
import pandas as pd
from browser_stuff import init_browser, get_soup
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Parameters
n = 20  # the # of article headlines displayed per ticker
tickers = [str(x) for x in input("Enter stock symbols separated by space: ").split()]

# Get Data
finwiz_url = 'https://finviz.com/quote.ashx?t='
news_tables = {}


for ticker in tickers:
    print(f"Scraping the {n} most recent headlines of {ticker}")
    url = finwiz_url + ticker.upper()
    driver = init_browser()
    html = get_soup(driver, url)
    news_table = html.find(id='news-table')
    news_tables[ticker] = news_table

try:
    for ticker in tickers:
        df = news_tables[ticker]
        df_tr = df.findAll('tr')

        print(f"\nRecent {n} News Headlines for {ticker.upper()}:")

        for i, table_row in enumerate(df_tr):
            a_text = table_row.a.text
            td_text = table_row.td.text
            td_text = td_text.strip()
            print(f"{a_text} ({td_text})")
            if i == n - 1:
                break
except KeyError:
    pass

# Iterate through the news
parsed_news = []
for file_name, news_table in news_tables.items():
    for x in news_table.findAll('tr'):
        text = x.a.get_text()
        date_scrape = x.td.text.split()

        if len(date_scrape) == 1:
            date = None
            time = date_scrape[0]
        else:
            date = date_scrape[0]
            time = date_scrape[1]

        ticker = file_name.split('_')[0]

        parsed_news.append([ticker, date, time, text])

# Sentiment Analysis
analyzer = SentimentIntensityAnalyzer()

columns = ['Ticker', 'Date', 'Time', 'Headline']
news = pd.DataFrame(parsed_news, columns=columns)
scores = news['Headline'].apply(analyzer.polarity_scores).tolist() # parses only the headline of the article.
# Not the actual text. You might get better mileage parsing actual article text.
df_scores = pd.DataFrame(scores)
news = news.join(df_scores, rsuffix='_right')

# View Data
news['Date'] = pd.to_datetime(news.Date).dt.date

unique_ticker = news['Ticker'].unique().tolist()
news_dict = {name: news.loc[news['Ticker'] == name] for name in unique_ticker}

values = []
for ticker in tickers:
    dataframe = news_dict[ticker]
    dataframe = dataframe.set_index('Ticker')
    dataframe = dataframe.drop(columns=['Headline'])
    print('\n')
    print(dataframe.head(n))

    mean = round(dataframe['compound'].mean(), 2)
    values.append(mean)

df = pd.DataFrame(list(zip(tickers, values)), columns=['Ticker', 'Mean Sentiment'])
df = df.set_index('Ticker')
df = df.sort_values('Mean Sentiment', ascending=False)
print(f'\nScale of -1 to 1, with -1 being highly negative and highly 1 being positive.')
print(df)

# do something with the top 3
df = df.head(3)


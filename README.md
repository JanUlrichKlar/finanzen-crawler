# finanzenpy
finanzenpy is based the a Python package Finanzen-Fundamentals that can be used to retrieve fundamentals of stocks, but 
was extended to retrieve historical stock prices. The stock identifier can be ISIN, WKN or the name of the stock itself. 
As the ISIN and WKN are unique it  is recommended to use one of them. 
The data is fetched from [finanzen.net](https://www.finanzen.net), a German language financial news site. Note that the 
api is English but all data will be returned in German.

# Installation
You can easily install finanzen-fundamentals via pip: `pip install finanzen-fundamentals`

If you choose to download the source code, make sure that you have the following dependencies installed:
* requests
* BeautifulSoup
* lxml
You can install all of them by running: `pip install requests BeautifulSoup lxml`.

# Usage
## Import
After you successfully installed the package, you can include it in your projects by importing it.

```import finanzen_fundamentals```

## Retrieve Fundamentals
You can retrieve the fundamentals of a single stock by running: 

```bmw_fundamentals = get_fundamentals("bmw")```

This will fetch the fundamentals of BMW and save it into a dictionary called bmw_fundamentals.
bmw_fundamentals will have the following keys:
* Quotes
* Key Ratios
* Income Statement
* Balance Sheet
* Other

The values for those keys will be variables, holding a year:value dictionary. If no data can be found, the value will be None.
You can also fetch estimates for expected values by using:

```bmw_estimates = stocks.get_estimates("bmw")```

This will save estimates for the most important key metrics if available. The resulting dictionary will hold variable names as keys and a year:value dictionary as values.

Note that we use stock names not stock symbols when fetching data. You can search for stock names by using

```stocks.search_stock("bmw", limit = 3)```

This will print the three most matching stock names for your search. You can increase the limit to 30. If you don't give a parameter, all available data will be printed (up to 30).

## Retrieve historical data
You can retrieve the daily historical data of a single stock by running: 

```stock_historical = stocks.get_historical(stock_identifier, start_date, end_date, exchange) ```

The stock_identifier could be the full name, the specific finanzen.net name or the ISIN of the stock
The start_date and end_date can be specified as a string dd/mm/yyyy or as datetime object.

```bmw_historical = stocks.get_historical("bmw","17/05/2019","21/06/2020", exchange='home') ```

or

```bmw_historical = stocks.get_historical("DE0005190003",datetime.datetime(2019, 5, 17),datetime.datetime(2020, 6, 21), exchange='home') ```

will have the same result.
The result will be a Dataframe containing date, open, close, high, low, volume and the currency which depends an the chosen exchange.
```
         date   open  close   high    low    volume currency
0   2020-06-19  27.20  27.30  27.74  27.10  166679.0      AUD
1   2020-06-18  27.50  27.31  27.94  26.63  290496.0      AUD
2   2020-06-17  24.89  27.02  27.59  24.86  295025.0      AUD
3   2020-06-16  23.85  25.00  25.00  23.80  262276.0      AUD
4   2020-06-15  22.25  23.25  23.88  22.25  193191.0      AUD
..         ...    ...    ...    ...    ...       ...      ...
273 2019-05-23  30.99  32.02  32.22  30.90  273275.0      AUD
274 2019-05-22  30.24  31.19  31.55  30.20  136460.0      AUD
275 2019-05-21  30.03  28.80  30.20  28.60  135705.0      AUD
276 2019-05-20  32.20  29.90  32.20  29.44  195136.0      AUD
277 2019-05-17  30.00  31.46  31.75  30.00  214843.0      AUD
````

If the historic data for a stock are retrieved for the first time the user is asked to specify the favorite exchange by the corresponding index.

```
Security unknown -- Starting search on finanzen.net
0  BAE Baader Bank
1  BDP Budapest
2  BER Berlin
3  BRX BX SWISS
4  BTE Bats
5  CHX BATS Chi-X Europe
6  DUS Düsseldorf
7  FSE Frankfurt
8  GVIE Global Market
9  HAM Hamburg
10  HAN Hannover
11  L&amp;S Lang und Schwarz
12  MUN München
13  MXK Mexiko Exchange
14  NASO NASDAQ OTC
15  XETRA XETRA
16  STU Stuttgart
17  SWX SIX Swiss Exchange
18  TGT Tradegate
19  XQTX Quotrix
Which exchange should be the home-exchange?
```
The full name, the specific finanzen.net name the ISIN and the favorite exchange will be saved in \finanzen_fundamentals\security_info.csv
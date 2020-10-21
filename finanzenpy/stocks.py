#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import datetime
import numpy as np
import pandas as pd
import requests
from lxml import html
from bs4 import BeautifulSoup

# Import Modules
from finanzenpy.scraper import _make_soup
from . import statics


# Define Function to Check for Error
def _check_site(soup):
    message = soup.find("div", {"class": "special_info_box"})
    if message is not None:
        message_text = message.get_text()
        load_error = "Die gewünschte Seite konnte nicht angezeigt werden"
        if load_error in message_text:
            # print('Could not find stock corresponding to ticker {}'.format(stock))
            # print('retry by interpreting {} as some search-text (ISIN, WKN, etc.)'.format(stock.upper()))
            # stock_name = _get_name_by(stock.upper())
            # get_fundamentals(stock_name)
            raise ValueError("Could not find Stock")


# Define Function to identify security by isin or something else
def identify_security(search_text: str):
    # load security list to check wether security was already searched before
    sec_list = pd.read_csv('/security_info.csv', keep_default_na=False)
    mask = np.column_stack([sec_list[col].str.contains(search_text, na=False) for col in sec_list])
    sec_index = sec_list.loc[mask.any(axis=1)]
    if sec_index.empty:
        print('Security unknown -- Starting search on finanzen.net')
        url_search = 'https://www.finanzen.net/suggest/finde/json?'
        payload = {
            'max_results': '1',
            'Keywords_mode': 'APPROX',
            'Keywords': search_text,
            'query': search_text,
            'bias': '100',
            'target_id': '0'}
        r = requests.get(url_search, params=payload)

        soup = BeautifulSoup(r.content, 'lxml')

        page = soup.find('p').getText()
        # Find stock name
        matching_name = [s for s in page.split(',') if "name" in s]
        sec_name = matching_name[0].split(':')[1]
        # Find stock ticker
        matching_ticker = [s for s in page.split(',') if "metadata" in s]
        sec_ticker = matching_ticker[0].split(':')[1].split('|')[0][1:]
        # Find isin
        matching_isin = [s for s in page.split(',') if "identifiers" in s]
        sec_isin = matching_isin[0].split(':')[1].split('|')[1]
        # Find the possible exchanges on finanzen.net
        # First request to get Info about stock (home-exchange, currency, etc.)
        url_base = "https://www.finanzen.net/historische-kurse/" + sec_ticker
        r = requests.get(url_base)
        soup = BeautifulSoup(r.content, 'lxml')
        table = soup.find_all('table')[2]
        options = table.find_all('option')

        exchanges = np.zeros((len(options), 2), dtype=object)
        for index, opt in enumerate(options):
            exchanges[index, 0] = re.search('value="(.*)">', str(opt)).group(1)
            exchanges[index, 1] = re.search('>(.*)<', str(opt)).group(1)
            print('{}  {} {}'.format(index, exchanges[index, 0], exchanges[index, 1]))

        # print(exchanges)
        hexchange_ind = int(input("Which exchange should be the home-exchange?"))
        sec_home_exchange = exchanges[hexchange_ind, 0]
        sec_list = sec_list.append(
            {'name': sec_name, 'ticker': sec_ticker, 'isin': sec_isin, 'exchange': sec_home_exchange},
            ignore_index=True)
        sec_list.to_csv('security_info.csv', index=False)
    else:
        sec_name = sec_index['name'].iloc[0]
        sec_ticker = sec_index['ticker'].iloc[0]
        sec_isin = sec_index['isin'].iloc[0]
        sec_home_exchange = sec_index['exchange'].iloc[0]

    return sec_name, sec_ticker, sec_isin, sec_home_exchange


# Define Function to Extract GuV/Bilanz from finanzen.net
def get_fundamentals(stock: str):
    # Find ticker also if it is a ISIN or WKN
    #stock = _get_name_by(stock)
    name, ticker, isin_nr, home_exchange = identify_security(stock)
    stock = ticker
    # Convert name to lowercase
    stock = stock.lower()
    # Load Data
    soup = _make_soup("https://www.finanzen.net/bilanz_guv/" + stock)
    # Check for Error
    _check_site(soup)

    # Define Function to Parse Table
    def _parse_table(soup, signaler: str):
        table_dict = {}
        table = soup.find("h2", text=re.compile(signaler)).parent
        years = [x.get_text() for x in table.find_all("th")[2:]]
        rows = table.find_all("tr")[1:]
        for row in rows:
            name = row.find("td", {"class": "font-bold"}).get_text()
            row_data = row.find_all("td")
            row_data = row_data[2:]
            row_data = [x.get_text() for x in row_data]
            row_data = [re.sub(r"\.", "", x) for x in row_data]
            row_data = [re.sub(",", ".", x) for x in row_data]
            row_data = [float(x) if x != "-" else None for x in row_data]
            table_dict[name] = dict(zip(years, row_data))
        return table_dict

    # Extract Stock Quote Info+
    try:
        quote_info = _parse_table(soup, "Die Aktie")
    except Exception:
        quote_info = None

    # Extract Key Ratios
    try:
        key_ratios = _parse_table(soup, "Unternehmenskennzahlen")
    except Exception:
        key_ratios = None

    # Extract Income Statement
    try:
        income_info = _parse_table(soup, "GuV")
    except Exception:
        income_info = None

    # Extract Balance Sheet
    try:
        balance_sheet = _parse_table(soup, "Bilanz")
    except Exception:
        balance_sheet = None

    # Extract Other Information
    try:
        other_info = _parse_table(soup, "sonstige Angaben")
    except Exception:
        other_info = None

    # Collect Fundamentals into single Directory
    fundamentals = {
        "Quotes": quote_info,
        "Key Ratios": key_ratios,
        "Income Statement": income_info,
        "Balance Sheet": balance_sheet,
        "Other": other_info
    }

    # Return Fundamentals
    return fundamentals


# Define Function to Extract Estimates
def get_estimates(stock: str):
    # Convert Stock Name to Lowercase
    name, ticker, isin_nr, home_exchange = identify_security(stock)
    stock = ticker
    stock = stock.lower()

    # Load Data
    soup = _make_soup("https://www.finanzen.net/schaetzungen/" + stock)

    # Check for Error
    _check_site(soup)

    # Parse Table containing Yearly Estimates
    table_dict = {}
    table = soup.find("h1", text=re.compile("^Schätzungen")).parent
    years = table.find_all("th")[1:]
    years = [x.get_text() for x in years]
    rows = table.find_all("tr")[1:]
    for row in rows:
        fields = row.find_all("td")
        fields = [x.get_text() for x in fields]
        name = fields[0]
        row_data = fields[1:]
        row_data = [x if x != "-" else None for x in row_data]
        row_data = [re.sub("[^\d,]", "", x) if x is not None else x for x in row_data]
        row_data = [re.sub(",", ".", x) if x is not None else x for x in row_data]
        row_data = [float(x) if x is not None else x for x in row_data]
        table_dict[name] = dict(zip(years, row_data))

    # Return Estimates in Dict
    return table_dict


# Define Function to Search for Stocks
def search_stock(stock: str, limit: int = -1):
    # Convert Stock Name to Lowercase
    stock = stock.lower()

    # Make Request
    soup = _make_soup("https://www.finanzen.net/suchergebnis.asp?_search=" + stock)

    # Check for Error
    if soup.find("div", {"class": "red"}) is not None:
        if "kein Ergebnis geliefert" in soup.find("div", {"class": "red"}).get_text():
            return list()

    # Define Function to Extract Results
    result_list = []
    table = soup.find("table", {"class": "table"})
    rows = table.find_all("tr")
    for row in rows[1:]:
        cells = row.find_all("td")
        name = cells[0].get_text()
        link = cells[0].find("a")["href"]
        link = "https://www.finanzen.net" + link
        result_list.append((name, link))

    # Filter Result if limit was given
    if limit > 0:
        # Decrease limit if bigger than result
        result_len = len(result_list)
        if limit > result_len:
            limit = result_len
        result_list = result_list[0:limit]

    # Return Result List as formatted String
    for result in result_list:
        result_name = result[0]
        result_short = re.search("aktien/(.+)-aktie", result[1]).group(1)
        print("{}: {}".format(result_name, result_short))


### backster82 additional functions

def check_site_availability(url):
    try:
        r = requests.get(url)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)


def get_parser(function, stock_name):
    base_url = "https://www.finanzen.net"

    functions = {
        "search": "/suchergebnis.asp?_search=",
        "stock": "/aktien/",
        "estimates": "/schaetzungen/",
        "fundamentals": "/bilanz_guv/",
        "index": "/index/"
    }

    if function not in functions:
        raise ValueError("Got unknown function %r in get_parser" % function)
        return 1

    check_site_availability(base_url)

    url = base_url + functions[function] + stock_name
    response = requests.get(url, verify=True)

    parser = html.fromstring(response.text)

    return parser


def get_estimates_lxml(stock: str, results=[]):
    url = "https://www.finanzen.net/schaetzungen/" + stock

    xp_base_xpath = '//div[contains(@class, "box table-quotes")]//h1[contains(text(), "Schätzungen")]//..'
    xp_data = xp_base_xpath + '//table//tr'

    response = requests.get(url, verify=True)
    parser = html.fromstring(response.text)

    data_table = []

    header_row = 0

    for data_element in parser.xpath(xp_data):
        table_row = []
        for i in data_element:
            table_row.append(i.xpath('./text()')[0])

        if header_row != 0:
            for i in range(1, len(table_row)):
                if not table_row[i] == '-':
                    table_row[i] = table_row[i].replace(".", "").replace(",", ".")
                    table_row[i] = float(table_row[i].split(" ")[0])

        else:
            table_row[0] = "Estimation"
            header_row = 1

        data_table.append(table_row)
        dataframe = pd.DataFrame(list(map(np.ravel, data_table)))
        dataframe.columns = dataframe.iloc[0]
        dataframe.drop(dataframe.index[0], inplace=True)

    return dataframe


def get_fundamentals_lxml(stock: str, results=[]):
    url = "https://www.finanzen.net/bilanz_guv/" + stock

    tables = ["Die Aktie",
              "Unternehmenskennzahlen",
              "GuV",
              "Bilanz",
              "sonstige Angaben"
              ]

    complete_data_set = []

    for table in tables:
        parser = get_parser("fundamentals", stock)

        xp_base = '//div[contains(@class, "box table-quotes")]//h2[contains(text(), "' + table + '")]//..'
        xp_head = xp_base + '//table//thead//tr'
        xp_data = xp_base + '//table//tbody'

        parsed_data_table = parser.xpath(xp_base)

        # drop second empty element in parsed_data_table
        # ToDo: find out why parser.xpath(xp_base) returns 2 elements
        # parsed_data_table.pop()

        for data_element in parsed_data_table:
            header_array = []
            table_data = []
            for i in data_element.xpath('.//table//thead//tr//th/text()'):
                header_array.append(i)

            table_data.append(header_array)

            # first table element is an checkbox so we'll drop it
            first_col = True
            for i in data_element.xpath('.//table//tr'):
                if not first_col:
                    data = i.xpath('.//td/text()')
                    for cnt in range(1, len(data)):
                        data[cnt] = data[cnt].replace(".", "").replace(",", ".")
                    table_data.append(data)
                else:
                    first_col = False

            dataframe = pd.DataFrame(list(map(np.ravel, table_data)))
            dataframe.columns = dataframe.iloc[0]
            dataframe.drop(dataframe.index[0], inplace=True)

            complete_data_set.append(dataframe)

    return pd.concat(complete_data_set, ignore_index=True)


def get_current_value_lxml(stock: str, exchange="TGT", results=[]):
    data_columns = [
        "name",
        "wkn",
        "isin",
        "symbol",
        "price",
        "currency",
        "chg_to_open",
        "chg_percent",
        "time",
        "exchange"
    ]

    url = "https://www.finanzen.net/aktien/" + stock + "-aktie" + statics.StockMarkets[exchange][
        'url_postfix']
    response = requests.get(url, verify=True)

    # sleep()
    parser = html.fromstring(response.text)
    summary_table = parser.xpath('//div[contains(@class,"row quotebox")][1]')

    i = 0

    summary_data = []

    for table_data in summary_table:
        raw_price = table_data.xpath(
            '//div[contains(@class,"row quotebox")][1]/div[contains(@class, "col-xs-5")]/text()')
        raw_currency = table_data.xpath(
            '//div[contains(@class,"row quotebox")][1]/div[contains(@class, "col-xs-5")]/span//text()')
        raw_change = table_data.xpath(
            '//div[contains(@class,"row quotebox")][1]/div[contains(@class, "col-xs-4")]/text()')
        raw_percentage = table_data.xpath(
            '//div[contains(@class,"row quotebox")][1]/div[contains(@class, "col-xs-3")]/text()')
        raw_name = table_data.xpath('//div[contains(@class, "col-sm-5")]//h1/text()')
        raw_instrument_id = table_data.xpath('//span[contains(@class, "instrument-id")]/text()')
        raw_time = table_data.xpath('//div[contains(@class,"row quotebox")]/div[4]/div[1]/text()')
        raw_exchange = table_data.xpath('//div[contains(@class,"row quotebox")]/div[4]/div[2]/text()')

        name = ''.join(raw_name).strip()
        time = ''.join(raw_time).strip()
        exchange = ''.join(raw_exchange).strip()

        instrument_id = ''.join(raw_instrument_id).strip()
        (wkn, isin) = instrument_id.split(sep='/')
        if 'Symbol' in isin:
            (isin, sym) = isin.split(sep='Symbol')
        else:
            sym = ""

        currency = ''.join(raw_currency).strip()

        summary_data = [
            name.replace('&nbsp', ''),
            wkn.replace(' ', '').replace("WKN:", ""),
            isin.replace(' ', '').replace("ISIN:", ""),
            sym.replace(' ', '').replace(":", ""),
            float(raw_price[0].replace(',', '.')),
            currency,
            float(raw_change[0].replace(',', '.')),
            float(raw_percentage[0].replace(',', '.')),
            time,
            statics.StockMarkets[exchange]['real_name']
        ]

    return pd.DataFrame(data=[summary_data], columns=data_columns)


def search_stock_lxml(stock: str, limit: int = -1, results=[]):
    indices = ["name", "fn_stock_name", "isin", "wkn"]
    df = pd.DataFrame(columns=indices)

    parser = get_parser("search", stock)

    table_xpath = '//div[contains(@class, "table")]//tr'
    summary_table = parser.xpath(table_xpath)

    if len(summary_table) == 0:
        raise ValueError("Site did find any entries for %r" % stock)

    skip_first_element = 0
    results = []

    for table_element in summary_table:
        # Todo: Find cause for the first element being [] []
        if skip_first_element == 0:
            skip_first_element = 1
        else:
            raw_name = ''.join(table_element.xpath('.//a/text()')).strip()
            raw_link = ''.join(table_element.xpath('.//a//@href')).strip()
            raw_isin = ''.join(table_element.xpath('.//td')[1].xpath('./text()')).strip()
            raw_wkn = ''.join(table_element.xpath('.//td')[2].xpath('./text()')).strip()

            fn_stock_name = raw_link.replace("/aktien/", "").replace("-aktie", "")

            if limit == 0:
                break
            elif limit > 0:
                limit = limit - 1
                df = df.append(pd.DataFrame(data=[[raw_name, fn_stock_name, raw_isin, raw_wkn]], columns=indices))
            else:
                df = df.append(pd.DataFrame(data=[[raw_name, fn_stock_name, raw_isin, raw_wkn]], columns=indices))

    return df


def get_historic(stock: str, start_date, end_date, exchange='home'):
    # load security list to check whether security was already searched before

    name, ticker, isin_nr, home_exchange = identify_security(stock)
    # set exchange to home which is in the csv from an earlier search or was identified right now
    if exchange == 'home':
        exchange = home_exchange

    # Request to get historical stock data
    url_base = "https://www.finanzen.net/historische-kurse/" + ticker
    # get date from input (accept datetime and string input)

    if isinstance(start_date, str):
        start_date = datetime.datetime.strptime(start_date, '%d/%m/%Y')
    intag1, inmonat1, injahr1 = start_date.day, start_date.month, start_date.year
    if isinstance(end_date, str):
        end_date = datetime.datetime.strptime(end_date, '%d/%m/%Y')
    intag2, inmonat2, injahr2 = end_date.day, end_date.month, end_date.year

    form_data = {'inTag1': intag1, 'inMonat1': inmonat1, 'inJahr1': injahr1,
                 'inTag2': intag2, 'inMonat2': inmonat2, 'inJahr2': injahr2,
                 'strBoerse': exchange}
    r = requests.post(url_base, data=form_data)
    soup = BeautifulSoup(r.content, 'lxml')
    # identify currency which depends on chosen exchange
    currency = soup.find('div', class_="col-xs-5 col-sm-4 text-sm-right text-nowrap").find('span').text
    # extract historic data from table |
    table = soup.find_all('table')[3]
    output_rows = []
    for table_row in table.findAll('tr'):
        columns = table_row.findAll('td')
        output_row = []
        for column in columns:
            output_row.append(column.text)
        output_rows.append(output_row)
    output_rows = [x for x in output_rows if x != []]

    historic_data = pd.DataFrame(np.array(output_rows),
                                 columns=['date', 'open', 'close', 'high', 'low', 'volume'])

    historic_data['date'] = pd.to_datetime(historic_data['date'], format='%d.%m.%Y')
    # as in german comma separates decimal places the data must be corrected
    # also sometimes no value exists so it is set to 0
    for price in ['open', 'close', 'high', 'low']:
        historic_data[price] = historic_data[price].str.replace('-', '0')
        historic_data[price] = historic_data[price].str.replace(',', '.').astype(float)
    historic_data['volume'] = historic_data['volume'].str.replace('-', '0')
    historic_data['volume'] = historic_data['volume'].str.replace('.', '').astype(float)
    # add column with currency for specific exchange
    historic_data['currency'] = currency

    return historic_data

# global list of Stockmarkets on finanzen.net their url components and real names
StockMarkets = {
    "BER": {"url_postfix": "@stBoerse_BER", "real_name": "Berlin"},
    "DUS": {"url_postfix": "@stBoerse_DUS", "real_name": "Düsseldorf"},
    "FSE": {"url_postfix": "@stBoerse_FSE", "real_name": "Frankfurt Stock Exchange"},
    "HAM": {"url_postfix": "stBoerse_HAM", "real_name": "Hamburg"},
    "HAN": {"url_postfix": "@stBoerse_HAN", "real_name": "Hannover"},
    "MUN": {"url_postfix": "@stBoerse_MUN", "real_name": "München"},
    "XETRA": {"url_postfix": "@stBoerse_XETRA", "real_name": "XETRA"},
    "STU": {"url_postfix": "@stBoerse_STU", "real_name": "Stuttgard"},
    "TGT": {"url_postfix": "@stBoerse_TGT", "real_name": "Tradegate"},
    "BAE": {"url_postfix": "@stBoerse_BAE", "real_name": "Baader Bank"},
    "BDP": {"url_postfix": "@stBoerse_BDP", "real_name": "Budapest"},
    "BRX": {"url_postfix": "@stBoerse_BRX", "real_name": "BX SWISS"},
    "BTE": {"url_postfix": "@stBoerse_BTE", "real_name": "Bats"},
    "BTT": {"url_postfix": "@stBoerse_BTT", "real_name": ""},
    "CLB": {"url_postfix": "@stBoerse_CLB", "real_name": ""},
    "GVIE": {"url_postfix": "@stBoerse_GVIE", "real_name": "Global Market"},
    "NAS": {"url_postfix": "@stBoerse_NAS", "real_name": "NASDAQ OTC"},
    "MXK": {"url_postfix": "@stBoerse_MXK", "real_name": ""},
    "SIX": {"url_postfix": "@stBoerse_SWX", "real_name": "SIX Swiss Exchange"},
    "XQTX": {"url_postfix": "@stBoerse_XQTX", "real_name": "Quotrix"},
    "AMEX": {"url_postfix": "@stBoerse_AMEX", "real_name": ""},
    "NYSE": {"url_postfix": "@stBoerse_NYSE", "real_name": "New York Stock Exchange"},
}

# global list of indices
# could add much more indices here
Indices = {
    # Germany
    "DAX": {"index_name": "dax", "country": "germany"},
    "QIX Deutschland": {"index_name": "qix-deutschland", "country": "germany"},
    "TecDAX": {"index_name": "tecdax", "country": "germany"},
    "MDAX": {"index_name": "mdax", "country": "germany"},
    "SDAX": {"index_name": "sdax", "country": "germany"},
    "VDAX-NEW": {"index_name": "vdax_new", "country": "germany"},
    # USA
    "Dow Jones": {"index_name": "dow_jones", "country": "usa"},
    "NASDAQ Comp.": {"index_name": "nasdaq_composite", "country": "usa"},
    "S&P 500": {"index_name": "s&p_500", "country": "usa"},
    "NASDAQ 100": {"index_name": "nasdaq_100", "country": "usa"},
    "S&P 600 Small Caps": {"index_name": "s&p_600_small_cap", "country": "usa"},
    # western europe
    "FTSE 100": {"index_name": "ftse_100", "country": "great britain"},
    "CAC 40": {"index_name": "cac_40", "country": "france"},
    "IBEX 35": {"index_name": "ibex_35", "country": "spain"},
    "ATX": {"index_name": "atx", "country": "austria"},
    "OMXS PI": {"index_name": "omxs_pi", "country": "sweden"},
    # eastern europe
    "PX": {"index_name": "px", "country": "czech republic"},
    "ATHEX 20": {"index_name": "athex_20", "country": "greek"},
    "SAX": {"index_name": "sax", "country": "slovakia"},
    "BUX": {"index_name": "bux", "country": "hungary"},
    "WIG 20": {"index_name": "wig_20", "country": "poland"},
    # middle east / africa
    "NSE 20": {"index_name": "nse_20", "country": "kenia"},
    "TA-100": {"index_name": "ta-100", "country": "israel"},
    "EGX30": {"index_name": "egx30", "country": "egypt"},
    "GSE": {"index_name": "gse", "country": "ghana"},
    "KSE 100": {"index_name": "kse_100", "country": "pakistan"},
    # continental america
    "S&P/TSX": {"index_name": "s&p_tsx_composite_index", "country": "canada"},
    "IPC": {"index_name": "ipc", "country": "mexico"},
    "S&P/TSX Venture": {"index_name": "s&p_tsx_venture_composite_index", "country": "canada"},
    "BSX": {"index_name": "bsx", "country": "bermuda"},
    "BOVESPA": {"index_name": "bovespa", "country": "brazil"},
    # asia america
    "NIKKEI 225": {"index_name": "nikkei_225", "country": "japan"},
    "Hang Seng": {"index_name": "hang_seng", "country": "hongkong"},
    "Australia All Ordinaries": {"index_name": "asx", "country": "australia"},
    "RTX": {"index_name": "rtx", "country": "russia"},
    "TOPIX 500": {"index_name": "topix-500", "country": "japan"},
}

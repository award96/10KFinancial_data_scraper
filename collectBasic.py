import pandas as pd
import finnAPI
from utilities import safe_index

"""
    Using the finnhub API collect introductory information on 
    all available companies.

    exchange_to_collect: refer to https://finnhub.io/docs/api#stock-symbols
                            a good default is 'US'
"""

def collect(symbolPath, basicPath, exchange_to_collect):
    find_symbols(symbolPath, exchange_to_collect)
    add_profile_data(symbolPath, basicPath)

def find_symbols(outputPath, exchange_to_collect):
    resp = finnAPI.get_symbol_json(exchange=exchange_to_collect)
    rows = []
    colNames = ['symbol', 'name', 'type']
    for i in range(len(resp)):
        this_company = resp[i]
        this_symb = safe_index(this_company, 'displaySymbol', None, printObject=True)
        this_name = safe_index(this_company, 'description', None, printObject=True)
        this_type = safe_index(this_company, 'type', None, printObject=True)
        rows.append([this_symb, this_name, this_type])
    df = pd.DataFrame(rows, columns=colNames)
    df.to_csv(outputPath)

def add_profile_data(inputPath, outputPath, save_point = 100):
    df = pd.read_csv(inputPath, index_col=0)
    industry_arr = []
    marketC_arr = []
    shares_arr = []
    exchange_arr = []
    for index, row in df.iterrows():
        if index >= save_point:
            if index % save_point == 0:
                print("saving partially finished collection to csv")
                dfCopy = df.copy(deep=True)
                record_data(dfCopy, industry_arr, marketC_arr, shares_arr, exchange_arr, outputPath)

        symbol = row['symbol']
        print(f"\nsymbol={symbol}")
        profileJson = finnAPI.get_profile_json(symbol)
        industry, marketCap, shares, exchange = parse_profile(profileJson)
        industry_arr.append(industry)
        marketC_arr.append(marketCap)
        shares_arr.append(shares)
        exchange_arr.append(exchange)
    record_data(df, industry_arr, marketC_arr, shares_arr, exchange_arr, outputPath, incomplete=False)

def parse_profile(profileJson):
    industry = safe_index(profileJson, 'finnhubIndustry', 'NA', True)
    marketCap = safe_index(profileJson, 'marketCapitalization', 'NA', True)
    shareOutstanding = safe_index(profileJson, 'shareOutstanding', 'NA',True)
    exchange = safe_index(profileJson, 'exchange', 'NA',True)

    return [industry, marketCap, shareOutstanding, exchange]

def record_data(df, industry_arr, marketC_arr, shares_arr, exchange_arr, outputPath, incomplete=True):
    if incomplete:
        df = df.loc[0:(len(industry_arr) - 1)]
    loc1 = len(df.columns)
    loc2 = loc1 + 1
    loc3 = loc2 + 1
    loc4 = loc3 + 1
    try:
        df.insert(loc=loc1, column="industry", value=industry_arr)
        df.insert(loc=loc2, column="marketCap2020", value=marketC_arr)
        df.insert(loc=loc3, column="sharesOutstanding", value=shares_arr)
        df.insert(loc=loc4, column="exchange", value=exchange_arr)
    except Exception:
        print("\n\n#############\nException")
        return
    df.to_csv(outputPath)




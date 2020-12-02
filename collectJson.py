import json
import pandas as pd
import finnAPI
from utilities import name_json_file

"""
    Using the finnhub API, collect the JSON data for companies
    that are in the csv output by collectBasic.py, and are in one of 
    the industries from industryList

    Use explorer.py to understand the JSON response data better, 
    or use a JSON visualizer.
"""
def collect(inputPath, industryList):
    df = pd.read_csv(inputPath, index_col=0)
    for industry in industryList:
        this_df = df[df['industry'] == industry]
        print(f"\n\n{this_df.shape[0]} companies found for industry: {industry}\n")
        for index, row in this_df.iterrows():
            symb = row['symbol']
            print(f"symbol = {symb}")
            jsonResp = finnAPI.get_tenK_json(symb)
            with open(name_json_file(symb), 'w') as file:
                json.dump(jsonResp, file)


# collect('basic.csv', ['Pharmaceuticals', 'Health Care', 'Life Sciences Tools & Services'])
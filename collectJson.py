import finnAPI
from utilities import name_json_file
import json
import pandas as pd

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
from utilities import name_json_file, name_horiz_col, generate_years_list, safe_index, list_to_dict

import pandas as pd
import numpy as np
import json

"""
    For use by a HorizontalProfile object. Turn json data downloaded
    by collectJson and the 'basic' data downloaded by collectBasic into
    a full horizontal profile of many companies of the same industry
"""

def generate(inputPath, industry, conceptList, year, baseYear):
    conceptDict = list_to_dict(conceptList)
    df = pd.read_csv(inputPath, index_col=0)
    if industry:
        df = df[df['industry'] == industry]
    df = add_empty_cols(df, conceptList, year, baseYear)
    for index, row in df.iterrows():
        symb = row['symbol']
        jsonPath = name_json_file(symb)
        with open(name_json_file(symb), 'r') as jsonFile:
            companyJson = json.load(jsonFile)
        tenKList = companyJson['data']
        for tenK in tenKList:
            thisYear = tenK['year']
            if thisYear > year or thisYear < baseYear:
                continue
            report = safe_index(tenK, 'report', {}, printObject=True)
            bs = safe_index(report, 'bs', [], printObject=True)
            cf = safe_index(report, 'cf', [], printObject=True)
            ic = safe_index(report, 'ic', [], printObject=True)
            for subReport in [bs, cf, ic]:
                add_data(df, subReport, conceptDict, thisYear, index)
    df.info()
    print(df.head(30))
    return df


def add_data(df, subReport, conceptDict, thisYear, index):
    if type(subReport) == list:
        for item in subReport:
            thisConcept = safe_index(item, 'concept', 'Null', printObject=True)
            add_data_subroutine(df, item, thisConcept, thisYear, conceptDict, 'value', index)
    elif type(subReport) == dict:
        for thisConcept in subReport:
            add_data_subroutine(df, subReport, thisConcept, thisYear, conceptDict, thisConcept, index)

def add_data_subroutine(df, item, thisConcept, thisYear, conceptDict, key, index):
    if thisConcept in conceptDict:
        thisCol = name_horiz_col(thisConcept, thisYear)
        thisVal = safe_index(item, key, 'Null')
        if (type(thisVal) != int):
            thisVal = np.nan
        df.at[index, thisCol] = thisVal


def add_empty_cols(df, conceptList, year, baseYear):
    yearList = generate_years_list(year, baseYear)
    length_df = df.shape[0]
    for year in yearList:
        colNames = [name_horiz_col(concept, year) for concept in conceptList]
        for i in range(len(colNames)):
            newCol = [np.nan] * length_df
            df.insert(loc=len(df.columns), column=colNames[i], value=newCol)
    return df

# df = generate('basic.csv', 'Biotechnology', ['NetIncomeLoss', 'ResearchAndDevelopmentExpense'], 2019, 2018)
# df.to_csv('filled.csv', index=False)
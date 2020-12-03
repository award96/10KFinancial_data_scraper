import pandas as pd
import numpy as np
import json

from utilities import (name_json_file, 
                        name_horiz_col, 
                        generate_years_list, 
                        safe_index, 
                        list_to_dict,
                        add_empty_cols)

"""
    For use by a HorizontalProfile object. Add JSON data downloaded
    by collectJson.py into the 'basic' csv data downloaded by 
    collectBasic.py into a full horizontal profile of 
    many companies of the same industry

    To use this module, create a HorizontalProfile object and the 
    'generate' function will be called upon instantiation.

    It's normal to have a lot of keyErrors, the data on FinnHub is
    not very consistent.
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

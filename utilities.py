import traceback
import numpy as np
"""
    Functions that have a more general use across the package
"""

def safe_index(dict_obj, key, returnOnError, printObject=False):
    """
        Index into a dict, and if the key is not found, handle the error

            The JSON responses from FinnHub API do not have the same keys
            every time. A missing key indicates that the given data 
            is not recorded in the FinnHub Database.
        ARGS
            dict_obj - dict
            key - str
            returnOnError - any type - what is to be returned if an error is raised
            printObject - bool - whether to print the dict_obj on error
        RETURNS
            dict_obj[key] - the value associated with the key for the dictionary 
                            OR, if an error is encountered, returns returnOnError

    """
    try:
        return dict_obj[key]
    except Exception:
        print("function utilities.safe_index() caught error")
        traceback.print_exc()
        print(f"\nreturning {returnOnError}\n")
        if printObject:
            print(f"dict_obj:  {dict_obj}\nkey: {key}\n")
        return returnOnError


def add_empty_cols(df, conceptList, year, baseYear):
    yearList = generate_years_list(year, baseYear)
    length_df = df.shape[0]
    for year in yearList:
        colNames = [name_horiz_col(concept, year) for concept in conceptList]
        for i in range(len(colNames)):
            newCol = [np.nan] * length_df
            df.insert(loc=len(df.columns), column=colNames[i], value=newCol)
    return df

def generate_all_year_pairs(yearRange):
    allPairs = []
    high, low = yearRange[0], yearRange[1]
    while high > low:
        while low < high:
            allPairs.append((high, low))
            low += 1
        low = yearRange[1]
        high -= 1
    return allPairs

def generate_years_list(year, baseYear):
    """
    ARGS:
        year (int) - usually the current year
        baseYear (int) - the start year (must be less than year)
    RETURNS:
        a list of ints. Descends from year to baseYear. Includes baseYear
        if the input is (2019, 2017) the list will be:
        [2019, 2018, 2017]
    """
    if (baseYear > year):
        raise ValueError(
            "baseYear must be less than year.\nThis error was raised by 'generate_years_list'")
    output = []
    while year >= baseYear:
        output.append(year)
        year -= 1
    return output

def split_year(period):
    if not period:
        return None
    elif type(period) == str and len(period) > 4:
        return period.split('-')[0]
    else:
        raise ValueError(f"Period is not of type string and format 'YYYY-MM-DD'\ntype(period) was {type(period)}\nprint(period): {print(period)}")
def split_year_from_col(colName):
    return (colName[:4], colName[4:])

def name_json_file(symbol):
    return 'json_data/' + symbol + '.json'

def name_horiz_col(concept, year):
    if (type(concept) != str):
        concept = str(concept)
    return str(year) + concept

def name_stock_col(year):
    return str(year) + 'stockPrice'

def list_to_dict(list_):
    d = {}
    for item in list_:
        d[item] = True
    return d


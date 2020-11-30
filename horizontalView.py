import pandas as pd
import numpy as np

import readWrite
from utilities import clean_duplicates


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


def generate_empty_df(symbol_list, df, colNames, baseLength):
    empty_rows = []

    for symb in symbol_list:
        newRow = []
        newRow.append(symb)
        df_this_symb = df[df['symbol'] == symb]
        industry = df_this_symb.iloc[0]['industry']
        marketCap = df_this_symb.iloc[0]['marketCap']
        newRow.extend([industry, marketCap])
        empty_vals = [np.nan] * (len(colNames) - baseLength)
        newRow.extend(empty_vals)

        empty_rows.append(newRow)
    empty_df = pd.DataFrame(empty_rows, columns=colNames)
    return empty_df


def naming_convention(year):
    return (str(year) + 'val')


def name_columns(yearsList, base=['symbol', 'industry', 'marketCap']):
    colNames = base
    baseLength = len(colNames)
    for i in range(len(yearsList)):
        year = yearsList[i]
        # columns : [base, 2019val, 2018val, ...]
        colNames.append(naming_convention(year))
    return (colNames, baseLength)


def fill_horizontal_df(horizontal_df, df, yearsList, key):
    for i in range(horizontal_df.shape[0]):  # fill in empty horizontal df
        df_this_symb = df[df['symbol'] == horizontal_df.iloc[i]['symbol']]

        for year in yearsList:  # iterate through each year
            lastYear = year - 1
            df_this_year = df_this_symb[df['year'] == year]
            if (df_this_year.shape[0] > 1):
                #print(f"\nThe dataframe has multiple rows for the year {year}. This script assumes 1 row, the 2nd will not be counted. Here is the dataframe\n{df_this_year}\n")
                pass
            valueThisYear = np.nan
            valid_index = df_this_year.first_valid_index()
            if valid_index:
                valueThisYear = df_this_year.iloc[0][key]

            horizontal_df.at[i, naming_convention(year)] = valueThisYear


def generate_horizontal_df(
    filepath,
    year,
    baseYear,
    key="netIncome",
    baseCols=[
        'symbol',
        'industry',
        'marketCap']):
    df = pd.read_csv(filepath, index_col=0)
    yearsList = generate_years_list(year, baseYear)
    colNames, baseLength = name_columns(yearsList, base=baseCols)
    df.sort_values(by=['symbol', 'year'])
    symbol_list_duplicates = df['symbol'].tolist()
    symbol_list = clean_duplicates(symbol_list_duplicates)
    horizontal_df = generate_empty_df(symbol_list, df, colNames, baseLength)
    fill_horizontal_df(horizontal_df, df, yearsList, key)
    return horizontal_df

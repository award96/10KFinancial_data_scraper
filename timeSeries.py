import pandas as pd
from utilities import split_year_from_col

def rename_columns(df):
    newColNames = ['year', 'symbol']
    uniqueYears = {}
    numbers = [str(i) for i in range(10)]
    for colName in df.columns:
        if colName[0] in numbers:
            year, colName = split_year_from_col(colName)
            if year not in uniqueYears:
                uniqueYears[year] = True
            if colName not in newColNames:
                newColNames.append(colName)
    return newColNames, uniqueYears

def convert(df):
    newColNames, uniqueYears = rename_columns(df)
    totalCompanies = df.shape[0]
    totalYears = len(uniqueYears)
    totalNewRows = totalCompanies * totalYears
    newDF = create_empty_df(newColNames, totalNewRows)
    oldColNames = list(df.columns)
    numbers = [str(i) for i in range(10)]
    yearList = list(uniqueYears.keys())
    yearList.sort()
    for index, row in df.iterrows():
        symbol= row['symbol']
        for oldCol in oldColNames:
            if oldCol[0] in numbers:
                value = row[oldCol]
                year, newCol = split_year_from_col(oldCol)
                new_index = choose_new_index(index, year, yearList)
                # print(f"\n\nsymbol = {symbol}, year = {year}\noldCol = {oldCol}")
                # print(f"base = {index * len(yearList)}, top = {yearList.index(year)}")
                # print(f"new_index = {new_index}")
                # print(f"this is the current series at {new_index}\n{newDF.iloc[new_index]}")
                newDF.at[new_index, newCol] = value
                newDF.at[new_index, 'symbol'] = symbol
                newDF.at[new_index, 'year'] = year
    return newDF

    
    
def create_empty_df(columnList, length):
    rows = [[None for i in range(len(columnList))] for j in range(length)]
    df = pd.DataFrame(rows, columns=columnList)
    return df

def choose_new_index(oldIndex, year, yearList):
    base = oldIndex * len(yearList)
    return base + yearList.index(year)
    
    

import pandas as pd
from horizontalView import naming_convention
import metrics


def analysis_naming_convention(endYear, startYear, percent=False):
    name = str(startYear) + "-" + str(endYear) + "horizontal"
    if percent:
        name += "Perc"
    return name


def analysis(df, endYear, startYear):
    df = df[df[naming_convention(endYear)].notnull(
    ) & df[naming_convention(startYear)].notnull()]
    horizontal = []
    horizontalPerc = []
    for index, row in df.iterrows():
        startVal = row[naming_convention(startYear)]
        endVal = row[naming_convention(endYear)]
        thisHorizontal, thisHorizontalPerc = metrics.horizontal(startVal, endVal)
        horizontal.append(thisHorizontal)
        horizontalPerc.append(thisHorizontalPerc)
    df[analysis_naming_convention(endYear, startYear)] = horizontal
    df[analysis_naming_convention(
        endYear, startYear, percent=True)] = horizontalPerc

    # https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html
    return df

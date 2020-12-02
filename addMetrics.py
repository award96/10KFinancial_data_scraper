import pandas as pd
import numpy as np
import finnAPI
from utilities import (generate_years_list, 
                        name_stock_col, 
                        safe_index, 
                        split_year,
                        add_empty_cols,
                        name_horiz_col)
"""
    Utilize the basic financials FinnHub API endpoint to add time series
    metrics to your dataframe
"""
def add(df, year, baseYear, conceptList=['operatingMargin']):
    df = add_empty_cols(df, conceptList, year, baseYear)
    for index, row in df.iterrows():
        symb = row['symbol']
        basic_financials = finnAPI.get_basic_financials_json(symb)
        series_data = safe_index(basic_financials, 'series', {})
        annual_data = safe_index(series_data, 'annual', {})
        for concept in conceptList:
            concept_annual = safe_index(annual_data, concept, [])
            for concept_thisYear in concept_annual:
                period = safe_index(concept_thisYear, 'period', None)
                value = safe_index(concept_thisYear, 'v', np.nan)
                thisYear = split_year(period)
                if thisYear and thisYear <= year and thisYear >= baseYear:
                    thisCol = name_horiz_col(concept, thisYear)
                    df.at[index, thisCol] = value
    return df

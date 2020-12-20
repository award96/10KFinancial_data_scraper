if __name__ == "__main__":
    import collectBasic
    # find all the ticker symbols listed on FinnHub's API
    # from the US exchange. Write them to ticker_symbols_output
    # Find basic info on all the companies in ticker_symbols_output
    # Write that data to basic_data_output
    ticker_symbols_output = 'csv_data/symbols.csv'
    basic_data_output = 'csv_data/basic.csv'
    exchange = 'US' # Note: downloading all this data will take a while
    collectBasic.collect(ticker_symbols_output, basic_data_output, exchange)

    import collectJson
    # For each company in basic_data_output, if it fits the industry,
    # gather all 10k financial statements on it, and write them to json files
    industry = 'Biotechnology'
    collectJson.collect(basic_data_output, [industry])

    from horizontalProfile import HorizontalProfile
    # For each company in basic_data_output, if it fits the industry,
    # mine the json files for the relevant concepts, and create a 
    # Pandas Dataframe where each row is a company

    conceptList = [
        'NetIncomeLoss',
        'OperatingIncomeLoss',
        'ResearchAndDevelopmentExpense',
        'GeneralAndAdministrativeExpense',
        'Revenues',
        'CostOfGoodsSold',
        'SalesRevenueGoodsNet',
        'SalesRevenueNet',
        'PaymentsToAcquirePropertyPlantAndEquipment',
        'NetCashProvidedByUsedInOperatingActivities',
        'CommonStockValue',
        'CashAndCashEquivalentsAtCarryingValue'
    ]

    
    summary_output = 'csv_data/biotech.csv'
    timeseries_output = 'csv_data/biotech_timeSeries.csv'

    hp = HorizontalProfile(
        filepath=basic_data_output,
        baseYear=2015,
        year=2020,
        symbol=None,
        industry=industry,
        outputPath=summary_output,
        inputPath=None,
        conceptList=conceptList
    )
    # Next write it to a csv file
    hp.write_to_output()
    # Next reorient the Dataframe so that each row
    # is a 10k statement, then write that to csv
    hp.add_timeSeries()
    hp.write_timeSeries_to_output(timeseries_output)
    
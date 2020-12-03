if __name__ == "__main__":
    from horizontalProfile import HorizontalProfile

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
    hp = HorizontalProfile(
        filepath='csv_data/basic.csv',
        baseYear=2015,
        year=2020,
        symbol=None,
        industry='Biotechnology',
        outputPath='csv_data/biotech.csv',
        inputPath=None,
        conceptList=conceptList
    )
    hp.add_metrics()
    hp.write_to_output(outputPath='csv_data/biotech_with_metrics.csv')
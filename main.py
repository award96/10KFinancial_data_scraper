if __name__ == "__main__":
    from horizontalProfile import HorizontalProfile

    conceptList = [
        'CashAndCashEquivalentsAtCarryingValue',
        'NetIncomeLoss',
        'OperatingIncomeLoss',
        'ResearchAndDevelopmentExpense',
        'GeneralAndAdministrativeExpense',
        'Revenues'
    ]
    hp = HorizontalProfile(
        'csv_data/basic.csv',
        2015,
        2019,
        None,
        'Biotechnology',
        'csv_data/biotech.csv',
        None,
        conceptList
    )
    hp.write_to_output()
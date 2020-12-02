from horizontalSuper import HorizontalSuper
import generateHorizontal

import pandas as pd
import numpy as np


class HorizontalProfile(HorizontalSuper):
    def __init__(
        self,
        filepath,
        baseYear=2018,
        year=2019,
        symbol=None,
        industry="Biotechnology",
        outputPath=None,
        inputPath=None,
        conceptList=['NetIncomeLoss', 'ResearchAndDevelopmentExpense']):

        super().__init__(filepath, 
            symbol=symbol, 
            industry=industry,
            outputPath=outputPath, 
            inputPath=inputPath, 
            conceptList=conceptList)

        self.baseYear = baseYear
        self.year = year

        self.df = self.instantiate_df()
        self.analysis = []

    def __repr__(self):
        start = f"HorizontalProfile generated from filepath: {self.filepath}\n"
        if self.inputPath:
            start = f"HorizontalProfile copied from inputPath: {self.inputPath}\n"
        middle = f"Years range is {self.baseYear} to {self.year}\nThe values are from the list of concepts: {self.conceptList}\n"
        optionSymbol, optionOutput = "", ""
        if self.symbol:
            optionSymbol = f"the focus company is represented by the symbol {self.symbol}\n"
        if self.outputPath:
            optionOutput = f"If the results are written to output, the path will be {self.outputPath}"
        return start + middle + optionSymbol + optionOutput

    def __str__(self):
        return f"filepath: {self.filepath} , baseYear: {self.baseYear} , year: {self.year} symbol: {self.symbol} , industry: {self.industry} , inputPath: {self.inputPath} , outputPath: {self.outputPath} , conceptList: {self.conceptList}"

    def get_baseYear(self):
        return self.baseYear

    def get_year(self):
        return self.year

    def get_col_names(self, excludeBase=False):
        if self.df:
            return list(df.columns)
        else:
            raise ValueError("self.df is None type")

    def instantiate_df(self):
        print(f"\n\nInstantiating df")
        if self.inputPath:
            print(f"copying from inputPath = {self.inputPath}")
            return pd.read_csv(self.inputPath)
        print(f"generating from filepath = {self.filepath}")
        return generateHorizontal.generate(self.filepath,
                                            self.industry,
                                            self.get_conceptList(),
                                            self.year,
                                            self.baseYear)
    


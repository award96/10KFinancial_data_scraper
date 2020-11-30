from horizontalSuper import HorizontalSuper
from horizontalAnalysis import HorizontalAnalysis
import horizontalView
import horizontalCalc

import pandas as pd
import numpy as np


class HorizontalProfile(HorizontalSuper):
    def __init__(
        self,
        filepath,
        baseYear=2018,
        year=2019,
        symbol=None,
        industry=None,
        outputPath=None,
        inputPath=None,
        key="netIncome",
        baseCols=[
            'symbol',
            'industry',
            'marketCap']):

        super().__init__(filepath, 
            symbol=symbol, 
            industry=industry,
            outputPath=outputPath, 
            inputPath=inputPath, 
            key=key, 
            baseCols=baseCols)

        self.baseYear = baseYear
        self.year = year

        self.df = self.instantiate_df()
        self.analysis = []

    def __repr__(self):
        start = f"HorizontalProfile from filepath: {self.filepath}\nYears range is {self.baseYear} to {self.year}\nThe values are from the key: {self.key}\n"
        optionSymbol, optionOutput = "", ""
        if self.symbol:
            optionSymbol = f"the focus company is represented by the symbol {self.symbol}\n"
        if self.outputPath:
            optionOutput = f"If the results are written to output the path will be {self.outputPath}"
        return start + optionSymbol + optionOutput

    def __str__(self):
        return f"filepath: {self.filepath} , baseYear: {self.baseYear} , year: {self.year} symbol: {self.symbol} , outputPath: {self.outputPath} , key: {self.key}"

    def get_baseYear(self):
        return self.baseYear

    def get_year(self):
        return self.year

    def get_col_names(self, excludeBase=False):
        yearsList = horizontalView.generate_years_list(
            self.year, self.baseYear)
        if excludeBase:
            return horizontalView.name_columns(yearsList, base=[])[0]
        return horizontalView.name_columns(yearsList, base=self.baseCols)
        
    def get_analysis(self):
        result = []
        for dataFrame in self.analysis:
            result.append(dataFrame.copy(deep=True))
        return result

    def instantiate_df(self):
        print(f"\n\nInstantiating df\nself.inputpath = {self.inputPath}")
        if self.inputPath:
            print("reading from inputPath")
            return pd.read_csv(self.inputPath, index_col=0)
        print("generating from filepath")
        return horizontalView.generate_horizontal_df(
            self.filepath, self.year, self.baseYear, key=self.key, baseCols=self.baseCols)
    
    def calculate_horiz_analysis(self, endYear, startYear):
        analysis_df = horizontalCalc.analysis(self.df, endYear, startYear)
        oldColumns = self.get_col_names(excludeBase=True)
        analysis_df = analysis_df.drop(columns = oldColumns)
        return analysis_df

    def create_horiz_analysis(self, endYear, startYear, analysisOutput):
        analysis_df = self.calculate_horiz_analysis(endYear=endYear, startYear=startYear)
        new_horizontal_analysis = HorizontalAnalysis(filepath=self.filepath,
            yearsList=[(endYear, startYear)],
            df=analysis_df,
            symbol=self.symbol,
            outputPath=analysisOutput,
            inputPath=self.outputPath,
            key=self.key,
            baseCols=self.baseCols)
        return new_horizontal_analysis


import pandas as pd
import numpy as np

from horizontalSuper import HorizontalSuper
import generateHorizontal
import addMetrics
import timeSeries
"""
    An object to keep track of the meaning behind a dataframe (ie what industry are we looking at)
    and to smooth the process of synthesizing JSON and CSV data, then writing it to a new csv file.

    hp = HorizontalProfile(**args)
    hp.write_to_output()
"""

class HorizontalProfile(HorizontalSuper):
    def __init__(
        self,
        filepath, # same as basicPath in collectBasic.collect method
        baseYear=2018,
        year=2019,
        symbol=None,
        industry="Biotechnology",
        outputPath=None, # what path to write the finished HP to
        inputPath=None, # if you've previously instantiated a HP and written it to csv
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

    def __str__(self):
        start = f"HorizontalProfile object generated from filepath: {self.filepath}\n"
        if self.inputPath:
            start = f"HorizontalProfile copied from inputPath: {self.inputPath}\n"
        middle = f"Years range is {self.baseYear} to {self.year}\nThe values are from the list of concepts: {self.conceptList}\n"
        optionSymbol, optionOutput = "", ""
        if self.symbol:
            optionSymbol = f"the focus company is represented by the symbol {self.symbol}\n"
        if self.outputPath:
            optionOutput = f"If the results are written to output, the path will be {self.outputPath}"
        return start + middle + optionSymbol + optionOutput

    def __repr__(self):
        return f"filepath: {self.filepath} , baseYear: {self.baseYear} , year: {self.year} symbol: {self.symbol} , industry: {self.industry} , inputPath: {self.inputPath} , outputPath: {self.outputPath} , conceptList: {self.conceptList}"

    def get_baseYear(self):
        return self.baseYear

    def get_year(self):
        return self.year

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
    def validateDF(self, newDF, write_on_error):
        if (type(newDF) != pd.core.frame.DataFrame):
            raise ValueError(f"new dataframe is of type {type(newDF)}, should be pandas dataframe")
        lengthOld = self.df.shape[0]
        lengthNew = newDF.shape[0]
        colNumOld = len(list(self.df.columns))
        colNumNew = len(list(newDF.columns))
        if (lengthOld == lengthNew) and (colNumOld < colNumNew):
            return True
        else:
            if write_on_error:
                newDF.to_csv(self.outputPath.split('.csv')[0] + '_error.csv', index=False)
            print("newDF.info():")
            newDF.info()
            raise ValueError(f"New Dataframe has lost columns or added rows\nlength: {lengthNew}, width: {colNumNew}")

    def add_metrics(self, newMetricsList=['operatingMargin'], write_on_error=True):
        self.metricsList = newMetricsList
        newDF = addMetrics.add(self.get_df(), 
                                self.year, 
                                self.baseYear, 
                                self.metricsList)

        if self.validateDF(newDF, write_on_error):
            self.df = newDF

    def add_timeSeries(self):
        new_timeSeries = timeSeries.convert(self.get_df())
        self.timeSeries = new_timeSeries
import pandas as pd

"""
    This parent class is used by the child class
    HorizontalProfile
"""
class HorizontalSuper:
    def __init__(
        self,
        filepath,
        symbol,
        industry,
        outputPath,
        inputPath,
        conceptList):
        self.filepath = filepath
        self.symbol = symbol
        self.industry = industry
        self.outputPath = outputPath
        self.inputPath = inputPath
        self.conceptList = conceptList
        self.df = None
        self.timeSeries = None

    def get_filepath(self):
        return self.filepath

    def get_symbol(self):
        return self.symbol

    def get_industry(self):
        return self.industry

    def get_outputPath(self):
        return self.outputPath

    def get_conceptList(self):
        return self.conceptList.copy()

    def __get_dataframe_obj(self, dfObj):
        """
            Do not call this function outside of the class
        """
        if dfObj is None:
                raise ValueError("dataframe is not yet defined")
        else:
            if (type(dfObj) != pd.core.frame.DataFrame):
                raise ValueError(f"dataframe is of type {type(dfObj)}, should be pandas dataframe")
            return dfObj.copy(deep=True)

    def get_df(self):
        return self.__get_dataframe_obj(self.df)

    def get_timeSeries(self):
        return self.__get_dataframe_obj(self.timeSeries)

    def get_col_names(self):
        if self.df is None:
            raise ValueError("self.df is NoneType")
        else:
            return list(self.df.columns)

    def __write_df_obj(self, dfObj, outputPath):
        """
            Class Method
        """
        if outputPath:
            self.outputPath = outputPath
        if (not outputPath) and (not self.outputPath):
            raise ValueError(
                "outputPath is None.\noutputPath is not defined in the method call, and outputPath was not defined upon instantiation")
        dfObj.to_csv(self.outputPath, index=False)

    def write_to_output(self, outputPath=None):
        self.__write_df_obj(self.df, outputPath)

    def write_timeSeries_to_output(self, outputPath=None):
        self.__write_df_obj(self.timeSeries, outputPath)

    
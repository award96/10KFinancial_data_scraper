import pandas as pd
import horizontalView

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

    def get_df(self):
        if not self.df:
                raise ValueError("self.df is not yet defined")
        else:
            if (type(self.df) != pd.core.frame.DataFrame):
                raise ValueError(f"self.df is of type {type(self.df)}, should be pandas dataframe")
            return self.df.copy(deep=True)

    def write_to_output(self, outputPath=None):
        if outputPath:
            self.outputPath = outputPath
        if (not outputPath) and (not self.outputPath):
            raise ValueError(
                "outputPath is None.\noutputPath is not defined in the method call, and outputPath was not defined upon instantiation")
        self.df.to_csv(self.outputPath, index=False)
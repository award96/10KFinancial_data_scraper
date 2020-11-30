import pandas as pd
import horizontalView

class HorizontalSuper:
    def __init__(
        self,
        filepath,
        symbol=None,
        industry=None,
        outputPath=None,
        inputPath=None,
        key="netIncome",
        baseCols=[
            'symbol',
            'industry',
            'marketCap']):
        self.filepath = filepath
        self.symbol = symbol
        self.industry = industry
        self.outputPath = outputPath
        self.inputPath = inputPath
        self.key = key
        self.baseCols = baseCols
        self.df = None

    def get_filepath(self):
        return self.filepath

    def get_symbol(self):
        return self.symbol
    def get_industry(self):
        return self.industry

    def get_outputPath(self):
        return self.outputPath

    def get_key(self):
        return self.key

    def get_df(self):
        if (type(self.df) != pd.core.frame.DataFrame):
            raise ValueError("self.df is not the correct type, should be pandas dataframe")
        return self.df.copy(deep=True)

    def write_to_output(self, outputPath=None):
        if outputPath:
            self.outputPath = outputPath
        if (not outputPath) and (not self.outputPath):
            raise ValueError(
                "outputPath is None.\noutputPath is not defined in the method call, and outputPath was not defined upon instantiation")
        self.df.to_csv(self.outputPath)
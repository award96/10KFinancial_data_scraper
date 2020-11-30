from horizontalSuper import HorizontalSuper
import horizontalCalc
import plotData

class HorizontalAnalysis(HorizontalSuper):
    def __init__(self, 
        filepath,
        yearsList, 
        df,
        symbol=None, 
        industry=None,
        outputPath=None, 
        inputPath=None, 
        key='netIncome', 
        baseCols=['symbol','industry','marketCap']):

        super().__init__(filepath, 
            symbol=symbol,
            industry=industry, 
            outputPath=outputPath, 
            inputPath=inputPath, 
            key=key, 
            baseCols=baseCols)


        self.yearsList = yearsList
        self.validate_yearList()
        self.df = df
        
    def get_col_names(self, excludeBase=False):
        analysis_cols = []
        for yearTuple in self.yearsList:
            analysis_cols.extend([horizontalCalc.analysis_naming_convention(yearTuple[0], yearTuple[1]), horizontalCalc.analysis_naming_convention(yearTuple[0], yearTuple[1], percent=True)])
        if excludeBase:
            return analysis_cols
        return self.baseCols + analysis_cols

    def histo(self):
        # self.symbol, self.industry
        for yearTuple in self.yearsList:
            # make a separate histo
            data = self.df[horizontalCalc.analysis_naming_convention(yearTuple[0],yearTuple[1])]
            if self.industry:
                data = data[data['industry'] == self.industry]
            # TODO check that self.symbol wasn't removed
            data = data.tolist() 
            title = f"Histogram of change in {self.key} from {yearTuple[1]} to {yearTuple[0]}"
            xaxisLabel = f"{self.key} (millions)"
            plotData.analysis_histo(data, title, xaxisLabel, bins=20)

    def validate_yearList(self):
        if (type(self.yearsList) != list):
            raise ValueError("yearList must be a list of tuples (biggerYear, smallerYear")
        for index, tuple_ in enumerate(self.yearsList):
            if (type(tuple_) != tuple):
                raise ValueError(f"A value of yearsList was not a tuple\nindex = {index}, type(val) = {type(tuple_)}")
            if (tuple_[0] <= tuple_[1]):
                raise ValueError(f"Tuples stored in yearsList must be of the format (biggerYear, smallerYear) where biggerYear > smallerYear\nFor index = {index}, biggerYear = {tuple_[0]} and smallerYear = {tuple[1]}")
        

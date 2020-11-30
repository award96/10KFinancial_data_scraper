import os.path
import sys


from horizontalProfile import HorizontalProfile
from horizontalAnalysis import HorizontalAnalysis
from utilities import generate_all_year_pairs

def analyze(HP, yearTuple, analysisBaseName):
     # analysisOutput = exampleName2019-2011.csv
    print(f"\nAnalyzing {yearTuple}")
    analysisOutput = analysisBaseName + str(yearTuple[1]) + "-" + str(yearTuple[0]) + ".csv"
    HA = HP.create_horiz_analysis(yearTuple[0], yearTuple[1], analysisOutput)
    HA.write_to_output()
    print(f"writing to {HA.get_outputPath()}\n")

def main(
        outputPath,
        yearRange, 
        horizontalInput, 
        horizontalOutput,
        analysisBaseName,
        analyzeAllYears, 
        specificYears,
        key
        ):

    HP = HorizontalProfile(filepath=outputPath,
        baseYear=yearRange[1],
        year=yearRange[0],
        inputPath=horizontalInput,
        outputPath=horizontalOutput,
        key=key)
    if not horizontalInput:
        HP.write_to_output()
    if analyzeAllYears:
        for yearTuple in generate_all_year_pairs(yearRange):
            analyze(HP, yearTuple, analysisBaseName)
    else:
        for yearTuple in specificYears:
            analyze(HP, yearTuple, analysisBaseName)

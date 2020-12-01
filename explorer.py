from utilities import name_json_file, safe_index

import os
import pandas as pd
import json

def mine_subreport(subreport):
    """
        take a BS, CF, or IC, and get all the useful info out of it
    """
    if type(subreport) == dict:
        print("\n\n###############\nfound dictionary!\n")
        for key in subreport:
            print(f"{key}:   {subreport[key]}")

def explore(filepath, industry):
    df = pd.read_csv(filepath, index_col=0)
    df = df[df['industry'] == industry]
    length = df.shape[0]
    years = {}
    bs_concepts = {}
    cf_concepts = {}
    ic_concepts = {}

    for index, row in df.iterrows():
        symb = row['symbol']
        print(f"\non file\n{name_json_file(symb)}")
        with open(name_json_file(symb), 'r') as jsonFile:
            tenKs = json.load(jsonFile)
        tenKarr = tenKs['data']
        for tenK in tenKarr:
            thisYear = safe_index(tenK, 'year', 'Null', printObject=True)
            if thisYear in years:
                years[thisYear] += 1
            else:
                years[thisYear] = 1

            report = safe_index(tenK, 'report', {}, printObject=True)
            bs = safe_index(report, 'bs', [], printObject=True)
            cf = safe_index(report, 'cf', [], printObject=True)
            ic = safe_index(report, 'ic', [], printObject=True)
            for item in bs:
                thisConcept = safe_index(item, 'concept', 'Null', printObject=True)
                if thisConcept in bs_concepts:
                    bs_concepts[thisConcept] += 1
                else:
                    bs_concepts[thisConcept] = 1
            for item in cf:
                thisConcept = safe_index(item, 'concept', 'Null', printObject=True)
                if thisConcept in cf_concepts:
                    cf_concepts[thisConcept] += 1
                else:
                    cf_concepts[thisConcept] = 1
            for item in ic:
                thisConcept = safe_index(item, 'concept', 'Null', printObject=True)
                if thisConcept in ic_concepts:
                    ic_concepts[thisConcept] += 1
                else:
                    ic_concepts[thisConcept] = 1
    print("\n\ndone!\n")
    print("\nYEARS\n")
    for key in years:
        print(f"{key}: {years[key]}")
    print("\n\nBS CONCEPTS\n")
    for key in bs_concepts:
        if bs_concepts[key] > length//20:
            print(f"{key}: {bs_concepts[key]}")
    print("\n\nCF CONCEPTS\n")
    for key in cf_concepts:
        if cf_concepts[key] > length//20:
            print(f"{key}: {cf_concepts[key]}")
    print("\n\nIC CONCEPTS\n")
    for key in ic_concepts:
        if ic_concepts[key] > length//20:
            print(f"{key}: {ic_concepts[key]}")
    print("\n##############\n")

    
        

explore('basic.csv', 'Biotechnology')

"""

cik
symbol
data - [array of filings] - 
                            year
                            startDate
                            endDate
                            report - {obj of rep types} - 
                                                            bs - [arr of concept-value pairs]
                                                            cf - [arr of concept-value pairs]
                                                            ic - [arr of concept-value pairs]
        
"""
from utilities import name_json_file, safe_index

import os
import pandas as pd
import json

def count_concepts_subreport(subreport, dictionary):
    if type(subreport) == dict:
       for key in subreport:
            if key in dictionary:
               dictionary[key] += 1
            else:
                dictionary[key] = 1
    elif type(subreport) == list:
       for item in subreport:
            thisConcept = safe_index(item, 'concept', 'Null', printObject=True)
            if thisConcept in dictionary:
                dictionary[thisConcept] += 1
            else:
                dictionary[thisConcept] = 1
    return dictionary

def print_findings(dictionary, minimum=25):
    for k, v in sorted(dictionary.items(), key=lambda p:p[1], reverse=True):
        if "NetIncome" in k or "netIncome" in k or "Netincome" in k or "netincome" in k:
            print(f"{k}:   {v}")


def explore(filepath, industry):
    count_docs = 0
    df = pd.read_csv(filepath, index_col=0)
    df = df[df['industry'] == industry]
    years = {}
    bs_concepts = {}
    cf_concepts = {}
    ic_concepts = {}

    for index, row in df.iterrows():
        symb = row['symbol']
        with open(name_json_file(symb), 'r') as jsonFile:
            tenKs = json.load(jsonFile)
        tenKarr = tenKs['data']
        for tenK in tenKarr:
            count_docs += 1
            thisYear = safe_index(tenK, 'year', 'Null', printObject=True)
            if thisYear in years:
                years[thisYear] += 1
            else:
                years[thisYear] = 1

            report = safe_index(tenK, 'report', {}, printObject=True)
            bs = safe_index(report, 'bs', [], printObject=True)
            cf = safe_index(report, 'cf', [], printObject=True)
            ic = safe_index(report, 'ic', [], printObject=True)
            bs_concepts = count_concepts_subreport(bs, bs_concepts)
            cf_concepts = count_concepts_subreport(cf, cf_concepts)
            ic_concepts = count_concepts_subreport(ic, ic_concepts)
            
    print("\n\ndone!\n")
    print(f"{count_docs} 10K statements viewed")
    print("\nCOUNT OF YEARS VIEWED\n")
    for key in years:
        print(f"{key}: {years[key]}")
    print("\n\nCOUNT OF BS CONCEPTS VIEWED\n")
    print_findings(bs_concepts, count_docs//4)
    print("\n\nCOUNT OF CF CONCEPTS VIEWED\n")
    print_findings(cf_concepts, count_docs//4)
    print("\n\nCOUNT OF IC CONCEPTS VIEWED\n")
    print_findings(ic_concepts, count_docs//4)
    print("\n##############\n")

    
        

explore('basic.csv', 'Biotechnology')

"""
Structure of API response

cik
symbol
data - [array of filings] - 
                            year
                            startDate
                            endDate
                            report - {obj of report types} - 
                                                            bs - [arr of concept-value pairs]
                                                            cf - [arr of concept-value pairs]
                                                            ic - [arr of concept-value pairs]

                                                            NOTE - bs, cf, and ic can also be dictionaries
                                                                    of the form concept: value

                                                                    ie
                                                                    {
                                                                        concept1: value1,
                                                                        concept2: value2,
                                                                        ...
                                                                    }
                                                            a concept is something like "NetIncomeLoss"
        
"""
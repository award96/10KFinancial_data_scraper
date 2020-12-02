import os
import pandas as pd
import json

from utilities import name_json_file, safe_index

"""
    When deciding what 'concepts' (essentially finnhub's keys as to what the data you're shown means)
    to record data on, this module provides the function 'explore', which will give the user an overview of
    what concepts are frequently recorded in the data, and what years are frequently recorded.

    What this module will tell you is what concepts are worth using as 'keys' to parse through the JSON data,
    and what concepts hardly appear at all.
"""

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
        if v > minimum:
            print(f"{k}:   {v}")


def explore(filepath, industry):
    count_docs = 0
    df = pd.read_csv(filepath, index_col=0)
    df = df[df['industry'] == industry]
    length = df.shape[0]
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
    for key, val in sorted(years.items(), reverse=True):
        print(f"{key}: {years[key]}")
    print("\n\nCOUNT OF BS CONCEPTS VIEWED\n")
    print_findings(bs_concepts, count_docs//4)
    print("\n\nCOUNT OF CF CONCEPTS VIEWED\n")
    print_findings(cf_concepts, count_docs//4)
    print("\n\nCOUNT OF IC CONCEPTS VIEWED\n")
    print_findings(ic_concepts, count_docs//4)
    print("\n##############\n")

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
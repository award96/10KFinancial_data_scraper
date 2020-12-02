import traceback

"""
    Functions that have a more general use across the package
"""

def safe_index(dict_obj, key, returnOnError, printObject=False):
    try:
        return dict_obj[key]
    except Exception:
        print("function utilities.safe_index() caught error")
        traceback.print_exc()
        print(f"\nreturning {returnOnError}\n")
        if printObject:
            print(f"dict_obj:  {dict_obj}\nkey: {key}\n")
        return returnOnError


def clean_duplicates(messyList):
    output = []
    d = {}
    for item in messyList:
        if item in d:
            continue
        else:
            output.append(item)
            d[item] = True
    return output

def generate_all_year_pairs(yearRange):
    allPairs = []
    high, low = yearRange[0], yearRange[1]
    while high > low:
        while low < high:
            allPairs.append((high, low))
            low += 1
        low = yearRange[1]
        high -= 1
    return allPairs

def generate_years_list(year, baseYear):
    """
    ARGS:
        year (int) - usually the current year
        baseYear (int) - the start year (must be less than year)
    RETURNS:
        a list of ints. Descends from year to baseYear. Includes baseYear
        if the input is (2019, 2017) the list will be:
        [2019, 2018, 2017]
    """
    if (baseYear > year):
        raise ValueError(
            "baseYear must be less than year.\nThis error was raised by 'generate_years_list'")
    output = []
    while year >= baseYear:
        output.append(year)
        year -= 1
    return output

def name_json_file(symbol):
    return 'json_data/' + symbol + '_json.csv'

def name_horiz_col(concept, year):
    if (type(concept) != str):
        concept = str(concept)
    return str(year) + concept
def list_to_dict(list_):
    d = {}
    for item in list_:
        d[item] = True
    return d
import traceback


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

def name_json_file(symbol):
    return 'data/' + symbol + '_json.csv'
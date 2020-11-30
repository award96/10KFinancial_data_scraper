"""
    read in symbols
    write down shared concepts
    write down data to csv

"""
import csv
import pandas as pd


def read_lines_to_array(filepath):
    lines_arr = []
    with open(filepath, 'r') as file:
        for line in file:
            # finnhub api only knows symbols without - and .
            if ("-" in line) or ("." in line):
                continue
            line = line.replace("\n", "")
            lines_arr.append(line)
    return lines_arr

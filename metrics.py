import pandas as pd
import numpy as np

def horizontal(start, end):
    val = end - start
    if (start == 0) or (start == np.nan):
        return (val, np.nan)
    percent = val * 100 / abs(start)
    return (val, percent)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def decorate():
    plt.ticklabel_format(axis="x", style="sci", scilimits=(6, 6))


def analysis_histo(data, title, xaxisLabel,bins=20):
     # Draw
    plt.figure(figsize=(16, 9))
    n, bins, patches = plt.hist(data, bins=bins, color='purple')
    # Decoration
    plt.title(title)
    plt.xlabel(xaxisLabel)
    decorate()
    plt.ylabel("Count")

    plt.show()

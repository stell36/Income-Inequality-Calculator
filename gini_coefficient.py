import numpy as np
import sys
import json
import csv
import os

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the full path to 'gini_input.csv' in the same directory
gini_input = os.path.join(current_dir, 'gini_input.csv')

def gini_pairwise(incomes):
    """
    Calculate the Gini coefficient of a list of incomes using the pairwise method.

    Parameters:
    incomes (list of float): List of income values.

    Returns:
    float: Gini coefficient.
    """
    n = len(incomes)
    if n == 0:
        return -1

    avg_income = np.nanmean(incomes)
    if avg_income == 0:
        return 0.0

    # Calculate the sum of absolute differences
    abs_diff_sum = 0.0
    for i in range(n):
        for j in range(n):
            if not (np.isnan(incomes[i]) or np.isnan(incomes[j])):
                abs_diff_sum += abs(incomes[i] - incomes[j])

    # Gini coefficient formula
    gini = abs_diff_sum / (2 * n**2 * avg_income)
    return gini

def gini_cumulative(incomes):
    """
    Calculate the Gini coefficient of a list of incomes using the cumulative method.

    Parameters:
    incomes (list of float): List of income values.

    Returns:
    float: Gini coefficient.
    """
    n = len(incomes)
    if n == 0:
        return -1

    # Sort the incomes
    sorted_incomes = np.sort(incomes)
    
    # Calculate the cumulative income and population shares
    cum_income = np.nancumsum(sorted_incomes)
    #cum_population = np.arange(1, n + 1)

    # Calculate the Gini coefficient using the cumulative method
    gini = 1 - (2 * np.sum(cum_income) / (n * cum_income[-1])) + (1 / n)
    
    return gini 
def readCSV(filename):
    incomes = []
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            try:
                value = float(row[0])
                incomes.append(value)
            except (ValueError, IndexError):
                continue
    return incomes

incomes = readCSV(gini_input)
print(gini_pairwise([50, 50, 70, 70, 70, 90, 150, 150, 150, 150]))
print(gini_cumulative([50, 50, 70, 70, 70, 90, 150, 150, 150, 150]))
print(gini_pairwise(incomes))
print(gini_cumulative(incomes))
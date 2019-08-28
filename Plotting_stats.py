# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 15:25:17 2019

@author: sseifi
"""

import pandas as pd
import seaborn as sns

import matplotlib.pyplot as plt

# Reading the global data sheet
TAV_data = pd.read_csv('TAV_spreadsheet.csv')

# Reading the final ASTM-F136 filetered datasheet (See: ASTM-F136.py)
TAV_data_final = pd.read_csv('TAV_spreadsheet_ASTM_compliant.csv')

# Getting the data set ready
TAV_data = TAV_data[["LosNr", "E (mean)", "Rm (mean)", "Rp (mean)" , "Ultimate Strain (mean)", "Necking (mean)", "Thickness"]]
TAV_data = TAV_data.replace('', 'NaN')      # replace missing data with NaN: pandas can handle NaN
TAV_data = TAV_data.astype(float)           # strings to float
TAV_data["LosNr"] = TAV_data["LosNr"].astype(int)   # Lot numbers should be integers

# Change empty values to NaN: seaborn package can handle NaNs
TAV_data = TAV_data.replace('', 'NaN')

# Initilize all lots as failed in ASTM-F136 
TAV_data['ASTM-F136'] = 'Failed'

# Change the failed to their correct value if they're passed
Passed_TAV_LosNr = list(TAV_data_final['LosNr'])
for i in Passed_TAV_LosNr:
    TAV_data.loc[TAV_data["LosNr"] == i, ["ASTM-F136"]]="Passed"


# Plotting some exploratory data analysis plots (e.g. Scatter matrix and heatmap)
cols = ['E (mean)', 'Rm (mean)', 'Rp (mean)', 'Ultimate Strain (mean)', 'Necking (mean)', 'ASTM-F136' ]
ScatterMatrix = sns.pairplot(TAV_data[cols], height=2.5, hue = 'ASTM-F136', plot_kws={'alpha': 0.5})
ScatterMatrix.savefig("Scatter.png")
plt.close()

CoorMatrix = sns.heatmap(TAV_data[cols].corr(), annot=True)
figure = CoorMatrix.get_figure()    
figure.savefig('Heatmap.png', dpi=400,  bbox_inches='tight')


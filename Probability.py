# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 15:03:11 2019

@author: sseifi
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Reading data
TAV_data = pd.read_csv('TAV_spreadsheet_ASTM_compliant.csv')


TAV_data['Probability_l'] = 0.0
TAV_data['Probability_u'] = 0.0

# Find the probablity of the lots
for lot_number1 in TAV_data['LosNr']:
    count_l = 0
    count_u = 0
    material1 = TAV_data[TAV_data['LosNr'] == lot_number1]
    for lot_number2 in TAV_data['LosNr']:
        material2 = TAV_data[TAV_data['LosNr'] == lot_number2]
        if (material2.E_mean.values[0]*0.955 < material1.E_mean.values[0] and 
            material2.Rp_mean.values[0]*0.955 < material1.Rp_mean.values[0] and
            material2.Rm_mean.values[0]*0.955 < material1.Rm_mean.values[0]):
            count_l = count_l+ 1
        if (material2.E_mean.values[0]*1.045 > material1.E_mean.values[0] and 
            material2.Rp_mean.values[0]*1.045 > material1.Rp_mean.values[0] and
            material2.Rm_mean.values[0]*1.045 > material1.Rm_mean.values[0]):
            count_u = count_u + 1
        
    TAV_data.loc[TAV_data["LosNr"] == lot_number1, ["Probability_l"]]= 100*round(count_l/(len(TAV_data)),2)
    TAV_data.loc[TAV_data["LosNr"] == lot_number1, ["Probability_u"]]= 100*round(count_u/(len(TAV_data)),2)

TAV_data.Probability = TAV_data.Probability_l.astype(int)
TAV_data.Probability = TAV_data.Probability_u.astype(int)

# Plotting some probability plots
fig1 = plt.figure(figsize = (7,7))
sns.scatterplot(TAV_data['Rp_mean'], TAV_data['Rm_mean'], hue = TAV_data['Probability_l'], s=50)
fig1.savefig('RpRm_probability.png', dpi=400,  bbox_inches='tight')


fig2 = plt.figure(figsize = (7,7))
sns.scatterplot(TAV_data['E_mean'], TAV_data['Rp_mean'], hue = TAV_data['Probability_l'], s=50)
fig2.savefig('ERp_probability.png', dpi=400,  bbox_inches='tight')

fig3 = plt.figure(figsize = (7,7))
sns.scatterplot(TAV_data['E_mean'], TAV_data['Rm_mean'], hue = TAV_data['Probability_l'], s=50)
fig3.savefig('ERm_probability.png', dpi=400,  bbox_inches='tight')

TAV_data.to_csv('TAV_spreadsheet_ASTM_compliant_probability.csv')
# -*- coding: utf-8 -*-
"""
Created on Tue May 14 10:14:09 2019

@author: sseifi
"""
import pandas as pd
import numpy as np

def ASTMF136_Criteria_Check(material):    
    
    # getting material atrributes
    thickness = material.Thickness.values[0]
    Rm = material.Rm_mean.values[0]
    Rp = material.Rp_mean.values[0]
    elongation = material.Elongation_mean.values[0]
    
    # this boolean determines if the criteria is passed for material
    flag = True
    
    # ASTM-F136 criteria according to page 3 table 2.    
    if (thickness <= 4.75 and Rm >= 860.0 and Rp >= 795.0 and elongation >= 10.0):
        flag = False
    
    if (thickness > 4.75 and thickness <= 44.45 and Rm >= 860.0 and Rp >= 795.0 and elongation >= 10.0):
        flag = False
        
    if (thickness > 44.45 and thickness < 63.5 and Rm >= 825.0 and Rp >= 760.0 and elongation >= 8.0):
        flag = False
    
    if (thickness > 63.5 and thickness <= 101.6 and Rm >= 825.0 and Rp >= 760.0 and elongation >= 8.0):
        flag = False
        
    return flag

def Toughness_Approx(material):
    E = material.E_mean.values[0]
    Rm = material.Rm_mean.values[0]
    Rp = material.Rp_mean.values[0]
    elongation = material.Elongation_mean.values[0]
    
    return (Rp+Rm)*0.5*10 - (1.0/(2*E))*((Rp+Rm)*0.5)**2    
   
# Reading the TAV data
TAV_data = pd.read_csv('TAV_spreadsheet.csv')

# Filtering the useful features
TAV_data = TAV_data[['LosNr', 'E (mean)', 'Rp (mean)', 'Rm (mean)', 'Ultimate Strain (mean)', 'Necking (mean)', 'Thickness']]

# Renaming the features to callable attributes
TAV_data.columns = ['LosNr', 'E_mean', 'Rp_mean', 'Rm_mean', 'Elongation_mean', 'Necking_mean', 'Thickness']

# Removing the ones with NaN (Note: Not sure if that's a good idea. Print out a message)
TAV_data_no_nan = TAV_data[~np.isnan(TAV_data).any(axis=1)]

# Make the input data numerics
TAV_data_no_nan['LosNr'].astype(int)
TAV_data_no_nan['E_mean'].astype(float)
TAV_data_no_nan['Rp_mean'].astype(float)
TAV_data_no_nan['Rm_mean'].astype(float)
TAV_data_no_nan['Elongation_mean'].astype(float)
TAV_data_no_nan['Necking_mean'].astype(float)
TAV_data_no_nan['Thickness'].astype(int)

# initializing a list of lots with no compliance
non_compliant_list = []

TAV_data_no_nan['Toughness'] = 0.0

# loop through mateial lots
for lot_number in TAV_data_no_nan['LosNr']:    
    
    # material has attribures of: LosNr, E_mean, Rp_mean etc. that can be called
    material = TAV_data_no_nan[TAV_data_no_nan['LosNr'] == lot_number]    
    
    # Add toughness to the dataset
    toughness = Toughness_Approx(material)
    TAV_data_no_nan.loc[TAV_data_no_nan["LosNr"] == lot_number, ["Toughness"]] = toughness
    
    # check the complicancy if there is none flag the material lot index
    Flag = ASTMF136_Criteria_Check(material)
    if (Flag == True):
        non_compliant_list.append(TAV_data_no_nan[TAV_data_no_nan['LosNr'] == lot_number].index[0])

# remove the flagged lots
TAV_data_final = TAV_data_no_nan.drop(non_compliant_list)

# Output comparisons
print ("              Total number of lots  = ", len(TAV_data))
print ("Number of lots with completed data  = ", len(TAV_data_no_nan))        
print ("Number of lots with ASTM complaince = ", len(TAV_data_final))    

# Create CSV file of the final data set: this is the data set final models are extracted from
TAV_data_final.to_csv('TAV_spreadsheet_ASTM_compliant.csv')
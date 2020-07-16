# -*- coding: utf-8 -*-
"""
This code is for extracting daily simulation results from WEPP
The output file name is grph#.txt
"""

import numpy as np
import pandas as pd

grid_size = 300 #meter
grids = 7303

# Extract only headers and simulations results
header = pd.read_csv('00_header_grph.txt',header = None)

header.columns = ["v"]

# row = number of simulation, column = number of catchment+1
all_sub_sed = np.zeros([2556,grids+1])
j = 0
for i in range(1,grids+1) :
#for i in range(1) :
    print(i)
    grph = pd.read_csv('grph_'+str(i)+'.txt', skiprows=[i for i in range(0,121)], \
                        header = None, delim_whitespace=True,dtype = {'8' :np.float})

    grph.columns = [header.v]
    
    """
    Extract only specific columns
    0 = simulation days,  8 = sediment leaving profile [kg/m]
    cf) 1 = precipitation [mm] -> check the order of "header" to extract more variables
    Since unit of sediment is in kg/m -> multiplying the width of hillslope will be in kg.
    """
    
    daily = grph.iloc[:-5,[0,8]] # drop last 5 rows (max, min, etc) and pick specific columns from grph
    daily.columns = ["day","sediment"]
    
    sediment = daily.sediment.values
    if j == 0 :
        all_sub_sed[:,0] = daily.day.values

    all_sub_sed[:,j+1] = sediment*  grid_size
    j = j+1
    
# the array "all_sub_sed" is time series data for MIKE SHE
grph.to_csv('grph.csv') # last subcatchment results just to check

np.savetxt('00_soil loss.txt',all_sub_sed[:,1:].astype(int),fmt='%.2f',delimiter='\t')

all_years = np.sum(all_sub_sed[:,1:], axis=1)
np.savetxt('00_sum_by_day.txt',all_years.astype(int),fmt='%.2f',delimiter='\t')

all_grids = np.sum(all_sub_sed[:,1:], axis=0)
np.savetxt('00_sum_by_grids.txt',all_grids.astype(int),fmt='%.2f',delimiter='\t')
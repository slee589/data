# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 11:05:28 2019

@author: slee589
"""

import numpy as np
import os

############ run 7303 grid cells with radar precip ################
simul_years = 2019-2013+1
soil = np.loadtxt(r'F:\03_Fisher_radar\WEPP\runs\SOIL\SOIL_CODE.txt')
gauges = np.loadtxt(r'F:\03_Fisher_radar\WEPP\runs\CLIGEN\gauge_output\gauges_code.txt')
land_use = np.loadtxt(r'F:\03_Fisher_radar\WEPP\runs\LAND_USE\land_use.txt')
tillage = np.loadtxt(r'F:\03_Fisher_radar\WEPP\runs\LAND_USE\tillage.txt')

# make run file for each grid
for i in range(1,7303+1) :
    f = open("run"+str(i)+".run","w")
    f.write("M \n") # Metric units selected
    f.write("Yes \n") # Enter N to run watershed option (not a SHELL option).
    f.write("1 \n") # 1 - continuous simulation
    f.write("1 \n") #1 - hillslope version (single hillslope only)
    f.write("No \n") #Do you want hillslope pass file output (Y/N)?
    """
     ---- ---- ------ ------- --- ---------- ----------
 [1] - Abbreviated annual
  2  - Detailed annual
  3  - Abbreviated event by event
  4  - Detailed event by event
  5  - Monthly 
 options for below--------------------------------------
    """
    f.write("5 \n") # Soil loss output options for continuous simulation (5 - monthly)
    f.write("No \n") # Do you want initial condition scenario output (Y/N)?
    f.write("..\output\loss_" + str(i)+".txt \n") #Enter file name for soil loss output --> 
    f.write("Yes \n") # Do you want water balance output (Y/N)?
    f.write("..\output\WB_" + str(i)+".txt \n")  # Enter file name for water balance output
    f.write("No \n") # Do you want crop output (Y/N)?
    f.write("No \n") # Do you want soil output (Y/N)?
    f.write("Yes \n") # Do you want distance and sediment loss output (Y/N)?
    f.write("..\output\plot_" + str(i)+".txt \n") # Enter file name for plotting output
    f.write("Yes \n") # Do you want large graphics output (Y/N)?
    f.write("..\output\grph_" + str(i)+".txt \n") # Enter file name for large graphics output
    f.write("No \n") # Do you want event by event output (Y/N)? 
    f.write("No \n") # Do you want element output (Y/N)
    f.write("Yes \n") # Do you want final summary output (Y/N)?
    f.write("..\output\summary_" + str(i)+".txt \n")
    f.write("No \n") # Do you want daily winter output (Y/N)?
    f.write("No \n") # Do you want plant yield output (Y/N)?
    
    code = i
    code = str(code)    
    # assign management / land use
    if land_use[i-1] == 1 and tillage[i-1] == 1:
        f.write("LAND_USE\corn_no_till.man \n")
    elif land_use[i-1] == 1 and tillage[i-1] == 2:
        f.write("LAND_USE\corn_mulch.man \n")
    elif land_use[i-1] == 1 and tillage[i-1] == 3:
        f.write("LAND_USE\corn_reduced.man \n")
    elif land_use[i-1] == 1 and tillage[i-1] == 4:
        f.write("LAND_USE\corn_conventional.man \n")
    elif land_use[i-1] == 2 and tillage[i-1] == 1:
        f.write("LAND_USE\soybean_no_till.man \n")
    elif land_use[i-1] == 2 and tillage[i-1] == 2:
        f.write("LAND_USE\soybean_mulch.man \n")
    elif land_use[i-1] == 2 and tillage[i-1] == 3:
        f.write("LAND_USE\soybean_reduced.man \n")
    elif land_use[i-1] == 2 and tillage[i-1] == 4:
        f.write("LAND_USE\soybean_conventional.man \n")
    elif land_use[i-1] == 4 and tillage[i-1] == 1:
        f.write("LAND_USE\grass.man \n")
    elif land_use[i-1] == 5 and tillage[i-1] == 1:
        f.write("LAND_USE\l_forest.man \n")
    elif land_use[i-1] == 3 and tillage[i-1] == 1:
        f.write("LAND_USE\l_forest.man \n")
    elif land_use[i-1] == 6 and tillage[i-1] == 1:
        f.write("LAND_USE\winter_wheat.man \n")
    
    # assign slope
    f.write(r"F:\03_Fisher_radar\WEPP\runs\SLOPE\slope"+str(i)+".slp \n")

#    ############################################### Assign gauge climate
    if gauges[i-1] == 2 :
        f.write("output_Normal.cli \n")
    elif gauges[i-1] == 1 :
        f.write("output_Rantoul.cli \n")
    
#    ############################################### Assign radar climate
#    f.write("output_"+str(i)+".cli \n")
        
    # assign soil 
    if soil[i-1] == 1 :
        f.write("SOIL\soil1.sol \n") # PIATT
    elif soil[i-1] == 2 :
        f.write("SOIL\soil2.sol \n") # CHAMPAIGN
    elif soil[i-1] == 3 :
        f.write("SOIL\soil3.sol \n") # FORD
    elif soil[i-1] == 4 :
        f.write("SOIL\soil4.sol \n") # MCLEAN
    f.write("0 \n") # [0] no irrigation
    f.write(str(simul_years)+" \n") # simulation years
    f.write("0 \n") # To bypass erosion calculations for very small events, enter 1
    f.close() 

# batch file
f = open("weppbat_radar.bat","w")
f.write("@echo off \n")
for i in range(1,7303+1) :
    f.write(r'"F:\03_Fisher_radar\WEPP\wepp\wepp.exe" '+ '< run'+str(i)+'.run > run'+str(i)+'.err \n')
f.write("@cls \n")
f.close()     

# run the batch file
os.system(r"F:\03_Fisher_radar\WEPP\runs\weppbat_radar.bat")



"""
   _____                 _                       
  / ____|               | |                      
 | |  __ _ __ __ _ _ __ | |__                    
 | | |_ | '__/ _` | '_ \| '_ \                   
 | |__| | | | (_| | |_) | | | |                  
  \_____|_|  \__,_| .__/|_| |_|    _             
  / ____|         | |             | |            
 | |  __  ___ _ __|_|___ _ __ __ _| |_ ___  _ __ 
 | | |_ |/ _ \ '_ \ / _ \ '__/ _` | __/ _ \| '__|
 | |__| |  __/ | | |  __/ | | (_| | || (_) | |   
  \_____|\___|_| |_|\___|_|  \__,_|\__\___/|_|   
                                                 
Created By Hugo Oliveira                                             
June 2023
"""

import pandas as pd
import numpy as np
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt
import os
from bisect import bisect_left 
import heatinglib as ht
import coolinglib as cl
import pair_elements as pe

t_max = 80 # Higher Temperature
t_min = 25 # Lower Temperature
t_room = 20 # I considered this value as room temperature for the Newton Cooling Law

# === Name of the file without .csv ===
file_name = 'Marble.Ter'

# Some preparations
df = pd.read_csv(file_name + '.csv')
df.columns = ['Time','Res']

# === Number of Cycles ===
number_cycles = 5 

number_points = number_cycles * 3 + 1
number_waits = number_cycles

# Apply Savgov Filter
window_size = 200
polynomial_order = 2
df['Res_Fil'] = savgol_filter(df['Res'], window_size, polynomial_order)

# Plot to Select the Data
plt.figure(figsize=(10, 6))
plt.plot(df['Time'], df['Res_Fil'], '--',color='lightgray')
points_get = plt.ginput(number_points, timeout=600)
plt.close()

# Organize the chosen data
steps = [num[0] for num in points_get]
steps = [round(num, 3) for num in steps]
# print(steps)

# Get the indexes from the data that corresponds to the manual selection
count = 0
indexes_data =[]
for valores in steps:
    indexes_data.append(bisect_left(df['Time'].values, valores))

# Calculating the mean value of the waiting time
pairs_indexes = pe.pair_elements_medias(indexes_data)
mean_values = []
for count in range(number_waits):
    mean_values.append(df['Res_Fil'].loc[pairs_indexes[count][0]:pairs_indexes[count][1]].mean())
media = pd.DataFrame(mean_values)

# Separating the Heating and Cooling Data
pairs_indexes_heating = pe.pair_elements_heating(indexes_data)
pairs_indexes_cooling = pe.pair_elements_cooling(indexes_data)

# Make all the calculations
final_heating_data = ht.heating(pairs_indexes_heating, df, number_cycles, t_min, t_max, t_room)
final_cooling_data = cl.cooling(pairs_indexes_cooling, df, number_cycles, t_min, t_max, t_room)

# Separate the Interval Data
separated_cycles = df[indexes_data[0]:indexes_data[-1]]
separated_cycles['Time'] = separated_cycles['Time'] - separated_cycles['Time'].iloc[0]


ir = separated_cycles['Res_Fil'].iloc[0]/10E3 # Initial Resistance
xh = final_heating_data['Temp']
yh = final_heating_data['Mean']/10E3
h_err = final_heating_data['STD']/10E3
xc = final_cooling_data['Temp']
yc = final_cooling_data['Mean']/10E3
c_err = final_cooling_data['STD']/10E3

plt.figure()
plt.errorbar(xh, (yh-ir)/ir, yerr=h_err/ir, fmt='o-', capsize =4, color='red')
plt.errorbar(xc, (yc-ir)/ir, yerr=c_err/ir, fmt='o-',capsize =4, color='blue')
plt.margins(0)
plt.tick_params(direction='in', axis='both', labelsize=16)
plt.xlabel('Temperature ($^\circ$C)',fontsize=18)
plt.ylabel('$\Delta R / R_{0}$',fontsize=18)
plt.title(file_name)

fname = file_name+'.svg'
plt.savefig(fname, dpi=330, facecolor='w', edgecolor='w',
        orientation='portrait', format='svg',
        transparent=True)
plt.show()

plt.figure()
plt.plot(separated_cycles['Time']/3600, separated_cycles['Res_Fil']/10E3, color='red')
plt.margins(0)
plt.tick_params(direction='in', axis='both', labelsize=16)
plt.xlabel('Time (h)',fontsize=18)
plt.ylabel('Resistance (kOhms)',fontsize=18)
plt.title(file_name)

fname = file_name+'_cycle.svg'
plt.savefig(fname, dpi=330, facecolor='w', edgecolor='w',
        orientation='portrait', format='svg',
        transparent=True)
plt.show()
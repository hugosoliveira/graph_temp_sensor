
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
import matplotlib.ticker as ticker
import heatinglib as ht
import coolinglib as cl
import pair_elements as pe
import cyclepoints as cpts

t_max = 80 # Higher Temperature
t_min = 25 # Lower Temperature
t_room = 20 # I considered this value as room temperature for the Newton Cooling Law

# === Name of the file without .csv ===
file_name = 'brick.ter'

# Some preparations
df = pd.read_csv(file_name + '.csv')
df.columns = ['Time','Res']

# === Number of Cycles ===
number_cycles = 5 

number_points = number_cycles * 3 + 1
number_waits = number_cycles

# Apply a Savitzky-Golay filter 
window_size = 200
polynomial_order = 2
df['Res_Fil'] = savgol_filter(df['Res'], window_size, polynomial_order)

# Verification of points in the loaded data
if os.path.isfile(file_name + '_points.csv'):
    steps = pd.read_csv(file_name + '_points.csv')
    steps = steps.values.tolist()
    steps_number = (len(steps)-1)/3

    if steps_number == number_cycles:
        # os.system('cls' if os.name == 'nt' else 'clear')
        print('-->FILE FOR POINTS FOUND<--')
    else:
        # os.system('cls' if os.name == 'nt' else 'clear')
        print('-->FILE FOR POINTS FOUND, BUT THE NUMBER OF POINTS DOES NOT MATCH THE NUMBER OF CYCLES. NEW POINTS WILL BE GENERATED <--')       
        # Plot to Select the Data
        plt.figure(figsize=(10, 6))
        plt.plot(df['Time'], df['Res_Fil'], '--',color='lightgray')
        points_get = plt.ginput(number_points, timeout=600)
        steps = cpts.cyclepoints(file_name, points_get)
        plt.close()
else:
        # os.system('cls' if os.name == 'nt' else 'clear')
        print('-->FILE FOR POINTS NOT FOUND. THEY WILL BE GENERATED<--') 
        # Plot to Select the Data
        plt.figure(figsize=(10, 6))
        plt.plot(df['Time'], df['Res_Fil'], '--',color='lightgray')
        points_get = plt.ginput(number_points, timeout=600)
        steps = cpts.cyclepoints(file_name, points_get)
        plt.close()

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
final_heating_data, heating_values = ht.heating(pairs_indexes_heating, df, number_cycles, t_min, t_max, t_room)
final_cooling_data, cooling_values = cl.cooling(pairs_indexes_cooling, df, number_cycles, t_min, t_max, t_room)

# Separate the Interval Data
separated_cycles = df[indexes_data[0]:indexes_data[-1]]
separated_cycles['Time'] = separated_cycles['Time'] - separated_cycles['Time'].iloc[0]

# Preparation for Plotting
# ir = separated_cycles['Res_Fil'].iloc[0]/1E3 # Initial Resistance
xh = final_heating_data['Temp']
yh = final_heating_data['Mean']/1E3
h_err = final_heating_data['STD']/1E3
xc = final_cooling_data['Temp']
yc = final_cooling_data['Mean']/1E3
c_err = final_cooling_data['STD']/1E3
ir = yh[0]
## GENERATING THE FIGURE

# ERROR FIGURE Resistance x Temperature
# Generate the Figure
fig, ax = plt.subplots(figsize=(4, 4))
# Plot the Figure as Error Bar
ax.errorbar(xh, (yh-ir)/ir, yerr=h_err/ir, fmt='-s', markersize=8, linewidth=2, elinewidth=1.8,capsize =5.5, capthick=1.8,color='red')
ax.errorbar(xc, (yc-ir)/ir, yerr=c_err/ir, fmt='-s',markersize=8, linewidth=2,elinewidth=1.8,capsize =5.5, capthick=1.8,color='blue')
# What x-ticks to show 
plt.xticks([25, 50, 75])
ax.yaxis.set_major_locator(ticker.MaxNLocator(nbins=8, prune=None))
# ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=5, prune=None))
# Show the number below in a mandatory way 
# plt.yticks(list(plt.yticks()[0]) + [0])
# Minor Ticks
# ax.xaxis.set_minor_locator(ticker.MultipleLocator(12.5))
ax.tick_params(axis='x', which='minor', direction='in', length=4,width=1.7)
# Margins
plt.margins(y=0.1)  # 10% margin in the y-axis
plt.margins(x=0.0)
# Major Ticks
plt.tick_params(direction='in', axis='both', length=7,width=1.7, bottom=True, top=True, left=True, right=True, labelsize=16)
# Labels
plt.xlabel('Temperature ($^\circ$C)',fontsize=18)
plt.ylabel('$\Delta R / R_{0}$',fontsize=18)
# Graph Title
plt.title(file_name)
# Linewidth of the frame
for spine in ['top', 'bottom', 'left', 'right']:
    ax.spines[spine].set_linewidth(1.7)
# Save the graph
fname = file_name+'.svg'
plt.savefig(fname, dpi=330, facecolor='w', edgecolor='w',
        orientation='portrait', format='svg',
        transparent=True)
plt.show()




fig, ax = plt.subplots(figsize=(4, 4))
ax.plot(separated_cycles['Time']/3600,((separated_cycles['Res_Fil']/1E3-ir)/ir), color='red', linewidth=2)
# Number of major ticks in the axis
ax.yaxis.set_major_locator(ticker.MaxNLocator(nbins=8, prune=None))
# ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=5, prune=None))
# Margins 
plt.margins(y=0.1)  # 10% margin in the y-axis
plt.margins(x=0.0)
# Ticks parameters
plt.tick_params(direction='in', axis='both', length=6,width=1.7, bottom=True, top=True, left=True, right=True, labelsize=16)
# Labels
plt.xlabel('Time (h)',fontsize=18)
plt.ylabel('$\Delta R / R_{0}$',fontsize=18)
# Title of the graph
plt.title(file_name)
# Linewidth of the framebox
for spine in ['top', 'bottom', 'left', 'right']:
    ax.spines[spine].set_linewidth(1.7)
#Save the file    
fname = file_name+'_cycle'+'.svg'
plt.savefig(fname, dpi=330, facecolor='w', edgecolor='w',
        orientation='portrait', format='svg',
        transparent=True)
plt.show()

# FIGURES FOR CONTROLLING THE DATA--NOT SAVED

plt.figure()
plt.plot(df['Time'],df['Res_Fil'], color='lightgray' )
for n in range(1,number_cycles+1):
    plt.plot(heating_values['T_'+str(n)], heating_values['C_'+str(n)], color='red')
    plt.plot(cooling_values['T_'+str(n)], cooling_values['C_'+str(n)], color='blue')
plt.show()

plt.figure()
for n in range(1,number_cycles+1):
    plt.plot(final_heating_data['Temp'], final_heating_data['R_'+str(n)],'-o')
    plt.legend('C_'+str(n))
    plt.title('HEATING')
    # plt.plot(cooling_values['T_'+str(n)], cooling_values['C_'+str(n)], color='blue')
plt.show()

plt.figure()
for n in range(1,number_cycles+1):
    plt.plot(final_cooling_data['Temp'], final_cooling_data['R_'+str(n)],'-o')
    plt.legend('C_'+str(n))
    plt.title('COOLING')
    # plt.plot(cooling_values['T_'+str(n)], cooling_values['C_'+str(n)], color='blue')
plt.show()
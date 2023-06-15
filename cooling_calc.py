import numpy as np
import pandas as pd

def cooling_calc(cooling_values, cycle,t_min, t_max, t_room):

    #cooling_values['T_'+str(cycle)] = cooling_values['T_'+str(cycle)] - cooling_values['T_'+str(cycle)].iloc[0]
    cooling_time_zero = cooling_values['T_'+str(cycle)] - cooling_values['T_'+str(cycle)].iloc[0]
    max_time_points = cooling_time_zero.count()
    total_time = cooling_time_zero.iloc[max_time_points-1]

    coef_1 = t_max-t_room
    coef_2 = np.log((t_min-t_room)/coef_1) * (1/total_time)
    time = np.linspace(0, total_time, max_time_points)
    temperatures = coef_1 * np.e**(coef_2*time) + t_room

    return temperatures
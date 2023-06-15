import numpy as np
import pandas as pd

def heating_calc(heating_values, cycle,t_min, t_max, t_room):

    heating_time_zero = heating_values['T_'+str(cycle)] - heating_values['T_'+str(cycle)].iloc[0]
    max_time_points = heating_time_zero.count()
    total_time = heating_time_zero.iloc[max_time_points-1]

    coef_1 = t_min-t_room
    coef_2 = np.log((t_max-t_room)/coef_1) * (1/total_time)
    time = np.linspace(0, total_time, max_time_points)
    temperatures = coef_1 * np.e**(coef_2*time) + t_room

    return temperatures
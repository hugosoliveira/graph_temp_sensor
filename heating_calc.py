import numpy as np
import pandas as pd

def heating_calc(heating_values, cycle,t_min, t_max, t_room):

    # heating_values = pd.read_csv('cooling.csv')
    heating_values['T_'+str(cycle)] = heating_values['T_'+str(cycle+1)] - heating_values['T_'+str(cycle+1)].iloc[0]
    max_time_points = heating_values['C_'+str(cycle+1)].count()
    total_time = heating_values['T_'+str(cycle+1)].iloc[max_time_points-1]

    coef_1 = t_min-t_room
    coef_2 = np.log((t_max-t_room)/coef_1) * (1/total_time)
    time = np.linspace(0, total_time, max_time_points)
    temperatures = coef_1 * np.e**(coef_2*time) + t_room

    return temperatures
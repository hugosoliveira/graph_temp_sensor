
import numpy as np
import pandas as pd
import cooling_calc as colc

def cooling(pairs_indexes_cooling, df, number_cycles,t_min,t_max,t_room):


    cooling_values = pd.DataFrame()

    for count in range(number_cycles):

        series = df['Res_Fil'].loc[pairs_indexes_cooling[count][0]:pairs_indexes_cooling[count][1]].values
        time = df['Time'].loc[pairs_indexes_cooling[count][0]:pairs_indexes_cooling[count][1]].values

        series = pd.DataFrame(series)
        time = pd.DataFrame(time)

        cooling_values = pd.concat([cooling_values, time], axis=1)
        cooling_values = pd.concat([cooling_values, series], axis=1)

    cooling_values.columns = ['{}_{}'.format(x, i) for i in range(1, number_cycles + 1) for x in ['T', 'C']]
    # cooling_values.to_csv('cooling.csv')
    # # Subtract the time to always start from zero
    # for col in heating_values.columns:
    #     if col.startswith('T_'):
    #         heating_values[col] = heating_values[col] - heating_values[col].iloc[0]

    # Insert the Temperature Values
    for cycle in range(1, number_cycles+1):
        
        # quantity_numbers = cooling_values['T_'+ str(i+1)].count()
        #Linear temperature Change
        # temperatures = pd.DataFrame(np.linspace(80, 25, quantity_numbers).tolist(), columns=['Temp_'+str(i+1)])
        temperatures = pd.DataFrame(colc.cooling_calc(cooling_values, cycle, t_min,t_max,t_room), columns=['Temp_'+str(cycle)])
        
       
        #insert_loc = cooling_values.columns.get_loc('T_' + str(cycle)) + 1

        df1 = cooling_values.iloc[:, :cooling_values.columns.get_loc('T_'+str(cycle))+1]
        df2 = cooling_values.iloc[:, cooling_values.columns.get_loc('T_'+str(cycle))+1:]
    
        cooling_values = pd.concat([df1, temperatures, df2], axis=1)
        cooling_values.to_csv('cooling_2.csv')

    # Final Cooling Data
    temperature_cooling = list(range(80, 24, -5))
    final_cooling_data = pd.DataFrame(columns=['Temp']+['R_{}'.format(i) for i in range(1,number_cycles + 1)])

    for temp in temperature_cooling:
        new_row = {'Temp': temp}
        for num in range(1, number_cycles+1):
            for i in range(cooling_values['Temp_' + str(num)].count()):
                if abs(cooling_values['Temp_' + str(num)].iloc[i] - temp) < 0.1:
                    new_row['R_' + str(num)] = cooling_values['C_' + str(num)].iloc[i]                    
        final_cooling_data = final_cooling_data._append(new_row, ignore_index=True)

    final_cooling_data['Mean'] = final_cooling_data.iloc[:, 1:].mean(axis=1)
    final_cooling_data['STD'] = final_cooling_data.iloc[:, 1:].std(axis=1)

    return final_cooling_data


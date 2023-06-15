
import numpy as np
import pandas as pd
import heating_calc as helc

def heating(pairs_indexes_heating, df, number_cycles,t_min,t_max,t_room):


    heating_values = pd.DataFrame()

    for count in range(number_cycles):

        series = df['Res_Fil'].loc[pairs_indexes_heating[count][0]:pairs_indexes_heating[count][1]].values
        time = df['Time'].loc[pairs_indexes_heating[count][0]:pairs_indexes_heating[count][1]].values

        series = pd.DataFrame(series)
        time = pd.DataFrame(time)

        heating_values = pd.concat([heating_values, time], axis=1)
        heating_values = pd.concat([heating_values, series], axis=1)

    heating_values.columns = ['{}_{}'.format(x, i) for i in range(1, number_cycles + 1) for x in ['T', 'C']]
    
    # # Subtract the time to always start from zero
    # for col in heating_values.columns:
    #     if col.startswith('T_'):
    #         heating_values[col] = heating_values[col] - heating_values[col].iloc[0]

    # Insert the Temperature Values
    for cycle in range(1, number_cycles+1):
        
        quantity_numbers = heating_values['T_'+ str(cycle)].count()
        #Linear temperature Changes -
        temperatures = pd.DataFrame(np.linspace(25, 80, quantity_numbers).tolist(), columns=['Temp_'+str(cycle)])
        # temperatures = pd.DataFrame(helc.heating_calc(heating_values, cycle, t_min,t_max,t_room), columns=['Temp_'+str(cycle)])
        
       
        #insert_loc = heating_values.columns.get_loc('T_' + str(cycle)) + 1

        df1 = heating_values.iloc[:, :heating_values.columns.get_loc('T_'+str(cycle))+1]
        df2 = heating_values.iloc[:, heating_values.columns.get_loc('T_'+str(cycle))+1:]
    
        heating_values = pd.concat([df1, temperatures, df2], axis=1)
        
    # Final heating Data
    temperature_heating = list(range(25, 81, 5))
    final_heating_data = pd.DataFrame(columns=['Temp']+['R_{}'.format(i) for i in range(1,number_cycles + 1)])

    for temp in temperature_heating:
        new_row = {'Temp': temp}
        for num in range(1, number_cycles+1):
            for i in range(heating_values['Temp_' + str(num)].count()):
                if abs(heating_values['Temp_' + str(num)].iloc[i] - temp) < 0.1:
                    new_row['R_' + str(num)] = heating_values['C_' + str(num)].iloc[i]
                    break                    
        final_heating_data = final_heating_data._append(new_row, ignore_index=True)
        print(final_heating_data)
    final_heating_data['Mean'] = final_heating_data.iloc[:, 1:].mean(axis=1)
    final_heating_data['STD'] = final_heating_data.iloc[:, 1:].std(axis=1)
    
    # print('heating')
    # print(heating_values)
    return final_heating_data, heating_values


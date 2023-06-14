import pandas as pd

def cyclepoints(file_name, points_get):

        # Organize the chosen data
        steps = [num[0] for num in points_get]
        steps = [round(num, 3) for num in steps]
        steps_df = pd.DataFrame(steps, columns = ['Points'])
        steps_df.to_csv(file_name + '_points.csv',index=False)
        return steps
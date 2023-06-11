from bokeh.plotting import figure, show, output_notebook
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.io import push_notebook
import pandas as pd

output_file("output.html")

# Name of the file
name_file = 'Limex.P.Ter.csv'

# Load the file in a dataframe
df = pd.read_csv(name_file)

df.columns = ['x','y']

# Assuming df is your dataframe and "x" and "y" are your columns.
source = ColumnDataSource(df)

TOOLTIPS = [
    ("index", "$index"),
    ("(x,y)", "($x, $y)"),
    ("desc", "@desc"),
]

# create a new plot with a title and axis labels
p = figure(title="simple line example", x_axis_label='x', y_axis_label='y', tooltips=TOOLTIPS)

# add a line renderer with legend and line thickness
p.circle('x', 'y', source=source)

# show the results
show(p)

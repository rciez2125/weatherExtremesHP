import pandas as pd
import numpy as np
import censusdata
from tabulate import tabulate
# adapted from https://towardsdatascience.com/mapping-us-census-data-with-python-607df3de4b9c

# make a plot of natural gas heating use for new york
#df = censusdata.download('acs5', 2019, censusdata.censusgeo([('state', '36'), ('county', '*')]), ['B25040_001E', 'B25040_001M', 'B25040_002E', 'B25040_002M'])
# state numbers are off (higher) by 4 from an alphabetical list ¯\_(ツ)_/¯
df = censusdata.download('acs5', 2019, censusdata.censusgeo([('state', '27'), ('county', '*')]), ['B25040_001E', 'B25040_001M', 'B25040_002E', 'B25040_002M'])
column_names = ['total_housing', 'housing_error', 'totalGas', 'gasError']
df.columns = column_names
#df.to_csv('nystatedata.csv')
df.to_csv('mnstatedata.csv')

df['percentGas'] = df.apply(lambda row: row['totalGas']/row['total_housing'], axis = 1)
new_indices = []
county_names = []

for index in df.index.tolist():
    new_index = index.geo[0][1] + index.geo[1][1]
    new_indices.append(new_index)
    county_name = index.name.split(',')[0]
    county_names.append(county_name)

df.index = new_indices
#df['tract_name'] = tract_names
df['county_name'] = county_names

import plotly.figure_factory as ff
fig = ff.create_choropleth(fips = df.index, scope = ['Minnesota'], values = df.percentGas.values, binning_endpoints=(0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9), title = 'Percentage of Homes with Natural Gas Heating Fuel', legend_title = 'Percentage using Natural Gas', simplify_county = 0.005)# colorscale = [[0, 'rgb(0,0,255)'], [1, 'rgb(255,0,0)']])
#fig = ff.create_choropleth(fips = df.index, scope = ['New York'], values = df.percentGas.values, binning_endpoints=(0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9), title = 'Percentage of Homes with Natural Gas Heating Fuel', legend_title = 'Percentage using Natural Gas', simplify_county = 0.005)# colorscale = [[0, 'rgb(0,0,255)'], [1, 'rgb(255,0,0)']])
fig.layout.template = None
fig.show()

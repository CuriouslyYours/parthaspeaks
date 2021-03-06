# -*- coding: utf-8 -*-
"""
Created on Sun May 24 22:01:53 2020

@author: Partha Chowdhury , email: partha2v@gmail.com , twitter: @yours_curiously
"""
# Import libraries
import pandas as pd
import numpy as np
import math

import geopandas as gpd
import json

from bokeh.io import output_notebook, show, output_file
from bokeh.plotting import figure
from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar, NumeralTickFormatter
from bokeh.palettes import brewer

from bokeh.io.doc import curdoc
from bokeh.models import Slider, HoverTool, Select
from bokeh.layouts import widgetbox, row, column

###---- Reading data directly from Govt. of India Website---- ######
tables = pd.read_html("https://www.mohfw.gov.in/")

### Cleaning imported tables
d1=tables[0]
#type(d1)  ##was just checking. such commmented code were required for recon

d1.iloc[:,1:5].tail(8)
d2=d1.copy()
d1.head(3)
#d2.head(3)
d2=d2.truncate(after=34) #WB position changing
d2.tail(3)
d2=d2.rename(columns={"Name of State / UT":"st_nm","Total Confirmed cases*":"Total_Cases","Cured/Discharged/Migrated*":"Recovered","Deaths**":"Deaths","Active Cases*":"ActiveCases"})
d2.head(3)
d2.to_csv('covid19_india.csv',index=False)

##### uncomment this part to craete html file
#output_file('covid19_india_v4.html')

###
#data_df_india=d2.copy()
data_df_india = pd.read_csv('data/covid19_india.csv')

#################

fp = r'data\india-polygon.shp'
sf_india = gpd.read_file(fp)
sf_india.head()
sf_india.columns
sf_india['st_nm']

#Merge the data file and shape file on the common column
merged = sf_india.merge(data_df_india, on = 'st_nm', how = 'left')
merged.head()
merged.columns

#Read data to json
merged_json = json.loads(merged.to_json())

#Convert to str like object
json_data = json.dumps(merged_json)
geosource= GeoJSONDataSource(geojson = json_data)

##############--------Total_Cases plot--------##############

#Define a sequential multi-hue color palette.
palette = brewer['YlGnBu'][9]
#Reverse color order so that dark blue is highest obesity.
palette = palette[::-1]
#Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors. Input nan_color.
color_mapper = LinearColorMapper(palette = palette, low = merged['Total_Cases'].min(), high = merged['Total_Cases'].max(), nan_color = '#d9d9d9')
#Define custom tick labels for color bar.
tick_labels = {'5000': '>5000'}

#Add hover tool
hover = HoverTool(tooltips = [ ('State','@st_nm'),('Cases','@Total_Cases')])
#Create color bar. 
color_bar = ColorBar(color_mapper=color_mapper, label_standoff=8,width = 500, height = 20,
                     border_line_color=None,location = (0,0), orientation = 'horizontal', major_label_overrides = tick_labels)
#Create figure object.
p3 = figure(title = 'Number of Covid-19 cases', plot_height = 800 , plot_width = 850, toolbar_location = None, tools = [hover])
p3.xaxis.visible = False
p3.yaxis.visible = False
p3.xgrid.grid_line_color = None
p3.ygrid.grid_line_color = None
#Add patch renderer to figure. 
p3.patches('xs','ys', source = geosource,fill_color = {'field' :'Total_Cases', 'transform' : color_mapper},
          line_color = 'black', line_width = 0.25, fill_alpha = 1)
#Specify layout
p3.add_layout(color_bar, 'below')

#Display plot
#show(p2)

##############--------End of Total_Cases plot--------##############

##############--------Death scenario plot--------##############

#Define a sequential multi-hue color palette.
palette2 = brewer['OrRd'][9]
#Reverse color order so that dark blue is highest obesity.
palette2 = palette2[::-1]
#Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors. Input nan_color.
color_mapper2 = LinearColorMapper(palette = palette2, low = merged['Deaths'].min(), high = merged['Deaths'].max(), nan_color = '#d9d9d9')
#Define custom tick labels for color bar.
tick_labels2 = {'5000': '>5000'}

#Add hover tool
hover2 = HoverTool(tooltips = [ ('State','@st_nm'),('Deaths','@Deaths')])
#Create color bar. 
color_bar2 = ColorBar(color_mapper=color_mapper2, label_standoff=8,width = 500, height = 20,
                     border_line_color=None,location = (0,0), orientation = 'horizontal', major_label_overrides = tick_labels2)


#Create figure object.
p4 = figure(title = 'Number of Covid-19 Deaths', plot_height = 800 , plot_width = 850, toolbar_location = None, tools = [hover2])
p4.xaxis.visible = False
p4.yaxis.visible = False
p4.xgrid.grid_line_color = None
p4.ygrid.grid_line_color = None
#Add patch renderer to figure. 
p4.patches('xs','ys', source = geosource,fill_color = {'field' :'Deaths', 'transform' : color_mapper2},
          line_color = 'black', line_width = 0.25, fill_alpha = 1)
#Specify layout
p4.add_layout(color_bar2, 'below')


##############--------End of Death scenario plot--------##############

##############--------Recovered scenario plot--------##############

#Define a sequential multi-hue color palette.
palette5 = brewer['BuGn'][9]
#Reverse color order so that dark blue is highest obesity.
palette5 = palette5[::-1]
#Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors. Input nan_color.
color_mapper5 = LinearColorMapper(palette = palette5, low = merged['Recovered'].min(), high = merged['Recovered'].max(), nan_color = '#d9d9d9')
#Define custom tick labels for color bar.
tick_labels5 = {'5000': '>5000'}

#Add hover tool
hover5 = HoverTool(tooltips = [ ('State','@st_nm'),('Recovered','@Recovered')])
#Create color bar. 
color_bar5 = ColorBar(color_mapper=color_mapper5, label_standoff=8,width = 500, height = 20,
                     border_line_color=None,location = (0,0), orientation = 'horizontal', major_label_overrides = tick_labels5)


#Create figure object.
p5 = figure(title = 'Number of Covid-19 Recovery', plot_height = 800 , plot_width = 850, toolbar_location = None, tools = [hover5])
p5.xaxis.visible = False
p5.yaxis.visible = False
p5.xgrid.grid_line_color = None
p5.ygrid.grid_line_color = None
#Add patch renderer to figure. 
p5.patches('xs','ys', source = geosource,fill_color = {'field' :'Recovered', 'transform' : color_mapper5},
          line_color = 'black', line_width = 0.25, fill_alpha = 1)
#Specify layout
p5.add_layout(color_bar5, 'below') 


##############--------End of Recovery plot--------##############

##############-------- Contri  of deaths--------##############

#Define a sequential multi-hue color palette.
# palette6 = brewer['OrRd'][9]
# #Reverse color order so that dark blue is highest obesity.
# palette6 = palette6[::-1]
# #Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors. Input nan_color.
# color_mapper6 = LinearColorMapper(palette = palette6, low = merged['contri_death'].min(), high = merged['contri_death'].max(), nan_color = '#d9d9d9')
# #Define custom tick labels for color bar.
# tick_labels6 = {'5000': '>5000'}

# #Add hover tool
# hover6 = HoverTool(tooltips = [ ('State','@st_nm'),('Contribution death%','@contri_death'),('Last Updated on','@Last_update')])
# #Create color bar. 
# color_bar6 = ColorBar(color_mapper=color_mapper6, label_standoff=8,width = 500, height = 20,
#                      border_line_color=None,location = (0,0), orientation = 'horizontal', major_label_overrides = tick_labels6)


# #Create figure object.
# p6 = figure(title = 'Contribution % to National Death toll', plot_height = 800 , plot_width = 850, toolbar_location = None, tools = [hover6])
# p6.xaxis.visible = False
# p6.yaxis.visible = False
# p6.xgrid.grid_line_color = None
# p6.ygrid.grid_line_color = None
# #Add patch renderer to figure. 
# p6.patches('xs','ys', source = geosource,fill_color = {'field' :'contri_death', 'transform' : color_mapper6},
#           line_color = 'black', line_width = 0.25, fill_alpha = 1)
# #Specify layout
# p6.add_layout(color_bar6, 'below') 



##############--------End of HBAR plot--------##############
#generate output file 

show(column(p3,p4,p5))
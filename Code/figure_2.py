#figure 2

from tkinter.tix import INTEGER
from tokenize import Double
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.gridspec as gridspec
import math


#This shouldn't need to change. If it's not working, double check the file is in the root folder of the repo.
figure_directory = "Figures"
data_directory = ".\Cleaned Data\Figure 2 Data Simplified and Cleaned.xlsx"
data = pd.read_excel(data_directory)

#This will be used to make our "Year Target" plots. Will become Circle, Square, and Upfacing Triangle respectively.
symbols = ['o','s','^']

#This is where we prep the data for plotting - don't know how usefull this loop is for figure 2. 
target_years = data['Target Year'].dropna().unique().astype(str)
target_years = target_years[1:]
iterations = 0

data['Target Percentile']=data['Target Percentile'].replace({50.0:'Average', 80.0:'Above\nAverage', 100.0:'Top\nPerformer'}) 
target_percentiles = data['Target Percentile'].dropna().unique().astype(str) #still has "None" values- how to get rid of?
target_percentiles = target_percentiles[1:]
iterations = 0
#Critical line of code needed to update the excel data. This will make the "50" "80" "100" become the new names we want "Average" "above..."

scenarios = data['Scenario'].unique()
scenarios = scenarios[1:]
#Use these colors, in this this order, for all figures representing the scenarios (BaU is #bdbdbd, specifically)
colors = ["#8c96c6","#8856a7","#810f7c"] 

Regions = sorted(data['Region'].dropna().unique().astype(str))
#This section makes the bars. 
fig = plt.figure(figsize=(22, 14))
subfigs = fig.subfigures(4, 3,wspace=0)
subfig = subfigs[2,0]
plt.subplots_adjust(wspace=0, hspace=.2)

region_iterations = 0
for Region in Regions:
    subfig = subfigs[math.trunc(region_iterations /3)][region_iterations % 3]
    inner = subfig.subplots(1,3)
    inner[0].yaxis.set_major_formatter(mtick.PercentFormatter(decimals=1))
    
    inner[0].set_xlabel(scenarios[0])
    inner[1].get_yaxis().set_visible(False)
    inner[1].set_xlabel(scenarios[1])
    inner[2].get_yaxis().set_visible(False)
    inner[2].set_xlabel(scenarios[2])
    region_data = data[data['Region'] == Region].dropna()
    region_min = min(region_data['Difference from BAU 2040'].unique())
    scenario_iterations = 0
    for scenario in scenarios:
        ax = inner[scenario_iterations % 3]
        scenario_data = region_data[region_data['Scenario'] == scenario]
        values = scenario_data['Difference between Scenario + Percentile Target Mean and BaU 2040'].unique() #We have three "Scenario + Percen..." values, we only need to plot one for each percentile + Scenario combination
        ax.set_ylim(region_min - .1, 0)
        ax.axhline(y=(sum(values)/len(values)), color="black", linestyle="--")
        ax.bar(target_percentiles, values,color= colors[scenario_iterations]) #Bar chart will be three bars. These are the average for the value in 2040 for the given scenario + percentile target combination.
        ax.tick_params(labelsize = 'small')
        #We now need to go to each percentile target, and plot its three year target values
        percentile_iterations = 0
        for percentile in target_percentiles:
            percentile_values = scenario_data[scenario_data["Target Percentile"] == percentile]
            #We need to plot each target year + target percentile + scenario value. This will the value in the year 2040, no extra math.
            for i in range(0, len(target_years)):
                values = percentile_values[percentile_values['Target Year'] == int(target_years[i])]
                values = values[values['Year'] == 2040]
                values = values['Difference from BAU 2040'].unique()
                ax.scatter(percentile_iterations,values,marker=symbols[i], color="gray", s = 60,edgecolors='black')
            percentile_iterations += 1
        scenario_iterations += 1
    subfig.suptitle(Region)
    region_iterations += 1
fig.suptitle("Percentage Point Reduction in Population Undernourishment, compared to BaU in 2040, by Scenario and Percentile Target")
fig.supylabel("Percentage Point Reduction in Undernourishment")
plt.savefig(figure_directory + "\\figure 2 Bars.svg", format="svg")

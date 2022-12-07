#figure 2

from tkinter.tix import INTEGER
from tokenize import Double
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.gridspec as gridspec
import math

#### CHANGE TO TRUE IF YOU ONLY WANT FIRST FIVE REGIONS ####
primary_regions_only = False
#### IF FALSE, IT WILL CREATE A FIGURE WITH ALL REGIONS ####

#This shouldn't need to change. If it's not working, double check the file is in the root folder of the repo.
figure_directory = "Figures"
data_directory = ".\Cleaned Data\Figure 2 Data Simplified and Cleaned Dec 2022.xlsx"
data = pd.read_excel(data_directory)

#This will be used to make our "Year Target" plots. Will become Circle, Square, and Upfacing Triangle respectively.
symbols = ['o','s','^']

#This is where we prep the data for plotting - don't know how usefull this loop is for figure 2. 
target_years = data['Target Year'].dropna().unique().astype(str)
target_years = target_years[1:]
iterations = 0

data['Target Percentile']=data['Target Percentile'].replace({50.0:'Average', 80.0:'Above\nAverage', 100.0:'Top\nPerformer'})
data['Scenario']=data['Scenario'].replace({'Business as Usual':'Business\nas Usual', 
                                            "Producing More Food":'Producing\nMore Food', 
                                            "Equal Food Distribution":'Equal\nFood Distribution', 
                                            "Raising average Caloric Consumption":"Raising\nCaloric Consumption"}) 
target_percentiles = data['Target Percentile'].dropna().unique().astype(str) #still has "None" values- how to get rid of?
target_percentiles = target_percentiles[1:]
iterations = 0
#Critical line of code needed to update the excel data. This will make the "50" "80" "100" become the new names we want "Average" "above..."

scenarios = data['Scenario'].unique()
#Use these colors, in this this order, for all figures representing the scenarios (BaU is #bdbdbd, specifically)
colors = ["#bdbdbd","#8c96c6","#8856a7","#810f7c"] 

Regions = sorted(data['Region'].dropna().unique().astype(str))
if primary_regions_only:
    Regions = Regions[:5]
#This section makes the bars. 
fig = plt.figure(figsize=(26, 22))
fig.suptitle("Prevalence of Undernourishment, in 2040, by Scenario and Percentile Target", fontsize = 20, y=1)
#fig.set_tight_layout(True)
subfigs = ""
if primary_regions_only:
    subfigs = fig.subfigures(2, 3)
else:
    subfigs = fig.subfigures(4, 3)
#subfig = subfigs[2,0]
fig.subplots_adjust(wspace=0, hspace=0, top=.85)
#fig.tight_layout(h_pad=.5, w_pad=.5)
#all_handles = ""
#all_labels = ""
region_iterations = 0
for Region in Regions:
    subfig = subfigs[math.trunc(region_iterations /3)][region_iterations % 3]
    inner = subfig.subplots(1,4)
    inner[0].yaxis.set_major_formatter(mtick.PercentFormatter(decimals=1))

    region_data = data[data['Region'] == Region].dropna()
    #region_min = min(region_data['Difference from BAU 2040'].unique())
    scenario_iterations = 0
    for scenario in scenarios:
        if scenario == scenarios[0]:
            ax = inner[0]
            scenario_data = region_data[region_data['Scenario'] == scenario]
            values = scenario_data['Average by Scenario and Percentile Target for the year 2040'].unique() #We have three "Scenario + Percen..." values, we only need to plot one for each percentile + Scenario combination
            ax.set_ylim(0,11)
            ax.bar(scenario, values,color= colors[scenario_iterations],label = scenario) #Bar chart will be three bars. These are the average for the value in 2040 for the given scenario + percentile target combination.
            ax.tick_params(labelsize = 'small')
        else:
            ax = inner[(scenario_iterations % 3)+1]
            scenario_data = region_data[region_data['Scenario'] == scenario]
            values = scenario_data['Average by Scenario and Percentile Target for the year 2040'].unique() #We have three "Scenario + Percen..." values, we only need to plot one for each percentile + Scenario combination
            ax.set_ylim(0,11)
            ax.axhline(y=scenario_data['Scenario Average for the year 2040'].unique(), color="black", linestyle="--", label = "Average Across Scenario")
            ax.bar(target_percentiles, values,color= colors[scenario_iterations], label = scenario) #Bar chart will be three bars. These are the average for the value in 2040 for the given scenario + percentile target combination.
            ax.tick_params(labelsize = 'small')
            #We now need to go to each percentile target, and plot its three year target values
            percentile_iterations = 0
            for percentile in target_percentiles:
                percentile_values = scenario_data[scenario_data["Target Percentile"] == percentile]
                #We need to plot each target year + target percentile + scenario value. This will the value in the year 2040, no extra math.
                for i in range(0, len(target_years)):
                    values = percentile_values[percentile_values['Target Year'] == int(target_years[i])]
                    values = values[values['Year'] == 2040]
                    values = values['Value'].unique()
                    ax.scatter(percentile_iterations,values,marker=symbols[i], color="gray", s = 60,edgecolors='black', label = "Target Year of: " + target_years[i])
                percentile_iterations += 1
        scenario_iterations += 1
    inner[0].set_ylabel("Prevalence of Undernourishment in 2040 (%)", x=.9)
    if region_iterations % 3 != 0:
        inner[0].get_yaxis().set_visible(False)
    if (math.trunc(region_iterations /3)):
        inner[0].get_xaxis().set_visible(False)
        inner[1].get_xaxis().set_visible(False)
        inner[2].get_xaxis().set_visible(False)
        inner[3].get_xaxis().set_visible(False)
    inner[1].get_yaxis().set_visible(False)
    inner[1].set_xlabel(scenarios[1])
    inner[2].get_yaxis().set_visible(False)
    inner[2].set_xlabel(scenarios[2])
    inner[3].get_yaxis().set_visible(False)
    inner[3].set_xlabel(scenarios[3])
    subfig.set_facecolor((0,0,0,0))
    subfig.align_labels()
    subfig.suptitle(Region, y=0.9)
    handles, labels = inner[0].get_legend_handles_labels()
    handles2, labels2 = inner[1].get_legend_handles_labels()
    handles3, labels3 = inner[2].get_legend_handles_labels()
    handles4, labels4 = inner[3].get_legend_handles_labels()
    handles = handles+ handles2
    handles.append(handles3[-1])
    handles.append(handles4[-1])
    handles.append(handles[0])
    handles.append(handles2[0])
    handles = handles[8:]
    labels = labels + labels2
    labels.append(labels3[-1])
    labels.append(labels4[-1])
    labels.append(labels[0])
    labels.append(labels2[0])
    labels = labels[8:]
    all_handles = handles
    all_labels = labels
   # if math.trunc(region_iterations /3) == 3 and region_iterations % 3 == 0:
        #inner[3].legend(handles,labels,bbox_to_anchor=(1,0), loc="center left")
    region_iterations += 1
fig.suptitle("Percentage Point Reduction in Population Undernourishment, compared to BaU in 2040, by Scenario and Percentile Target", x = 0.5, y = 1.03)
fig.supylabel("Percentage Point Reduction in Undernourishment")
#plt.savefig(figure_directory + "\\figure 2 Bars.svg", format="svg")
if primary_regions_only:
    subfigs[1][2].legend(handles, labels, loc = "center",prop={'size': 30})
    plt.savefig(figure_directory + "\\figure 2 Bars_main_regions.svg", format="svg", bbox_inches = 'tight',pad_inches=1)
    #plt.show()
else:
    subfigs[3][1].legend(handles, labels, loc = "center",prop={'size': 25})
    plt.savefig(figure_directory + "\\figure 2 Bars_all_regions.svg", format="svg", bbox_inches = 'tight',pad_inches=1)
    #plt.show()


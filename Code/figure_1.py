from cProfile import label
from tkinter.tix import INTEGER
from tokenize import Double
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.ticker as mtick


#This shouldn't need to change. If it's not working, double check the file is in the root folder of the repo.
figure_directory = "Figures"
data_directory = ".\Cleaned Data\Figure 1 Data.xlsx"
data = pd.read_excel(data_directory, sheet_name="Data in Years")

#This will be used to make our "Year Target" plots. Will become Circle, Square, and Upfacing Triangle respectively.
symbols = ['o','s','^']

#This is where we prep the data for plotting.
target_years = data['Target Year'].dropna().unique().astype(str)
iterations = 0
for year in target_years:
    target_years[iterations] = year.replace(".0", "")
    iterations += 1
data['Percentile Target']=data['Percentile Target'].replace({50.0:'Average', 80.0:'Above\nAverage', 100.0:'Top\nPerformer'}) 
target_percentiles = data['Percentile Target'].dropna().unique().astype(str)
iterations = 0
#Critical line of code needed to update the excel data. This will make the "50" "80" "100" become the new names we want "Average" "above..."

#The if statements we talked about changing, is not needed. The above will make our values in the df now be 

scenarios = data['Scenario'].unique()
scenarios = scenarios[4:8]
#Use these colors, in this this order, for all figures representing the scenarios (BaU is #bdbdbd, specifically)
colors = ["#8c96c6","#8856a7","#810f7c"] 

#This section makes the bars. We will edit here to be "(1,5, figsize.... '={width_rations:[6,1,3,3,3]})"
fig, axs = plt.subplots(1,5, figsize=(17,7), constrained_layout=True, gridspec_kw={'width_ratios': [6,1,3,3,3]}) 

#BAU needs special treatment (we now want axs[1] to be BaU, so it comes after the line graph)
scenario_data = data[data['Scenario'] == scenarios[0]] #Filter to only the BaU data
value = scenario_data['2040'] #We only care about the 2040 value, because we have no averages for it. There's only one BaU outcome.
axs[1].bar(" ", value,color= "#bdbdbd")
axs[1].set_xlabel(scenarios[0])
axs[1].set_ylabel("Prevalence of Undernourishment in 2040") #This is the only bar chart that gets a y-axis. It will be uniform for the following three bar charts.
axs[1].set_ylim(top=8) #Change this if the bars have way too much whitespace above, or don't fit. New data may cause that.
axs[1].yaxis.set_major_formatter(mtick.PercentFormatter(decimals=1))

axs[3].set_title("Prevalence of Undernourishment in 2040 by Scenario and Percentile Target") #This title could go further left, or right, depending on what lets it fit + not be over the line graph

axs[3].set_title("Prevalence of Undernourishment in 2040 \nby Scenario and Percentile Target") #This title could go further left, or right, depending on what lets it fit + not be over the line graph


#We need to track how many scenarios we have gone thorugh
iterations = 0
for scenario in scenarios:
    if scenario != scenarios[0]: #Skip BaU, it's special.
        scenario_data = data[data['Scenario'] == scenario]
        values = scenario_data['Scenario + Percentile Target Average Outcome'].unique() #We have three "Scenario + Percen..." values, we only need to plot one for each percentile + Scenario combination
        values = values[1:] #Drop an NA
        axs[iterations+2].bar(target_percentiles, values,color= colors[iterations]) #Bar chart will be three bars. These are the average for the value in 2040 for the given scenario + percentile target combination.
        percentile_iterations = 0
        axs[iterations+2].tick_params(labelsize = 'medium') #Can use small font or labelrotation = 45 if these are still overlapping.
        #We now need to go to each percentile target, and plot its three year target values
        for percentile in target_percentiles:
            percentile_values = scenario_data[scenario_data["Percentile Target"] == percentile]
            #We need to plot each target year + target percentile + scenario value. This will the value in the year 2040, no extra math.
            for i in range(0, len(target_years)):
                value = percentile_values[percentile_values['Target Year'] == float(target_years[i])]
                axs[iterations+2].scatter(percentile_iterations,value['2040'],marker=symbols[i], color="gray", s = 60,edgecolors='black',label = "Target Year of: " + target_years[i])
            percentile_iterations += 1
        
        #Give the figure its scenario data (name, scenario average)
        axs[iterations+2].set_xlabel(scenario)
        axs[iterations+2].axhline(y=(sum(values)/len(values)), color="black", linestyle="--",label="Average Across Scenario")
        #Make it match BaU's y-axis
        axs[iterations+2].set_ylim(top=8)
        #Hide the y-axis, since it shares with BaU
        axs[iterations+2].get_yaxis().set_visible(False)
        iterations += 1

#plt.savefig(figure_directory + "figure 1 Bars.svg", format="svg")
#plt.clf()
#Make the Line Graph Here (This will now be figure axs[0]). Keeping this code after the bar charts is fine, don't need to move this, just make sure it's in the same 1x5 subplot as the 0th figure.
colors = ["#bdbdbd","#8c96c6","#8856a7","#810f7c"] #Use these colors, in this this order, for all figures representing the scenarios (BaU is #bdbdbd, specifically)

data = pd.read_excel(data_directory, sheet_name="Data_unpivoted")
data = data[data['Scenario'].isin(scenarios)]
data = data[data['Target Year'].isna() == True]
data = data.loc[:,['Scenario','Year','Value']]
iterations = 0
#Go through each scenario, and plot its data from 2017 -> 2040
for scenario in scenarios:
    scenario_data = data[data['Scenario'] == scenario]
    axs[0].plot(scenario_data['Year'], scenario_data['Value'], color=colors[iterations], linewidth = 4,label=scenario) #will need to change plt -> axs[0]
    iterations += 1
axs[0].yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
axs[0].set_xlabel("Year")
axs[0].set_ylabel("% of Population")
axs[0].set_title("Prevalence of Global Undernourishment")
axs[0].set_ylabel("Prevalence of Undernourishment")
axs[0].set_title("Prevalence of Undernourishment by Scenario Over Time")
axs[0].set_ylim(0,8)
handles, labels = axs[0].get_legend_handles_labels()
handles2,labels2 = axs[4].get_legend_handles_labels()
handles= handles + handles2[0:3]
labels = labels + labels2[0:3]
handles.append(handles2[9])
labels.append(labels2[9])
axs[4].legend(handles, labels,bbox_to_anchor=(1, 1))
fig.align_xlabels()
plt.savefig(figure_directory + "figure 1 Line + Bar.svg", format="svg", bbox_inches="tight") #This will become the only save fig with the changes mentioned in the TODO section
axs[4].legend(handles, labels,bbox_to_anchor=(1.05, 1))
fig.align_xlabels()
plt.savefig(figure_directory + "figure 1 Line + Bar.svg", format="svg", bbox_inches="tight") #This will become the only save fig with the changes mentioned in the TODO section


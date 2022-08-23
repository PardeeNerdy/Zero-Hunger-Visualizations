from tkinter.tix import INTEGER
from tokenize import Double
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.ticker as mtick

figure_directory = "./Figures/"

data_directory = "./Cleaned Data/Figure 1 Data.xlsx"
data = pd.read_excel(data_directory, sheet_name="Data in Years")

symbols = ['o','s','^']

target_years = data['Target Year'].dropna().unique().astype(str)
iterations = 0
for year in target_years:
    target_years[iterations] = year.replace(".0", "")
    iterations += 1

target_percentiles = data['Percentile Target'].dropna().unique().astype(str)
iterations = 0
for percentile in target_percentiles:
    target_percentiles[iterations] = percentile.replace(".0", "th")
    iterations += 1

scenarios = data['Scenario'].unique()
scenarios = scenarios[4:8]

#Make Bars
colors = ["#8c96c6","#8856a7","#810f7c"]
#Get all three values to plot onto bar by scenario
scenario_data = data[data['Scenario'] == 'BaU']
value = scenario_data['2040']
fig, axs = plt.subplots(1,4, figsize=(10,5), constrained_layout=True, gridspec_kw={'width_ratios': [1, 3,3,3]})
axs[0].bar(" ", value,color= "#bdbdbd")
axs[0].set_xlabel('BaU')
axs[0].set_ylabel("Percent of Global Population Malnourished in 2040")
axs[0].set_ylim(top=3.5)
axs[0].yaxis.set_major_formatter(mtick.PercentFormatter(decimals=1))

axs[2].set_title("Percent of Global Population Undernourised in 2040 by Scenario and Percentile Target")
iterations = 0
for scenario in scenarios:
    if scenario != "BaU":
        scenario_data = data[data['Scenario'] == scenario]
        values = scenario_data['Scenario + Percentile Target Average Outcome'].unique()
        values = values[1:]
        axs[iterations+1].bar(target_percentiles, values,color= colors[iterations])
        percentile_iterations = 0
        for percentile in target_percentiles:
            percentile = percentile.replace("th", "")
            percentile_values = scenario_data[scenario_data["Percentile Target"] == float(percentile)]
            for i in range(0,3):
                value = percentile_values[percentile_values['Target Year'] == float(target_years[i])]
                axs[iterations+1].scatter(percentile_iterations,value['2040'],marker=symbols[i], color="gray", s = 60,edgecolors='black')
                
            percentile_iterations += 1
            
        axs[iterations+1].set_xlabel(scenario)
        axs[iterations+1].axhline(y=(sum(values)/len(values)), color="black", linestyle="--")
        axs[iterations+1].set_ylim(top=3.5)
        axs[iterations+1].get_yaxis().set_visible(False)
        iterations += 1
axs[3].legend(target_years,title="Target Year")
plt.savefig(figure_directory + "figure 1 Bars.svg", format="svg")
plt.clf()

colors = ["#bdbdbd","#8c96c6","#8856a7","#810f7c"]
data = pd.read_excel(data_directory, sheet_name="Data_unpivoted")
data = data[data['Scenario'].isin(scenarios)]
data = data[data['Target Year'].isna() == True]
data = data.loc[:,['Scenario','Year','Value']]
iterations = 0
fig, ax = plt.subplots(figsize=(8, 6))
for scenario in scenarios:
    scenario_data = data[data['Scenario'] == scenario]
    plt.plot(scenario_data['Year'], scenario_data['Value'], color=colors[iterations], linewidth = 4)
    iterations += 1
plt.legend(scenarios, title="Scenario")
ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
ax.set_xlabel("Year")
ax.set_ylabel("Percent of Global Population Malnourished")
ax.set_title("Percent of Global Population Undernourised by Scenario Over Time")
plt.savefig(figure_directory + "figure 1 Line.svg", format="svg")
    #percentile_averages = data.loc[data['Scenario'], ['Scenario + Percentile Target Average Outcome']]

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerLine2D
from matplotlib import colors as mcolors
import random

file = 'hnp_stats_csv/HNP_StatsData.csv'
hn_reader = pd.read_csv(file)
colors = list(mcolors.CSS4_COLORS.keys())
tick = [1960, 1970, 1980, 1990, 2000, 2010, 2017]


def create_single_country_indicator_plot(indicator_name, *args):
    """Generates plots using world bank's data health and nutrition indicators (csv file) by
    country code and indicator name. Multiple country codes can be passed. Plots are created separately.
    Plots have to be dismissed or saved in order to generate the next country plot"""
    for arg in args:
        country = hn_reader[hn_reader['Country Code'] == arg]
        indicator = country[country['Indicator Name'] == indicator_name]
        labels = list(indicator)
        data = list(indicator.values)
        arg, = plt.plot(labels[4:62], data[0][4:62], color='green', marker='o', linestyle='solid', linewidth=1,
                        markersize=4, label=arg)
        plt.legend(handler_map={arg: HandlerLine2D(numpoints=1)})
        plt.xlabel('Year')
        plt.ylabel(indicator_name)
        plt.xticks(tick, tick)
        plt.show()


def create_multiple_country_indicator_plot(indicator_name, *args):
    """Generates plots using world bank's data health and nutrition indicators (csv file) by
    country code and indicator name. We can pass multiple country codes. Plots are created upon the same chart"""
    for arg in args:
        country = hn_reader[hn_reader['Country Code'] == arg]
        indicator = country[country['Indicator Name'] == indicator_name]
        labels = list(indicator)
        data = list(indicator.values)
        arg, = plt.plot(labels[4:62], data[0][4:62], color=random.choice(colors), marker='o', linestyle='solid', linewidth=1,
                        markersize=4, label=arg)
        plt.legend(handler_map={arg: HandlerLine2D(numpoints=1)})
        plt.xlabel('Year')
        plt.ylabel(indicator_name)
        plt.xticks(tick, tick)
    plt.show()
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerLine2D
from matplotlib import colors as mcolors
import random

file = 'hnp_stats_csv/HNP_StatsData.csv'
hn_reader = pd.read_csv(file)
hn_reader_countries = pd.read_csv(file, skiprows=range(1, 15710), na_values=0)
colors = list(mcolors.CSS4_COLORS.keys())


def create_single_country_indicator_plot(indicator_name, *args):
    """Generates line diagram using world bank's data health and nutrition indicators (csv file) by
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
        plt.xticks([1960, 1970, 1980, 1990, 2000, 2010, 2017])
        plt.show()


def create_multiple_country_indicator_plot(indicator_name, *args):
    """Generates line diagram using world bank's data health and nutrition indicators (csv file) by
    country code and indicator name. We can pass multiple country codes. Plots are created upon the same chart"""
    for arg in args:
        country = hn_reader[hn_reader['Country Code'] == arg]
        indicator = country[country['Indicator Name'] == indicator_name]
        labels = list(indicator)
        data = list(indicator.values)
        arg, = plt.plot(labels[4:62], data[0][4:62], color=random.choice(colors), marker='o', linestyle='solid',
                        linewidth=1, markersize=4, label=arg)
        plt.legend(handler_map={arg: HandlerLine2D(numpoints=1)})
        plt.xlabel('Year')
        plt.ylabel(indicator_name)
        plt.xticks(tick)
    plt.show()


def create_3D_indicator_scatter(x_axis, y_axis, z_axis, year, size_prime_factor):
    """Generates scatter diagram using world bank's data health and nutrition indicators (csv file).
     z_axis refers to circles size"""
    ind1 = hn_reader_countries[hn_reader_countries['Indicator Name'] == x_axis][year]
    ind2 = hn_reader_countries[hn_reader_countries['Indicator Name'] == y_axis][year]
    ind3 = hn_reader_countries[hn_reader_countries['Indicator Name'] == z_axis][year]
    # TODO: legend country name and population
    country_name = hn_reader_countries[hn_reader_countries['Indicator Name'] ==
                                       'GNI per capita, Atlas method (current US$)']['Country Name']
    x, y, s = list(ind1), list(ind2), [x/size_prime_factor for x in list(ind3)]
    plt.scatter(x, y, s=s)
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    plt.title('Data extracted from WB ' + year)
    plt.show()


def create_population_pyramid(country, year):
    """Generates population pyramid by country and year using world bank's data health and
    nutrition indicators (csv file) """
    # TODO: put *args instead of country into function arguments
    all_data = pd.DataFrame(hn_reader)
    required_rows = all_data.filter(items=['Country Name', 'Indicator Name', year])
    required_rows.set_index('Indicator Name', inplace=True)
    female_data, male_data = required_rows.filter(like="Female population"
                                                       "", axis=0), required_rows.filter(like='Male population', axis=0)
    female_data['indicator'] = female_data.index
    female_data.index, male_data.index = pd.RangeIndex(start=0, stop=4403, step=1), \
                                         pd.RangeIndex(start=0, stop=4403, step=1)
    female_data.rename(columns={year: 'female'}, inplace=True)
    male_data.rename(columns={year: 'male'}, inplace=True)
    del male_data['Country Name']
    pyramid_data = pd.concat([female_data, male_data], axis=1, join_axes=[female_data.index])
    pyramid_data = pyramid_data[['indicator', 'Country Name', 'female', 'male']]
    pyramid_data['indicator'] = pyramid_data['indicator'].apply(lambda x: x[17:])
    pyramid_data_by_country = pyramid_data[pyramid_data['Country Name'] == country]
    p1 = plt.barh(pyramid_data_by_country['indicator'], pyramid_data_by_country['female']*(-1), color="red")
    p2 = plt.barh(pyramid_data_by_country['indicator'], pyramid_data_by_country['male'], color="blue")
    plt.legend((p1[0], p2[0]), ('Female', 'Male'))
    plt.xticks([-2000000, -1000000, 0, 1000000, 2000000], [2, 1, 0, 1, 2])
    plt.xlabel('Population (in millions)')
    plt.ylabel('Age ranges')
    plt.title("Population pyramid " + country + " " + year)
    plt.show()

def create_indicator_histogram(indicator, year, *args, bins=None, row_width=0.8, sample=None):
    all_data = pd.DataFrame(hn_reader)
    result = pd.DataFrame()
    for arg in args:
        country = all_data[all_data['Country Code'] == arg]
        ind = country[country['Indicator Name'] == indicator]
        ind_df = ind[year].to_frame()
        result = result.append(ind_df)
    plt.hist(result.round(decimals=2), bins=bins, range=(result.min(), result.max()), rwidth=row_width)
    plt.title(sample + ' ' + indicator + ' ' + year)
    plt.xlabel('World Bank indicators database')
    plt.show()
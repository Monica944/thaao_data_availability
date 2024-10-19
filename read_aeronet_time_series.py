# -*- coding: utf-8 -*-
"""read_aeronet_time_series.ipynb

Automatically generated by Colab. Modified by Filippo Calì Quaglia Oct 2024

Original file is located at
    https://colab.research.google.com/drive/13V4WAnA6dhQR1o2pHXZA0Wm2-H5Xk498

- **Module:** read_aeronet_time_series.ipynb
- **Authors:** Petar Grigorov and Pawan Gupta
- **Organization:** NASA AERONET (https://aeronet.gsfc.nasa.gov/)
- **Date:** 07/03/2023
- **Last Revision:** 07/29/2024
- **Purpose:** Time-series analysis of AERONET sites AOD levels
- **Disclaimer:** The code is for demonstration purposes only. Users are responsible to check for accuracy and revise to fit their objective.
- **Contact:** Report any concern or question related to the code to pawan.gupta@nasa.gov or petar.t.grigorov@nasa.gov
- **Readme:** https://github.com/pawanpgupta/AERONET/blob/Python/README/Read_AERONET_TimeSeries

**Required packages installation and importing**
"""
#
# !pip uninstall -y numpy pandas
# !pip install numpy==1.26.4 pandas==2.0.3
# !pip install beautifulsoup4
# !pip install requests
# !pip install calplot

import calplot  # for creating heat maps
import datetime  # for time data manipulation
import math  # useful math operations
import matplotlib.dates as mdates  # for converting datetime to numeric
import matplotlib.pyplot as plt  # for creating plots
import numpy as np  # for array manipulation
import os
import pandas as pd  # for data querying and processing
import re  # regular expression matching operations (RegEx)
import requests  # useful for sending HTTP requests
import warnings
from bs4 import BeautifulSoup  # reads data from website (web scraping)
from collections import Counter  # for keeping track of unique data

import thaao_settings as ts

warnings.filterwarnings('ignore')

"""**Connecting and mounting local drive onto colab notebook**"""

# from google.colab import files      #ensures output zip file can be downloaded
# from google.colab import drive      #imports local google drive
# drive.mount('/drive')               #mounts local google drive onto colab
# !mkdir Output_TimeSeries            #makes directory where output files will be stored

"""**Setup input parameters such as date, data level, averaging type, AOD range for mapping, AOD/Angstrom exponent, and geographical limits**"""

instr = 'aeronet'
date_list = pd.date_range(
        ts.instr_na_list[instr]['start_instr'], ts.instr_na_list[instr]['end_instr'], freq='D').tolist()
folder = os.path.join(ts.basefolder, "thaao_" + instr)
site = 'Thule'  # Please make sure site name is spelled properly
dt_initial = ts.instr_na_list[instr]['start_instr'].strftime('%Y%m%d')  # starting date YYYYMMDD format
dt_final = ts.instr_na_list[instr]['end_instr'].strftime('%Y%m%d')  # final date YYYYMMDD format
level = 1.5  # AERONET data level
average_type = 1  # daily (1), monthly (2)
feature_choice = 1  # Enter '1' if you are specifying an AOD wavelength or '2' if you are specifying an Angstrom exponent
wavelength = 500  # Available choices: 1640, 1020, 870, 865, 779, 675, 667, 620, 560, 555, 551, 532, 531, 510, 500, 490, 443, 440, 412, 400, 380, 340
Angstrom_exp = '440-675'  # Available choices: '440-870','380-500','440-675','500-870','340-440','440-675(Polar)'

if __name__ == "__main__":
    """**Get desired AERONET data using web services, then scraping data from website**"""

    yr_initial = dt_initial[:4]  # initial year
    mon_initial = dt_initial[4:6]  # initial month
    day_initial = dt_initial[6:]  # initial day

    yr_final = dt_final[:4]  # final year
    mon_final = dt_final[4:6]  # final month
    day_final = dt_final[6:]  # final day

    if level == 1 or level == 1.0:
        level = 10
    elif level == 1.5:
        level = 15
    elif level == 2 or level == 2.0:
        level = 20
    else:
        print("\nIncorrect input for data level type. Defaulting to level 1.5...")
        level = 15

    if level == 20 and int(
            yr_initial) == datetime.date.today().year:  # if user wants level 2 data for the current year, program alerts that data may not be available
        level = 15  # defaults to level 1.5 data
        print("\nThere is no level 2 data available for the current year. Defaulting to level 1.5 data...")

    url = 'https://aeronet.gsfc.nasa.gov/cgi-bin/print_web_data_v3?site=' + site + '&year=' + yr_initial + '&month=' + mon_initial + '&day=' + day_initial + '&year2=' + yr_final + '&month2=' + mon_final + '&day2=' + day_final + '&AOD' + str(
            level) + '=1&AVG=20'
    soup = BeautifulSoup(requests.get(url).text)  # web services contents are read here from URL

    """**Writes soup data to text file, assigns contents to Pandas dataframe, prepares data for plotting**"""
    with open(
            os.path.join(ts.basefolder, 'thaao_aeronet', 'temp.txt'),
            "w") as oFile:  # writes the data scraped from "beautiful soup" to a text file on your local Google drive
        oFile.write(str(soup.text))
        oFile.close()

    df = pd.read_csv(
            os.path.join(ts.basefolder, 'thaao_aeronet', 'temp.txt'),
            skiprows=6)  # loads the csv data into a Pandas dataframe

    if len(df) > 0:
        df = df.replace(-999.0, np.nan)  # replaces all -999.0 vakyes with NaN; helps with accurate data aggregation
        df[['Day', 'Month', 'Year']] = df['Date(dd:mm:yyyy)'].str.split(
                ':', expand=True)  # splits the date column and then joins it back together using "-" instead of ":"
        df['Date'] = df[['Year', 'Month', 'Day']].apply(
                lambda x: '-'.join(x.values.astype(str)),
                axis="columns")  # because datetime format in python does not recognize colons
        df['Date'] = pd.to_datetime(df['Date'])  # converts the new date column to datetime format
    else:
        print("No data to parse. Please retry with different parameters.")

    aeronet = pd.DataFrame(columns=['dt', 'mask'])
    for i in date_list:
        if i in df['Date'].values:
            aeronet.loc[i] = [i, True]
    ts.save_txt(instr, aeronet)

    """**AOD Wavelength or Angstrom Exponent Selection**"""

    AOD_col = [col for col in df.columns if
               'AOD_' in col and 'nm' in col]  # list of AOD columns, used for mapping user input to them
    AOD_col = [item for item in AOD_col if 'N[' not in item]
    Ang_exp_col = [col for col in df.columns if
                   'Angstrom_Exponent' in col]  # list of Angstrom Exponent columns, used for mapping user input to them
    Ang_exp_col = [item for item in Ang_exp_col if 'N[' not in item]

    AOD_val = [int(re.search(r'\d+', col).group()) for col in AOD_col]  # expected user input choices for AOD
    Ang_exp_val = [item.split('_')[0] for item in Ang_exp_col]  # expected user input choices for AE
    Ang_exp_val[-1] += '(Polar)'  # manually adds the polar channel to the list

    if feature_choice == 1:
        if wavelength in AOD_val:  # if user input for AOD wavelength matches a value in the list, code proceeds forward. Otherwise it prompts user to try again
            for i in range(len(AOD_col)):
                if wavelength == AOD_val[
                    i]:  # code scans the list of columns and list of possible values, and matches user input to the appropriate column name
                    df = df[['Date', 'Day_of_Year', AOD_col[
                        i]]]  # if a match exists, the column name is matched to the actual column and it is then appended to the dataset
        else:
            df = df[['Date', 'Day_of_Year', 'AOD_500nm']]
            print("\nInput for AOD wavelength is not in list. Defaulting to 500nm...")
    elif feature_choice == 2:
        if Angstrom_exp in Ang_exp_val:  # if user input for Angstrom Exponent matches a value in the list, code proceeds forward. Otherwise it prompts user to try again
            for i in range(len(Ang_exp_col)):
                if Angstrom_exp == Ang_exp_val[
                    i]:  # code scans the list of columns and list of possible values, and matches user input to the appropriate column nam
                    df = df[['Date', 'Day_of_Year', Ang_exp_col[
                        i]]]  # if a match exists, the column name is matched to the actual column and it is then appended to the dataset
        else:
            df = df[['Date', 'Day_of_Year', '440-675']]
            print("\nInput for Angstrom Exponent is not in list. Defaulting to 440-675...")
    else:
        feature_choice == 1
        print("\nIncorrect input for feature choice. Defaulting to AOD wavelength (1)...")
        if wavelength in AOD_val:  # if user input for AOD wavelength matches a value in the list, code proceeds forward. Otherwise it prompts user to try again
            for i in range(len(AOD_col)):
                if wavelength == AOD_val[
                    i]:  # code scans the list of columns and list of possible values, and matches user input to the appropriate column name
                    df = df[['Date', 'Day_of_Year', AOD_col[
                        i]]]  # if a match exists, the column name is matched to the actual column and it is then appended to the dataset
        else:
            df = df[['Date', 'Day_of_Year', 'AOD_500nm']]
            print("\nInput for AOD wavelength is not in list. Defaulting to 500nm...")

    df = df.dropna().reset_index(drop=True)  # Drops NaN or -999.0 values
    df

    """**Time-series analysis**"""

    if average_type == 2:
        df = df.groupby(pd.PeriodIndex(df['Date'], freq="M")).mean().reset_index()

    plot = df.plot('Date', df.columns[-1], title="Site: " + str(site), figsize=(16, 8))
    plt.scatter(df['Date'], df[df.columns[-1]])  # superimposed scatter plot of points, in addition to the line graph
    plt.ylabel(df.columns[-1].replace('_', ' '))
    plot.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Set the x-axis format to display dates
    fig = plot.get_figure()
    fig.savefig('/content/Output_TimeSeries/TimeSeries_' + str(site) + '.png')  # saves figure
    plt.show()

    """**Tile Map of Time Series**"""

    if average_type == 1:
        df[['Year', 'Month', 'Day']] = df['Date'].astype(str).str.split('-', expand=True)
        df['Month'] = df['Month'].astype(int)
        num_missing_months = 12 - len(set(df['Month'].to_list()))
        df = df.drop(columns=['Month', 'Day'])
        df['Year'] = df['Year'].astype(int)

        # Extracting year, month, and values from the data
        years = df['Year'].to_list()
        num_missing_years = max(years) - min(years) + 1 - len(set(years))
        days = df['Day_of_Year'].to_list()
        months = np.arange(1, 13, 1).tolist()
        values = df.iloc[:, 2].to_list()

        # Creating a 2D matrix to represent the heatmap
        heatmap = np.zeros((max(years) - min(years) + 1, max(days)))

        # Populating the heatmap with values
        for i in range(len(df)):
            year_index = years[i] - min(years)
            day_index = days[i] - 1
            heatmap[year_index, day_index] = values[i]

        # assign all zeroes (missing values) in heatmap matrix as NaN so that matplotlib set_bad function can work
        num_rows, num_cols = heatmap.shape
        for i in range(num_rows):
            for j in range(num_cols):
                if heatmap[i, j] == 0.0:
                    heatmap[i, j] = 'NaN'

        # Plotting the heatmap
        plt.rcParams["figure.figsize"] = [18, 8]
        ax = plt.subplot()
        current_cmap = plt.cm.get_cmap('RdYlGn_r')
        current_cmap.set_bad(color='white')
        current_cmap.set_extremes(under='gray', over='magenta')
        plt.imshow(heatmap, cmap=current_cmap, interpolation='nearest', aspect='auto', vmin=0, vmax=1.0)
        plt.colorbar(label=df.columns[2], extend='both')
        month_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
        plt.xticks(np.arange(0, 365, 31), month_labels)
        plt.yticks(np.arange(len(Counter(years).keys()) + num_missing_years), np.arange(min(years), max(years) + 1))
        plt.title('Site: ' + str(site), size=12)
        plt.savefig('/content/Output_TimeSeries/TilePlot_Daily_' + str(site) + '.png')
        plt.show()

    elif average_type == 2:
        df[['Year', 'Month']] = df['Date'].astype(str).str.split('-', expand=True)
        df['Year'] = df['Year'].astype(int)
        df['Month'] = df['Month'].astype(int)

        # Extracting year, month, and values from the data
        years = df['Year'].to_list()
        num_missing_years = max(years) - min(years) + 1 - len(set(years))
        months = df['Month'].to_list()
        values = df.iloc[:, 2].to_list()

        # Creating a 2D matrix to represent the heatmap
        heatmap = np.zeros((max(years) - min(years) + 1, max(months)))

        # Populating the heatmap with values
        for i in range(len(df)):
            year_index = years[i] - min(years)
            month_index = months[i] - 1
            heatmap[year_index, month_index] = values[i]

        # assign all zeroes (missing values) in heatmap matrix as NaN so that matplotlib set_bad function can work
        num_rows, num_cols = heatmap.shape
        for i in range(num_rows):
            for j in range(num_cols):
                if heatmap[i, j] == 0.0:
                    heatmap[i, j] = 'NaN'

        # Plotting the heatmap
        plt.rcParams["figure.figsize"] = [12, 8]
        ax = plt.subplot()
        current_cmap = plt.cm.get_cmap('RdYlGn_r')
        current_cmap.set_bad(color='white')
        current_cmap.set_extremes(under='gray', over='magenta')
        plt.imshow(heatmap, cmap=current_cmap, interpolation='nearest', aspect='auto')
        plt.colorbar(label=df.columns[2], extend='both')
        plt.xticks(np.arange(len(Counter(months).keys())), np.arange(1, len(Counter(months).keys()) + 1))
        plt.yticks(np.arange(len(Counter(years).keys()) + num_missing_years), np.arange(min(years), max(years) + 1))
        ax.set_xticklabels(
                ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec'], fontsize=10)
        plt.title('Site: ' + str(site), size=12)
        plt.savefig('/content/Output_TimeSeries/TilePlot_Monthly_' + str(site) + '.png')
        plt.show()

    """**Calendar plot of Time series (Daily averages only)**"""

    if average_type == 1:
        df_cal = df.set_index('Date')
        df_cal.index = pd.DatetimeIndex(df_cal.index)
        df_cal = df_cal.reindex(pd.date_range(df['Date'].min(), df['Date'].max()), fill_value=0)

        current_cmap = plt.cm.get_cmap('RdYlGn_r')
        current_cmap.set_extremes(under='white', over='magenta')

        fig, ax = calplot.calplot(
                df_cal[df_cal.columns[1]], edgecolor='black', linewidth=2, colorbar=False,
                suptitle="Site: " + str(site), suptitle_kws={'size': 11, 'weight': 'bold'}, cmap=current_cmap,
                vmin=df[df.columns[2]].min(), vmax=1)

        fig.colorbar(
                ax[0].get_children()[1], ax=ax.ravel().tolist(), extend='both', orientation='horizontal', aspect=50,
                pad=0.03, label=df_cal.columns[1])

        plt.savefig('/content/Output_TimeSeries/CalendarPlot_Daily_' + str(site) + '.png', bbox_inches='tight')

    """**Annual variability plot (Daily averages only)**"""

    if average_type == 1:
        df_annual = df[['Year', df.columns[2]]]  # isolates year and AOD columns to new dataframe
        df_annual = pd.merge(
                df_annual, df_annual.groupby(['Year']).size().reset_index().rename(
                        columns={0: "Count"}))  # counts total number of yearly data
        df_annual = df_annual[df_annual.Count >= 30]  # filters out years with less than 30 measurements
        df_annual = df_annual.drop(columns=['Count']).reset_index(
                drop=True)  # drops Count column after filtering dataset

        if len(df_annual['Year'].unique()) > 1:
            df_sigma = df_annual.groupby(
                    ['Year']).std().reset_index()  # takes standard deviation of AOD measurements per year
            df_sigma = df_sigma.rename(
                    columns={df.columns[2]: df.columns[2] + str('_sigma')})  # assigns standard deviation column name
            df_miu = df_annual.groupby(['Year']).mean().reset_index()  # takes average of AOD measurements per year
            df_miu = df_miu.rename(columns={df.columns[2]: df.columns[2] + str('_miu')})  # assigns mean AOD column name

            df_statistics = pd.merge(
                    df_sigma, df_miu)  # merges yearly average and standard deviation of AOD measurements
            df_statistics['Upper'] = df_statistics[df_statistics.columns[2]] + df_statistics[
                df_statistics.columns[1]]  # Upper bound of shaded region
            df_statistics['Lower'] = df_statistics[df_statistics.columns[2]] - df_statistics[
                df_statistics.columns[1]]  # Lower bound of shaded region

            plt.style.use('dark_background')  # set dark background
            plt.plot(
                    df_statistics['Year'], df_statistics[df_statistics.columns[2]], color='white', linewidth=3,
                    label='Actual Data')  # creates line plot of Year vs average yearly measurement
            plt.fill_between(
                    df_statistics['Year'],
                    df_statistics[df_statistics.columns[2]] - df_statistics[df_statistics.columns[1]],
                    df_statistics[df_statistics.columns[2]] + df_statistics[df_statistics.columns[1]], color='yellow',
                    alpha=0.8)  # plot standard deviation
            plt.scatter(
                    df_statistics['Year'], df_statistics[df_statistics.columns[2]], color='white',
                    s=150)  # superimposed scatter plot to show data as dots
            p = np.poly1d(
                    np.polyfit(
                            df_statistics['Year'], df_statistics[df_statistics.columns[2]],
                            1))  # calculates 1st order trendline
            plt.plot(
                    df_statistics['Year'], p(df_statistics['Year']), color='red', linewidth=3, linestyle='dashed',
                    label='Linear Regression')  # plots trendline
            plt.xticks(
                    np.arange(df_statistics['Year'].min(), df_statistics['Year'].max() + 1, 1.0), fontsize=14,
                    rotation=30, ha='center')  # adjust xticks
            plt.yticks(
                    np.arange(
                            int(df_statistics['Lower'].min() * 10) / 10.0,
                            math.ceil(df_statistics['Upper'].max() * 10) / 10.0, 0.025), fontsize=14)  # adjust yticks
            plt.xlabel('Year', size=16, fontweight="bold")  # adjust xlabel size name and font
            plt.ylabel(df.columns[2].replace('_', ' '), size=16, fontweight="bold")  # adjust ylabel size name and font
            plt.title(
                    "Annual AOD Averages for " + str(site) + " Site with 1 Standard Deviation", size=18,
                    fontweight="bold")  # sets graph title
            # plt.text(x = df_annual['Year'].min(), y = df_statistics['Upper'].max(), s = 'Y(Linear) ='+str(p))
            # +'\nR2 ='+str(r2_score(p(df_statistics['Year']), df_statistics[df_statistics.columns[2]]).round(3))+'\n\nY(Lasso) = '+str(p_lasso)+'\nR2 ='+str(r2_score(p_lasso(Predicted_Lasso['Year']), df_statistics[df_statistics.columns[2]]).round(3)), ha='left', va='top',fontsize=16) #displays trendline and R2 value
            plt.legend()  # displays legend
            plt.savefig('/content/Output_TimeSeries/AnnualAOD_Averages_' + str(site) + '.png')  # saves figure as png
            plt.show()  # display graph

    """**Download the saved time series plot as png file**"""

    # while True:  #     zip_download = str(input("Would you like to download your output in a zipped folder (y or n)?: "))  #     if zip_download == 'y' or zip_download == 'Y' or zip_download == 'Yes' or zip_download == 'yes':  #         shutil.make_archive('Output_TimeSeries', 'zip', '/content/Output_TimeSeries')  # zips all output files  #         files.download('Output_TimeSeries.zip')  # Note: Must use Chrome browser for download to work  #         break  #     elif zip_download == 'n' or zip_download == 'N' or zip_download == 'No' or zip_download == 'no':  #         break  #     else:  #         print("\nIncorrect input. Please try again!")

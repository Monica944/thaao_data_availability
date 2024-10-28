#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
#
"""
https://github.com/NASAARSET/GEMS_AQ
https://colab.research.google.com/drive/13V4WAnA6dhQR1o2pHXZA0Wm2-H5Xk498
"""

# =============================================================
# CREATED:
# AFFILIATION: INGV
# AUTHORS: Filippo Cali' Quaglia
# =============================================================
#
# -------------------------------------------------------------------------------
__author__ = "Filippo Cali' Quaglia"
__credits__ = ["??????"]
__license__ = "GPL"
__version__ = "0.1"
__email__ = "filippo.caliquaglia@ingv.it"
__status__ = "Research"
__lastupdate__ = "October 2024"

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

import datetime  # for time data manipulation
import os

import numpy as np  # for array manipulation
import pandas as pd  # for data querying and processing
import requests  # useful for sending HTTP requests
from bs4 import BeautifulSoup  # reads data from website (web scraping)

import thaao_settings as ts

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

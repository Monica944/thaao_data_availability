#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
#
"""
Brief description
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
__lastupdate__ = ""

import datetime as dt
import os

basefolder = os.path.join("H:\\Shared drives", "Dati")
da_folder = os.path.join(basefolder, 'thaao_data_availability')

instr_list = ['uv-vis_spec', 'lidar_ae', 'o3_sondes', 'aero_sondes', 'rs_sondes', 'gbms', 'wv_isotopes', 'metar',
              'vespa', 'ceilometer', 'hatpro', 'dir_rad_trkr', 'pm10', 'ftir', 'aeronet', 'ecapac_mrr',
              # 'ecapac_aws_snow', 'ecapac_disdro_precip', 'ecapac_aws', 'aws(p,T,RH)', 'mms_trios', 'lidar_temp',
              # 'skycam', 'gnss', 'macmap_seismometer_1', 'macmap_seismometer_2', 'macmap_seismometer_3',
              # 'macmap_seismometer_4', 'macmap_tide_gauge', 'rad_uli', 'rad_usi', 'rad_dli', 'rad_dsi', 'rad_tb',
              'rad_par_up', 'rad_par_down']

# switches
switch_campaigns = ''  # Draw field campaigns?
switch_all = ''  # Plot full panels?
switch_history = ''  # Draw historical events?
switch_yearly = ''  # Plot single-year panels?
switch_prog_bar = ''  # Draw progress bar?
switch_gif = ''  # Plot panels for gif?

# inputs
start_a = ''
end_a = ''
time_freq_a = ''

start_y = ''
end_y = ''

start_c = ''
end_c = ''
time_freq_c = ''
time_window_c = ''

# consider when instruments are not available and when there are not the conditions (i.e., sun)
instr_metadata = {'metar': {'institution': 'U.Alaska,Florence,StonyBrook/USSF', 'start_instr': dt.datetime(1951, 10, 1),
                            'end_instr'  : dt.datetime.today(), 'start_seas': dt.datetime(1900, 1, 1),
                            'end_seas'   : dt.datetime(1900, 12, 31)},
                  'vespa': {'institution': 'INGV', 'start_instr': dt.datetime(2016, 7, 1),
                            'end_instr'  : dt.datetime.today(), 'start_seas': dt.datetime(1900, 1, 1),
                            'end_seas'   : dt.datetime(1900, 12, 31)},
                  'ceilometer': {'institution': 'ENEA', 'start_instr': dt.datetime(2019, 11, 1),
                                 'end_instr'  : dt.datetime.today(), 'start_seas': dt.datetime(1900, 1, 1),
                                 'end_seas'   : dt.datetime(1900, 12, 31)},
                  'hatpro': {'institution': 'ENEA', 'start_instr': dt.datetime(2017, 1, 1),
                             'end_instr'  : dt.datetime(2024, 6, 30), 'start_seas': dt.datetime(1900, 1, 1),
                             'end_seas'   : dt.datetime(1900, 12, 31)},
                  'dir_rad_trkr': {'institution': 'DMI+ENEA', 'start_instr': dt.datetime(2002, 10, 1),
                                   'end_instr'  : dt.datetime.today(), 'start_seas': dt.datetime(1900, 2, 1),
                                   'end_seas'   : dt.datetime(1900, 10, 31)},
                  'pm10': {'institution': 'U.Alaska,Florence,StonyBrook/USSF', 'start_instr': dt.datetime(2010, 1, 1),
                           'end_instr'  : dt.datetime.today(), 'start_seas': dt.datetime(1900, 1, 1),
                           'end_seas'   : dt.datetime(1900, 12, 31)},
                  'ecapac_mrr': {'institution': 'ENEA', 'start_instr': dt.datetime(2022, 9, 1),
                                 'end_instr'  : dt.datetime.today(), 'start_seas': dt.datetime(1900, 1, 1),
                                 'end_seas'   : dt.datetime(1900, 12, 31)},
                  'ecapac_aws_snow': {'institution': 'ENEA', 'start_instr': dt.datetime(2022, 9, 1),
                                      'end_instr'  : dt.datetime.today(), 'start_seas': dt.datetime(1900, 1, 1),
                                      'end_seas'   : dt.datetime(1900, 12, 31)},
                  'ecapac_disdro_precip': {'institution': 'ENEA', 'start_instr': dt.datetime(2022, 9, 1),
                                           'end_instr'  : dt.datetime.today(), 'start_seas': dt.datetime(1900, 1, 1),
                                           'end_seas'   : dt.datetime(1900, 12, 31)},
                  'rs_sondes': {'institution': 'DMI+INGV', 'start_instr': dt.datetime(1973, 1, 1),
                                'end_instr'  : dt.datetime.today(), 'start_seas': dt.datetime(1900, 1, 1),
                                'end_seas'   : dt.datetime(1900, 12, 31)},
                  'o3_sondes': {'institution': 'DMI', 'start_instr': dt.datetime(1991, 12, 1),
                                'end_instr'  : dt.datetime(2016, 12, 31), 'start_seas': dt.datetime(1900, 1, 1),
                                'end_seas'   : dt.datetime(1900, 12, 31)},
                  'aero_sondes': {'institution': 'DMI', 'start_instr': dt.datetime(1992, 1, 1),
                                  'end_instr'  : dt.datetime(1998, 12, 31), 'start_seas': dt.datetime(1900, 1, 1),
                                  'end_seas'   : dt.datetime(1900, 12, 31)},
                  'rad_tb': {'institution': 'ENEA', 'start_instr': dt.datetime(2017, 1, 1),
                             'end_instr'  : dt.datetime.today(), 'start_seas': dt.datetime(1900, 1, 1),
                             'end_seas'   : dt.datetime(1900, 12, 31)},
                  'skycam': {'institution': 'ENEA', 'start_instr': dt.datetime(2017, 2, 1),
                             'end_instr'  : dt.datetime.today(), 'start_seas': dt.datetime(1900, 1, 1),
                             'end_seas'   : dt.datetime(1900, 12, 31)},
                  'gnss': {'institution': 'INGV', 'start_instr': dt.datetime(2021, 5, 1),
                           'end_instr'  : dt.datetime.today(), 'start_seas': dt.datetime(1900, 1, 1),
                           'end_seas'   : dt.datetime(1900, 12, 31)},
                  'rad_uli': {'institution': 'ENEA', 'start_instr': dt.datetime(2016, 7, 1),
                              'end_instr'  : dt.datetime.today(), 'start_seas': dt.datetime(1900, 1, 1),
                              'end_seas'   : dt.datetime(1900, 12, 31)},
                  'rad_usi': {'institution': 'ENEA', 'start_instr': dt.datetime(2016, 7, 1),
                              'end_instr'  : dt.datetime.today(), 'start_seas': dt.datetime(1900, 1, 1),
                              'end_seas'   : dt.datetime(1900, 12, 31)},
                  'rad_dli': {'institution': 'ENEA', 'start_instr': dt.datetime(2009, 1, 1),
                              'end_instr'  : dt.datetime.today(), 'start_seas': dt.datetime(1900, 1, 1),
                              'end_seas'   : dt.datetime(1900, 12, 31)},
                  'rad_dsi': {'institution': 'DMI+ENEA', 'start_instr': dt.datetime(2003, 2, 1),
                              'end_instr'  : dt.datetime.today(), 'start_seas': dt.datetime(1900, 1, 1),
                              'end_seas'   : dt.datetime(1900, 12, 31)},
                  'wv_isotopes': {'institution': 'U.Alaska,Florence,StonyBrook/USSF',
                                  'start_instr': dt.datetime(2017, 8, 1), 'end_instr': dt.datetime(2019, 12, 31),
                                  'start_seas' : dt.datetime(1900, 1, 1), 'end_seas': dt.datetime(1900, 12, 31)},
                  'macmap_seismometer_1': {'institution': 'INGV', 'start_instr': dt.datetime(2021, 8, 1),
                                           'end_instr'  : dt.datetime.today(), 'start_seas': dt.datetime(1900, 3, 1),
                                           'end_seas'   : dt.datetime(1900, 11, 30)},
                  'macmap_seismometer_2': {'institution': 'INGV', 'start_instr': dt.datetime(2021, 8, 1),
                                           'end_instr'  : dt.datetime.today(), 'start_seas': dt.datetime(1900, 3, 1),
                                           'end_seas'   : dt.datetime(1900, 11, 30)},
                  'macmap_seismometer_3': {'institution': 'INGV', 'start_instr': dt.datetime(2021, 8, 1),
                                           'end_instr'  : dt.datetime.today(), 'start_seas': dt.datetime(1900, 3, 1),
                                           'end_seas'   : dt.datetime(1900, 11, 30)},
                  'macmap_seismometer_4': {'institution': 'INGV', 'start_instr': dt.datetime(2022, 9, 1),
                                           'end_instr'  : dt.datetime.today(), 'start_seas': dt.datetime(1900, 3, 1),
                                           'end_seas'   : dt.datetime(1900, 11, 30)},
                  'macmap_tide_gauge': {'institution': 'INGV', 'start_instr': dt.datetime(2021, 8, 1),
                                        'end_instr'  : dt.datetime.today(), 'start_seas': dt.datetime(1900, 3, 1),
                                        'end_seas'   : dt.datetime(1900, 11, 30)},
                  'mms_trios': {'institution': 'INGV', 'start_instr': dt.datetime(2021, 9, 1),
                                'end_instr'  : dt.datetime.today(), 'start_seas': dt.datetime(1900, 3, 1),
                                'end_seas'   : dt.datetime(1900, 10, 31)},
                  'ftir': {'institution': 'NCAR', 'start_instr': dt.datetime(1999, 10, 1),
                           'end_instr'  : dt.datetime.today(), 'start_seas': dt.datetime(1900, 3, 1),
                           'end_seas'   : dt.datetime(1900, 10, 31)},
                  'aeronet': {'institution': 'NCAR', 'start_instr': dt.datetime(2007, 3, 1),
                              'end_instr'  : dt.datetime.today(), 'start_seas': dt.datetime(1900, 3, 1),
                              'end_seas'   : dt.datetime(1900, 10, 31)},
                  'aws(p,T,RH)': {'institution': 'ENEA+INGV', 'start_instr': dt.datetime(2017, 9, 1),
                                  'end_instr'  : dt.datetime.today(), 'start_seas': dt.datetime(1900, 9, 1),
                                  'end_seas'   : dt.datetime.today()},
                  'lidar_temp': {'institution': 'U.Sap+ENEA', 'start_instr': dt.datetime(1993, 11, 1),
                                 'end_instr'  : dt.datetime.today(), 'start_seas': dt.datetime(1900, 11, 1),
                                 'end_seas'   : dt.datetime(1900, 3, 31)},
                  'lidar_ae': {'institution': 'U.Sap+ENEA', 'start_instr': dt.datetime(1991, 9, 1),
                               'end_instr'  : dt.datetime(1996, 3, 31), 'start_seas': dt.datetime(1900, 9, 1),
                               'end_seas'   : dt.datetime(1900, 3, 31)},
                  'uv-vis_spec': {'institution': 'DMI', 'start_instr': dt.datetime(1991, 2, 1),
                                  'end_instr'  : dt.datetime(2016, 11, 30), 'start_seas': dt.datetime(1900, 2, 1),
                                  'end_seas'   : dt.datetime(1900, 11, 30)},
                  'gbms': {'institution': 'U.Alaska,Florence,StonyBrook/USSF', 'start_instr': dt.datetime(1992, 1, 1),
                           'end_instr'  : dt.datetime(2012, 12, 31), 'start_seas': dt.datetime(1900, 1, 1),
                           'end_seas'   : dt.datetime(1900, 12, 31)},
                  'rad_par_up': {'institution': 'ENEA', 'start_instr': dt.datetime(2016, 7, 1),
                                 'end_instr'  : dt.datetime.today(), 'start_seas': dt.datetime(1900, 1, 1),
                                 'end_seas'   : dt.datetime(1900, 12, 31)},
                  'rad_par_down': {'institution': 'ENEA', 'start_instr': dt.datetime(2016, 7, 1),
                                   'end_instr'  : dt.datetime.today(), 'start_seas': dt.datetime(1900, 1, 1),
                                   'end_seas'   : dt.datetime(1900, 12, 31)}}

institution_colors = {'DMI'                              : 'green', 'INGV': 'blue', 'ENEA': 'red', 'NCAR': 'purple',
                      'ENEA+INGV'                        : 'olive', 'U.Sap+ENEA': 'brown', 'DMI+INGV': 'orange',
                      'DMI+ENEA'                         : 'pink', 'U.Alaska,Florence,StonyBrook/USSF': 'black',
                      'not active'                       : 'grey'}

events_dict = {15: {'date': dt.datetime(1903, 3, 30), 'label': 'Danish Literary \n Expedition'},
               8 : {'date': dt.datetime(1910, 6, 30), 'label': 'Thule Outpost'},
               9 : {'date': dt.datetime(1912, 6, 30), 'label': "First (of 7) Rasmussen's \n Expeditions"},
               12: {'date': dt.datetime(1914, 7, 28), 'label': 'WW I starts'},
               13: {'date': dt.datetime(1918, 11, 11), 'label': 'WW I ends'},
               30: {'date': dt.datetime(1928, 5, 24), 'label': 'U. Nobile above \n North Pole'},
               31: {'date': dt.datetime(1932, 6, 30), 'label': 'Second IPY'},
               11: {'date': dt.datetime(1933, 3, 30), 'label': 'Thule Outpost under \n the Danish Gov. control'},
               21: {'date': dt.datetime(1939, 9, 1), 'label': 'WW II starts'},
               53: {'date': dt.datetime(1941, 6, 30), 'label': 'Bluie West Program \n starts'},
               36: {'date': dt.datetime(1943, 6, 30), 'label': 'Bluie West 6 \n Met Station'},
               5 : {'date': dt.datetime(1945, 9, 2), 'label': 'WW II ends'},
               51: {'date': dt.datetime(1947, 1, 30), 'label': 'DMI Geomagnetic Obs'},
               3 : {'date': dt.datetime(1951, 6, 6), 'label': 'TAB installation \n starts'},
               4 : {'date': dt.datetime(1951, 10, 1), 'label': 'TAB installation \n ends'},
               23: {'date': dt.datetime(1953, 3, 30), 'label': 'Op. IceCap'},
               39: {'date': dt.datetime(1953, 6, 30), 'label': 'Greenland ex-Danish \n colony'},
               52: {'date': dt.datetime(1953, 6, 30), 'label': 'Pituffik inhabitants \n relocated to Qaanaaq'},
               42: {'date': dt.datetime(1954, 6, 30), 'label': 'DEW line \n building'},
               37: {'date': dt.datetime(1954, 12, 1), 'label': 'DMI takes over \n the Bluie West 6 \n Met Station'},
               32: {'date': dt.datetime(1957, 6, 30), 'label': 'Third IPY'},
               18: {'date': dt.datetime(1958, 3, 30), 'label': 'Camp Century \n construction'},
               22: {'date': dt.datetime(1958, 3, 30), 'label': 'Op. Chrome \n Dome '},
               14: {'date': dt.datetime(1959, 3, 30), 'label': 'First NSF prj \n in Thule funded'},
               19: {'date': dt.datetime(1961, 3, 30), 'label': 'BMEWS \n construction'},
               20: {'date': dt.datetime(1966, 3, 30), 'label': 'Camp Century \n abandoned'},
               16: {'date': dt.datetime(1968, 1, 21), 'label': 'B-52 crash'},
               35: {'date': dt.datetime(1972, 6, 30), 'label': 'DMI lab \n @bldg. #1985 ?'},
               27: {'date': dt.datetime(1981, 3, 18), 'label': 'Italy signs \n the Antarctic Treaty'},
               25: {'date': dt.datetime(1982, 3, 29), 'label': 'El Chichón eruption'},
               38: {'date': dt.datetime(1985, 6, 30), 'label': 'Greenland \n exits CEE'},
               6 : {'date': dt.datetime(1989, 9, 1), 'label': 'Berlin Wall falls'},
               33: {'date': dt.datetime(1990, 6, 30), 'label': 'IT lidar \n @bldg. #216 \n @TAB'},
               24: {'date': dt.datetime(1991, 6, 15), 'label': 'Mt. Pinatubo \n eruption'},
               7 : {'date': dt.datetime(1991, 11, 12), 'label': 'I was born :)'},
               29: {'date': dt.datetime(1997, 6, 30), 'label': 'CNR "Dirigibile Italia" \n station'},
               17: {'date': dt.datetime(2007, 3, 1), 'label': 'Fourth IPY --> APECS!'},
               34: {'date': dt.datetime(2010, 6, 30), 'label': 'IT lidar --> \n bldg. #1971@S.Mount.'},
               1 : {'date': dt.datetime(2012, 6, 30), 'label': 'bldg. #1985 --> \n bldg. #1971'},
               41: {'date': dt.datetime(2012, 6, 30), 'label': 'IT Observatory Status \n @ Arctic Council'},
               28: {'date': dt.datetime(2013, 6, 30), 'label': 'PRA'},
               50: {'date': dt.datetime(2014, 6, 30), 'label': 'ARCA prj \n MIUR 2y'},
               49: {'date': dt.datetime(2015, 6, 30), 'label': 'SVAAP prj \n PNRA 1y'},
               48: {'date': dt.datetime(2016, 6, 30), 'label': 'OASIS-YOPP prj \n PNRA 2y'},
               44: {'date': dt.datetime(2019, 5, 14), 'label': 'CLARA2 prj \n PNRA 3y'},
               43: {'date': dt.datetime(2020, 2, 1), 'label': 'COVID hits'},
               45: {'date': dt.datetime(2020, 6, 30), 'label': 'MACMAP prj \n INGV 3y'},
               46: {'date': dt.datetime(2021, 1, 4), 'label': 'ECAPAC prj \n PRA 2y'},
               47: {'date': dt.datetime(2021, 6, 30), 'label': 'SEANA prj \n ext 2y'},
               40: {'date': dt.datetime(2023, 4, 6), 'label': 'Greenland National \n Research Strategy \n Plan'},
               10: {'date': dt.datetime(2023, 4, 6), 'label': 'TAB --> PSB'},
               54: {'date': dt.datetime(2024, 6, 1), 'label': 'NASA ARCSIX'},
               55: {'date': dt.datetime(2024, 6, 1), 'label': 'THAAO funded as \n INGV infrastructure'},
               2 : {'date': dt.datetime.today(), 'label': 'today'}}

campaigns_dict = {1 : {'start': dt.datetime(1991, 1, 1), 'end': dt.datetime(1991, 1, 31)},
                  2 : {'start': dt.datetime(1991, 12, 1), 'end': dt.datetime(1991, 12, 31)},
                  3 : {'start': dt.datetime(1992, 1, 1), 'end': dt.datetime(1992, 1, 31)},
                  4 : {'start': dt.datetime(1992, 11, 1), 'end': dt.datetime(1992, 11, 30)},
                  5 : {'start': dt.datetime(1993, 1, 1), 'end': dt.datetime(1993, 1, 31)},
                  6 : {'start': dt.datetime(1993, 7, 1), 'end': dt.datetime(1993, 7, 31)},
                  7 : {'start': dt.datetime(1994, 1, 1), 'end': dt.datetime(1994, 1, 31)},
                  8 : {'start': dt.datetime(1994, 7, 1), 'end': dt.datetime(1994, 7, 31)},
                  9 : {'start': dt.datetime(1995, 1, 1), 'end': dt.datetime(1995, 1, 31)},
                  10: {'start': dt.datetime(1997, 1, 1), 'end': dt.datetime(1997, 1, 31)},
                  11: {'start': dt.datetime(1998, 5, 1), 'end': dt.datetime(1998, 5, 31)},
                  12: {'start': dt.datetime(2002, 1, 1), 'end': dt.datetime(2002, 1, 31)},
                  13: {'start': dt.datetime(2003, 1, 1), 'end': dt.datetime(2003, 1, 31)},
                  14: {'start': dt.datetime(2006, 12, 1), 'end': dt.datetime(2006, 12, 31)},
                  15: {'start': dt.datetime(2009, 1, 1), 'end': dt.datetime(2009, 1, 31)},
                  16: {'start': dt.datetime(2010, 1, 1), 'end': dt.datetime(2010, 1, 31)},
                  17: {'start': dt.datetime(2010, 10, 1), 'end': dt.datetime(2010, 10, 31)},
                  18: {'start': dt.datetime(2012, 1, 1), 'end': dt.datetime(2012, 2, 29)},
                  19: {'start': dt.datetime(2013, 2, 21), 'end': dt.datetime(2013, 3, 18)},
                  20: {'start': dt.datetime(2014, 1, 1), 'end': dt.datetime(2014, 2, 28)},
                  21: {'start': dt.datetime(2016, 6, 11), 'end': dt.datetime(2016, 7, 18)},
                  22: {'start': dt.datetime(2017, 2, 16), 'end': dt.datetime(2017, 2, 21)},
                  23: {'start': dt.datetime(2018, 2, 22), 'end': dt.datetime(2018, 3, 2)},
                  24: {'start': dt.datetime(2019, 2, 27), 'end': dt.datetime(2019, 3, 8)},
                  25: {'start': dt.datetime(2019, 11, 6), 'end': dt.datetime(2019, 11, 15)},
                  26: {'start': dt.datetime(2021, 4, 21), 'end': dt.datetime(2021, 5, 21)},
                  27: {'start': dt.datetime(2021, 8, 10), 'end': dt.datetime(2021, 8, 27)},
                  28: {'start': dt.datetime(2022, 3, 22), 'end': dt.datetime(2022, 4, 9)},
                  29: {'start': dt.datetime(2022, 9, 7), 'end': dt.datetime(2022, 9, 23)},
                  30: {'start': dt.datetime(2023, 4, 18), 'end': dt.datetime(2023, 5, 6)},
                  31: {'start': dt.datetime(2023, 9, 26), 'end': dt.datetime(2023, 10, 5)},
                  32: {'start': dt.datetime(2024, 3, 19), 'end': dt.datetime(2024, 4, 6)},
                  33: {'start': dt.datetime(2024, 5, 25), 'end': dt.datetime(2024, 6, 17)},
                  34: {'start': dt.datetime(2024, 7, 22), 'end': dt.datetime(2024, 8, 7)},
                  36: {'start': dt.datetime(2024, 9, 26), 'end': dt.datetime(2024, 10, 5)}, }

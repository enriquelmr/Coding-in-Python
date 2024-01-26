import pandas as pd
import numpy as np
import datetime
import math as ma
import matplotlib.dates as mdates
import matplotlib
import matplotlib.pyplot as plt
import os
from mpl_toolkits.axes_grid.inset_locator import inset_axes
from sklearn.linear_model import LinearRegression
from collections import OrderedDict
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math as ma
import matplotlib.dates as mdates
from pathlib import Path
from datetime import datetime, timedelta, time
import os
import glob
from sklearn.linear_model import LinearRegression


station="KWS1M"

def handle_data(station):
    station_id=station
    pd.set_option("display.max_rows",None,"display.max_columns", None)
    station_datafolder=station+'/'+station+"_Data/"
    path=""
    file_name="/Users/sweber/projects/13_AVUSPro/04_pres/KWS1M_L2_60S_20210310_20221213_20230123-153253.csv"
    data = pd.read_csv(path+file_name, comment="#", encoding="ISO-8859-1")
    print(data.columns)
    data.index = pd.to_datetime(data["JulianTime"])
    data = data.loc["2021-11-01 00:00":"2022-12-31 23:59"]
    del data["JulianTime"]
    return data,path


def plot_barh_flags(df,data_path,station):
        # --- FLAG DEFINITIONS --- #

        # S => used for solar parameters
        # A => used for ambient parameters
        MISSING_FLAG = 1e20  # S,A
        TIMESHIFT_FLAG = 1e18  # S,A # NOT YET USED
        MIN_PHYS_FLAG = 1e16  # S,A
        MAX_PHYS_FLAG = 1e15  # S,A
        TRACK_SHAD_FLAG = 1e12  # S
        GRADIENT_FLAG = 1e12  # A
        CLEANING_FLAG = 1e10  # S,A
        OTHER_VAL_FLAG = 1e21  # Filtered by other value (for AVUSpro measurements)

        REDUN_FLAG = 1e8  # S # NOT YET IMPLEMENTED
        TWO_COMP_FLAG = 1e7  # S
        THREE_COMP_FLAG = 1e6  # S
        REPLACED_FLAG = 1e5  # S,A
        CLEAR_SKY_EXC_FLAG = 1e4  # S
        RARE_OBS_FLAG = 1e2  # S,A
        CORRECT_FLAG = 1e0  # S,A
        
        FLAG_DESC_RAD = OrderedDict([
                (np.log10(CORRECT_FLAG) , "Correct"),
                (np.log10(RARE_OBS_FLAG) , "Rare Observation"),
                (np.log10(CLEAR_SKY_EXC_FLAG) , "Above Clear Sky Limit"),
                (np.log10(REPLACED_FLAG) , "Corrected"),
                (np.log10(THREE_COMP_FLAG) , "3 Comp. Test Failed"),
                (np.log10(TWO_COMP_FLAG) , "2 Comp. Test Failed"),
                (np.log10(REDUN_FLAG) , "Redundancy"),
                (np.log10(CLEANING_FLAG) , "Cleaning Event"),
                (np.log10(TRACK_SHAD_FLAG) , "Tracking Shading Error"),
                (np.log10(MAX_PHYS_FLAG) , "> Max. Phys. Limit"),
                (np.log10(MIN_PHYS_FLAG) , "< Min. Phys. Limit"),
                (np.log10(TIMESHIFT_FLAG) , "Timeshift Error"),
                (np.log10(MISSING_FLAG) , "Missing Values")
        ])
        
        FLAG_DESC_AUX = OrderedDict([
                (np.log10(CORRECT_FLAG) , "Correct"),
                (np.log10(RARE_OBS_FLAG) , "Rare Observation"),
                (np.log10(REPLACED_FLAG) , "Corrected"),
                (np.log10(REDUN_FLAG) , "Redundancy"),
                (np.log10(CLEANING_FLAG) , "Cleaning Event"),
                (np.log10(GRADIENT_FLAG) , "Above Gradient Limit"),
                (np.log10(MAX_PHYS_FLAG) , "> Max. Phys. Limit"),
                (np.log10(MIN_PHYS_FLAG) , "< Min. Phys. Limit"),
                (np.log10(TIMESHIFT_FLAG) , "Timeshift Error"),
                (np.log10(OTHER_VAL_FLAG), "Filtered by other value"),
                (np.log10(MISSING_FLAG) , "Missing Values")
        ])


        # separate general flag (timestep and not value-related flag) regarding the cleaning status
        DIRT_CLEANING_FLAG = 1e2
        WARN_CLEANING_FLAG = 1e1
        SUFF_CLEANING_FLAG = 1e0

        
        FLAG_DESC_SER = OrderedDict([
                (np.log10(SUFF_CLEANING_FLAG) , "Frequent Cleaning"),
                (np.log10(WARN_CLEANING_FLAG) , "Substandard Cleaning"),
                (np.log10(DIRT_CLEANING_FLAG) , "Insufficient Cleaning")
        ])

        # make lists of flag parameters for each category
        rad_flags = ["GHI_RSI1_Wm-2_avg_flag","GTI_RefCell1_Wm-2_avg_flag","GTI_RefCell2_Wm-2_avg_flag","GTI_RefCell3_Wm-2_avg_flag",
                     "DNI_RSI1_Wm-2_avg_flag","DHI_RSI1_Wm-2_avg_flag"]
        # save names to be shown in the plot
        rad_flag_names = ["GHI (RSI)","GTI RefCell1","GTI RefCell2","GTI RefCell3", "DNI (RSI)","DHI (RSI)"]
        print("Took RSI Variables")
        
        aux_flags = ["Temp_ThHyg1_degC_avg_flag", "Temp_Logger1_degC_avg_flag","TempMeasU_AVUS1_degC_avg_flag", "RH_ThHyg1_per100_avg_flag","RH_AVUS1_per100_avg_flag", "WindSpeed_Anemo1_ms_avg_flag",
                     "WindSpeed_Anemo1_ms_max_flag", "WindDir_Wvane1_deg_avg360_flag","Precip_Pluvio1_mm_sum_flag", "Pres_Logger1_hPa_avg_flag",
                     "LastMeasSample_AVUS1_mV_avg_flag","LastMeasRef_AVUS1_mV_avg_flag","TimeLastEv_AVUS1_-_avg_flag","LastClean_AVUS1_per100_avg_flag"]
        aux_flag_names = ["Temperature (Air)", "Temperature (Logger)", "Temperature (AVUS)","Relative Humidity","Relative Humidity (AVUS)", "Wind Speed", "Wind Gusts","Wind Direction",
                          "Precipitation (hourly values)", "Atmospheric Pressure","Measurement Sample (AVUS)","Measurement Reference (AVUS)","Time since last rain (AVUS)","Cleanliness (AVUS)"]

        ser_flags = ["ServiceButton_Logger1_-_sum_flag"]
        ser_flag_names = ["Service Button HelioScale"]
        
        '''
        # make lists of flag parameters for each category
        rad_flags = ["GHI_ThPyra1_Wm-2_avg_flag", "GHI_RSI1_Wm-2_avg_flag", "GTI_RefCell1_Wm-2_avg_flag",
                     "GTI_RefCell2_Wm-2_avg_flag", "GTI_RefCell3_Wm-2_avg_flag",
                     "DNI_ThPyrh1_Wm-2_avg_flag", "DNI_RSI1_Wm-2_avg_flag", "DHI_RSI1_Wm-2_avg_flag"]
        # save names to be shown in the plot
        rad_flag_names = ["GHI (ThPyra1)", "GHI (RSI)", "GTI RefCell1", "GTI RefCell2", "GTI RefCell3", "DNI (ThPyra1)",
                          "DNI (RSI)", "DHI (RSI)"]
        print("Took RSI Variables")

        aux_flags = ["Temp_ThHyg1_degC_avg_flag", "Temp_Logger1_degC_avg_flag", "TempMeasU_AVUS1_degC_avg_flag",
                     "RH_ThHyg1_per100_avg_flag","RH_AVUS1_per100_avg_flag", "WindSpeed_Anemo1_ms_avg_flag",
                     "WindSpeed_Anemo1_ms_max_flag", "WindDir_Wvane1_deg_avg360_flag", "Precip_Pluvio1_mm_sum_flag",
                     "Pres_Logger1_hPa_avg_flag",
                     "LastMeasSample_AVUS1_mV_avg_flag", "LastMeasRef_AVUS1_mV_avg_flag", "TimeLastEv_AVUS1_-_avg_flag",
                     "LastClean_AVUS1_per100_avg_flag"]
        aux_flag_names = ["Temperature (Air)", "Temperature (Logger)", "Temperature (AVUS)", "Relative Humidity",
                          "Relative Humidity (AVUS)", "Wind Speed", "Wind Gusts", "Wind Direction",
                          "Precipitation (hourly values)", "Atmospheric Pressure", "Measurement Sample (AVUS)",
                          "Measurement Reference (AVUS)", "Time since last rain (AVUS)", "Cleanliness (AVUS)"]

        ser_flags = ["ServiceButton_Logger1_-_sum_flag"]
        ser_flag_names = ["Service Button"]
        '''

        # calculate flag from string

        df_flags_rad = np.floor(np.log10(df[rad_flags].copy().astype(np.dtype("float64")).fillna(-9999)))
        df_flags_aux = np.floor(np.log10(df[aux_flags].copy().astype(np.dtype("float64")).fillna(-9999)))
        df_flags_ser = np.floor(np.log10(df[ser_flags].copy().astype(np.dtype("float64")).fillna(-9999)))

        
        # for precipitaion aux_flag_names = ["Temperature (Air)", "Temperature (Logger)", "Relative Humidity", "Wind Speed", "Wind Gusts", "Wind Direction", "Precipitation (hourly values)", "Atmospheric Pressure"]
        #print(df_flags_rad)

        # histogram bins
        n_bins = np.arange(-0.5, 22, 1)
        n_bins_ser = np.arange(-0.5, 3, 1)

        # create dataframes containing the relative proportion of each flag
        flags_bar_rad = pd.DataFrame(0, index=rad_flag_names, columns=FLAG_DESC_RAD.keys())
        print(FLAG_DESC_RAD)
        flags_bar_aux = pd.DataFrame(0, index=aux_flag_names, columns=FLAG_DESC_AUX.keys())
        flags_bar_ser = pd.DataFrame(0, index=ser_flag_names, columns=FLAG_DESC_SER.keys())

        
        
        for col, col_name in zip(df_flags_rad.columns, rad_flag_names):
            bar_rad=df_flags_rad.loc[:,col]
            flags_bar_rad.loc[col_name,:] = bar_rad.value_counts(normalize=True, sort=False, ascending=True, bins=n_bins, dropna=True)
        
        for col, col_name in zip(df_flags_aux.columns, aux_flag_names):
            bar_aux=df_flags_aux.loc[:,col]
            flags_bar_aux.loc[col_name,:] = bar_aux.value_counts(normalize=True, sort=False, ascending=True, bins=n_bins, dropna=True)
            print(bar_aux.value_counts(normalize=True, sort=False, ascending=True, bins=n_bins, dropna=True))
        
        for col, col_name in zip(df_flags_ser.columns, ser_flag_names):
            flags_bar_ser.loc[col_name,:] = pd.Series(df_flags_ser.loc[:,col]).value_counts(normalize=True, sort=False, ascending=True, bins=n_bins_ser, dropna=True)

        
        
        # defining the colors shown for each flag for all categories
        # colormap included in following image:
        # https://matplotlib.org/_images/colormaps_reference_05.png
        colors_irr=np.array([0.45, 0.52, 0.4, 0.68, 0.75, 0.8, 0.98, 0.3, 0.9, 0.1, 0.2, 1.0, 0.0])
        color_map_irr = plt.cm.nipy_spectral(colors_irr)
        
        colors_aux=np.array([0.45, 0.52, 0.68, 0.75, 0.3, 0.9, 0.1, 0.2, 0.98, 0.6, 0.0])
        color_map_aux = plt.cm.nipy_spectral(colors_aux)
        
        #colors_ser=np.array([0.45, 0.75, 0.85])
        colors_ser=np.array([0.45, 0.68, 0.8])
        color_map_ser = plt.cm.nipy_spectral(colors_ser)


        ## Barplot
        main_fontsize=12
        fig_barplot, (ax, ax2, ax3) = plt.subplots(nrows=3,figsize=(6,10), gridspec_kw = {'height_ratios':[5, 12, 1]})

        plt.subplots_adjust(hspace = 0.4)
        flags_bar_rad.iloc[::-1].plot.barh(width=0.5,stacked=True,color=color_map_irr, fontsize=main_fontsize, ax=ax)
        ax.set_xlabel('Relative Amount', fontsize=main_fontsize)
        ax.legend(FLAG_DESC_RAD.values(), bbox_to_anchor=(1.04,0.5), loc="center left", borderaxespad=0, fontsize=10)
        ax.set_xlim([0,1])
        #ax.grid()
        ax.set_title('Radiation parameters',fontsize=main_fontsize+2)


        flags_bar_aux.iloc[::-1].plot.barh(width=0.5,stacked=True,color=color_map_aux, fontsize=main_fontsize, ax=ax2)
        ax2.set_xlabel('Relative Amount', fontsize=main_fontsize)
        ax2.legend(FLAG_DESC_AUX.values(), bbox_to_anchor=(1.04,0.5), loc="center left", borderaxespad=0, fontsize=10)
        ax2.set_xlim([0,1])
        ax2.set_title('Auxiliary parameters',fontsize=main_fontsize+2)
        

        flags_bar_ser.plot.barh(width=0.5,stacked=True,color=color_map_ser, fontsize=main_fontsize, ax=ax3)
        ax3.set_xlabel('Relative Amount', fontsize=main_fontsize)
        ax3.legend(FLAG_DESC_SER.values(), bbox_to_anchor=(1.04,0.5), loc="center left", borderaxespad=0, fontsize=10)
        ax3.set_xlim([0,1])
        ax3.set_title('Cleaning (Pressing of Service Button)',fontsize=main_fontsize+2)
        figname=data_path+station+'barplot_flags.pdf'
        plt.savefig(str(figname),bbox_inches='tight')
        
        return flags_bar_aux,flags_bar_rad

data,path=handle_data(station)
flags_bar_aux,flags_bar_rad=plot_barh_flags(data,path,station)
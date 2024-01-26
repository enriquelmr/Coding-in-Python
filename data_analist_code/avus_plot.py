import pandas as pd
import numpy as np
from datetime import datetime, timedelta, time
import matplotlib.pyplot as plt
#from pandas.plotting import register_matplotlib_converters
#register_matplotlib_converters()
from pathlib import Path




def avuspro_plot_LM(df_filtered, station): #,df_filtered2,df_filtered3
	
	cleanliness = df_filtered['LastClean_AVUS1_per100_avg']
	precip_pluv = df_filtered['Precip_Pluvio1_mm_sum']
	service_button = df_filtered['SampleNo_AVUS1_-_avg']#['ServiceButton_Logger1_-_sum']
	precip_time = df_filtered['PrecipCleanEv_AVUS1_-_avg']#'PrecipTime_AVUS1_min_avg'
	cleanliness_sigma= df_filtered['LastClean_AVUS1_per100_avg'].resample('1D').std() \
		  / np.sqrt(df_filtered['LastClean_AVUS1_per100_avg'].resample('1D').size())
	soiling_daily_sigma =cleanliness_sigma.rolling(window=2).apply(lambda x: np.sqrt(sum(x ** 2)), raw=False)
	#sigma means the uncertainity


	cleanliness_daily_mean=cleanliness.resample('d',label='left',convention="start").mean()
	precip_pluv_daily_mean=precip_pluv.resample('d',label='left',convention="start").sum()
	service_button_daily_mean = service_button.resample('d',label='left',convention="start").mean().apply(np.ceil).diff(periods = 1)
	precip_time_daily_max = precip_time.resample('d',label='left',convention="start").max()
	soiling_daily_mean =  cleanliness_daily_mean.diff()
	
	#create figure
	fig, axes = plt.subplots(2, 1,sharex=True, figsize=(10,7))
	plt.subplots_adjust(hspace=0.1)

	###########################################################################
	#Subplot 1
	axes[0].plot(cleanliness_daily_mean.index,cleanliness_daily_mean,label="Cleanliness",color="red")
	axes[0].scatter(service_button_daily_mean.index, service_button_daily_mean*100, marker='P', color='darkgreen', label='Cleaning')

	axes[0].set_ylim(50,103)

	axes[0].set_ylabel("Cleanliness [%]",fontsize=14)
	axes[0].tick_params(axis='both', which='major', labelsize=12)

	#Second figure with scale in the right hand side
	axes0_twin =axes[0].twinx()
	axes0_twin.set_ylim(0,15)
	axes0_twin.bar(precip_time_daily_max.index, precip_time_daily_max, label='Max daily rain duration', color=(0.0, 0.0, 1.0, 0.5))
	
	axes0_twin.set_ylabel('Max rain duration [min]',fontsize=14)	

	###########################################################################
	#Subplot 2
	axes[1].errorbar(
		x = soiling_daily_mean.index,
		y = soiling_daily_mean,
		yerr=soiling_daily_sigma,
		fmt='_',
		ms=10,
		mew=1,
		ecolor='silver',
		color='darkgreen',
		elinewidth=2,
		capsize=2,
		label="Daily soiling rate",
		zorder=0.
	)
	axes[1].axhline(0, lw=1, c='silver', zorder=-100.)
	axes[1].set_ylim(-42,45)
	axes[1].set_ylabel("Daily soiling rate [%/d]",fontsize=14)
	axes[1].tick_params(axis='both', which='major', labelsize=12)
	
	axes[1].tick_params(axis='x', rotation=45)
	#Second figure with scale in the right hand side
	axes1_twin=axes[1].twinx()
	axes1_twin.set_ylim(0,45)
	axes1_twin.bar(precip_pluv_daily_mean.index,precip_pluv_daily_mean,color='lightblue',label="Rain [mm]",linestyle='--')
	axes1_twin.set_ylabel("Rain [mm]",fontsize=14)

	# Create a combined legend in the position of the title
	legend = fig.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05), ncol=5)
	plt.tight_layout(rect=[0, 0, 1, 1.01])
	
	###################save figure#############################################

	plt.savefig(f"{station}_plot.png", format='png',overwrite=True,bbox_inches='tight')
	print("Figure successfully created and saved!")

########################################################################################################################


#choose the input_path from which file u want to plot
input_path = "/home/shared/dbmod/KWS1M_L2_60S_20211101_20230625_20230808-161600.csv"; station="KWS1M"
#input_path = "/home/shared/dbmod/KWS1S_L2_60S_20211101_20230627_20230808-152040.csv"; station="KWS1S"
#input_path = "/home/shared/dbmod/KWS2S_L2_60S_20211101_20230627_20230816-105457.csv"; station="KWS2S"
data = pd.read_csv(input_path,comment="#",encoding="ISO-8859-1")
data.index = pd.to_datetime(data["JulianTime"])
data = data.loc["2021-11-01 00:00":"2022-12-30 23:59"]



#avuspro_plot(data)
avuspro_plot_LM(data,station)

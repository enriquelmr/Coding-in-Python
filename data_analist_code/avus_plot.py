import pandas as pd
import numpy as np
from datetime import datetime, timedelta, time
import matplotlib.pyplot as plt
#from pandas.plotting import register_matplotlib_converters
#register_matplotlib_converters()
from pathlib import Path


def avuspro_plot(df_filtered):
	# prepare data for plotting (calculate daily mean + uncertainty)

	# calculate daily mean of the measurement data
	df_filtered_daily = df_filtered.resample('1D').mean()
	df_filtered_daily_max = df_filtered.resample('1D').max()
	df_filtered_daily_sum = df_filtered.resample('1D').sum()
	# print(df_filtered.columns)
	# input()

	# calculate the uncertainty of the mean cleanliness
	# (standard formula of uncertainty of the mean:
	# calculate standard deviation of measurements of for each day and divide by the sqrt of the number of measurement points)
	df_filtered_daily['LastClean_AVUS1_per100_avg_unc'] \
		= df_filtered['LastClean_AVUS1_per100_avg'].resample('1D').std() \
		  / np.sqrt(df_filtered['LastClean_AVUS1_per100_avg'].resample('1D').size())

	# calculate the daily soiling rate:
	# daily soiling rate is the difference to the previous day
	df_filtered_daily['SoilingRate_daily'] = df_filtered_daily['LastClean_AVUS1_per100_avg'].diff(
		periods=1  # 1 refers to previous row
	)

	# calculate uncertainty of daily soiling rate
	# define function to calculate the uncertainty of a difference
	# def fun(x):
	#     """Funktion to calculate the uncertainty of a difference of two values with
	#     Gaussian uncertainty propagation.
	#     """
	#     s = np.sqrt(sum(x ** 2))
	#     return s

	# apply the defined function to subsequent pairs of the cleanliness values
	# df_filtered_daily['SoilingRate_daily_unc'] = df_filtered_daily['LastClean_AVUS1_per100_avg_unc'].rolling(
	#     window=2
	# ).apply(fun, raw=False)

	# REPLACING ABOVE FUNCTION BY LAMBDA EXPRESSION
	df_filtered_daily['SoilingRate_daily_unc'] = df_filtered_daily['LastClean_AVUS1_per100_avg_unc'].rolling(
		window=2
	).apply(lambda x: np.sqrt(sum(x ** 2)), raw=False)

	# calculate daily mean values of the raw data (this data frame is needed for the rain data, because rain data is removed during filtering)
	# NOTE: Nothing to do here, this data is in df_filtered_daily.
	# df_raw_daily = df_raw.resample('1D').mean()

	# with pd.option_context('display.max_rows', 100, 'display.max_columns', 100):
	#    print(df_raw_daily)

	###############################################################################
	# make plot

	f, axarr = plt.subplots(nrows=2, ncols=1, sharex=True, figsize=(10, 7), tight_layout=True)

	# plot cleanliness on first axis
	ax = axarr[0]

	# plot points
	# ax.plot(df_filtered_daily['LastClean_AVUS1_per100_avg'], '.')  # plot without uncertainty
	# ax.errorbar(
	#     x=df_filtered_daily['LastClean_AVUS1_per100_avg'].index,
	#     y=df_filtered_daily['LastClean_AVUS1_per100_avg'],
	#     yerr=df_filtered_daily['LastClean_AVUS1_per100_avg_unc'],
	#     fmt='.',
	#     ecolor='silver',
	#     zorder=0.
	# )

	data_plot = df_filtered_daily[
		'LastClean_AVUS1_per100_avg']#.dropna()  # drop lines with nan values in order to have a continuous black line
	ax.plot(data_plot, c='red', lw=2, alpha=0.6, zorder=10., label="Cleanliness")

	ax.set_ylim(58, 103)
	ax.axvline(10, lw=.4, c='silver', zorder=-100.)

	ax.set_ylabel('Cleanliness [%]')

	ax.tick_params(axis='y', right=False)  # switch off right ticks for cleanliness axis

	# plot rain duration on first axis
	ax2 = ax.twinx()
	width = 0.5
	x = df_filtered_daily.index
	y1 = df_filtered_daily_max['PrecipCleanEv_AVUS1_-_avg']  # / (60 * 24)
	# y2 = df_filtered_daily['TimeLastEv_AVUS1_-_avg_raw'] / (60 * 60 * 24)  # convert from minutes per hour to hours per day
	# ax2.bar(x, y1*0.1,width=width,alpha = 0.6, align='center', label = "Rain time", color = "lightred", zorder = 10.)
	# plot daily max of rain_sl_meas
	data_plot2 = df_filtered_daily['SampleNo_AVUS1_-_avg'].apply(np.ceil).diff(periods = 1)
	data_plot2 = data_plot2[data_plot2 > 0.]#.dropna()
	data_plot2 = data_plot2*0.5

	ax2.bar(x, y1, width=width, align='edge', label="Max daily rain duration", color="blue", alpha=0.5, zorder=5.)
	ax2.scatter(data_plot2.index, data_plot2+18, c='forestgreen', marker='P', zorder = 5., label = "Cleaning")

	ax2.set_ylim([0, 20])
	ax2.set_ylabel("Max rain duration [min]")  # \n / Rain time [10 min]")
	########
	ax.set_zorder(ax2.get_zorder() + 1)  # put ax in front of ax2
	ax.patch.set_visible(False)  # hide the 'canvas'
	#####
	# lines_labels = [leg.get_legend_handles_labels() for leg in f.axes]
	# lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]

	# f.legend(lines, labels, loc = "upper centre", mode="expand",
	#            borderaxespad=0, ncol=3)

	# plot daily soiling rate on second axis
	ax3 = axarr[1]
	ax3.errorbar(
		x=df_filtered_daily['SoilingRate_daily'].index,
		y=df_filtered_daily['SoilingRate_daily'],
		yerr=df_filtered_daily['SoilingRate_daily_unc'],
		fmt='_',
		ms=10,
		mew=1,
		ecolor='silver',
		color='blue',
		elinewidth=2,
		capsize=2,
		label="Daily soiling rate",
		zorder=0.
	)
	#ax3.plot(df_filtered_daily['SoilingRate_daily'].index,df_filtered_daily['SoilingRate_daily'], c='red', lw=2, alpha=0.8, zorder=10., label="Cleanliness")
	ax3.axhline(0, lw=1, c='silver', zorder=-100.)
	ax3.set_ylabel('Daily soiling rate  [%/d]')

	ax4 = ax3.twinx()
	x = df_filtered_daily.index
	y = df_filtered_daily_sum['Precip_Pluvio1_mm_sum']
	ax4.bar(x, y, width=width, align='center', color="lightblue", alpha=0.8, zorder=100., label="Precipitation")
	ax4.set_ylabel("Precipitation [mm]")

	# lines_labels = [leg.get_legend_handles_labels() for leg in f.axes]
	# lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]

	# print(lines_labels)
	# input()
	lines_labels = [leg.get_legend_handles_labels() for leg in f.axes]
	lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]

		#print(lines_labels)
		#input()

	#f.legend(lines, labels, loc = 9, mode="expand", frameon = False, bbox_to_anchor=(1.02,1.05),
	   #     ncol=6, fontsize = 12)#borderaxespad=0,
	#f.legend(lines, labels, loc=2, mode="expand", frameon=False, #bbox_to_anchor=(110,1.0),
	 #        ncol=4, fontsize=12)#, borderaxespad=2)
	#f.legend(loc='lower left', mode = "expand", bbox_to_anchor=(0,1.02,1,0.2),
	 #     fancybox=True, shadow=True, ncol=5)
	ax2.legend(lines,labels, bbox_to_anchor=(0.5,1.15), loc='upper center',
					  ncol=5)#, mode="expand", borderaxespad=0.)
	# plot vertical lines at midnight on both axes
	dti = pd.date_range(start=df_filtered.index[0].strftime("%Y-%m-%d"),
						end=df_filtered.index[-1].strftime("%Y-%m-%d"), freq='D')

	#for ax in axarr:
	#    for x in dti:
	#        ax.axvline(x, lw=.5, c='silver', zorder=-100)
	plt.grid(axis='x', color='0.95')
	plt.xlim(df_filtered.index[0].strftime("%Y-%m-%d %H:%M"), df_filtered.index[-1].strftime("%Y-%m-%d %H:%M"))
	ax3.set_ylim([50, -55])

	plt.tight_layout()

	f.autofmt_xdate()
	avus_plot_path = Path('KWS1M.pdf')   ################################## Change! ##################################
	plt.savefig(str(avus_plot_path))


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
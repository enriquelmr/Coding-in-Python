import pandas as pd

parameter_full_day_snow = 1.0
station = 'LVREZ'


folder_path = '/home/shared/solar_ressource_assessment/offline_sources/HelioClim3/'
path = folder_path + station +'.csv'

# Read the CSV file
data = pd.read_csv(path, comment="#", sep=';')

# Create a datetime column
data['Time'] = data['Time'].str.replace('24:00', '00:00')
data['Datetime'] = pd.to_datetime(data['Date'] + ' ' + data['Time'])

data.set_index('Datetime', inplace=True)

# Resample the data to daily frequency and sum the values
data_resampled = data.resample('D').sum()

# Group by year and month and take the average
grouped_data = data_resampled.groupby([data_resampled.index.month]).sum()

#data_resampled2 = grouped_data.resample('M').sum()
# Print the result if needed
print(grouped_data["Snowfall"]/65)
#print(data_resampled2)



import pandas as pd
import matplotlib.pyplot as plt

# Set a parameter value to consider a day as a snowing day
parameter_full_day_snow = 0.5
parameter_full_day_snow_depth = 0.01
station = 'PLZWA'


folder_path = '/home/shared/solar_ressource_assessment/offline_sources/HelioClim3/'
path = folder_path + station +'.csv'


###################### Reading the files #####################################
# folder_path_sg = f'/home/shared/solar_ressource_assessment/offline_sources/Solargis/{station}'
# Read the CSV file
data_hc3 = pd.read_csv(path, comment="#", sep=';', usecols =  ['Date', 'Time', 'Snowfall','Snow depth'])

# Create a datetime column
data_hc3['Time'] = data_hc3['Time'].str.replace('24:00', '00:00')
data_hc3['Datetime'] = pd.to_datetime(data_hc3['Date'] + ' ' + data_hc3['Time'])


data_hc3.set_index('Datetime', inplace=True)

# Resample the data to daily frequency and sum the values
data_resampled = data_hc3.resample('D').sum()
data_resampled_avg = data_hc3.resample('D').mean()


################### Filter the data for the specified date range#############
start_date = '2013-01-01'
end_date = '2023-11-30'
filtered_data = data_resampled[(data_resampled.index >= start_date) & (data_resampled.index <= end_date)]
filtered_data_avg = data_resampled_avg[(data_resampled_avg.index >= start_date) & (data_resampled_avg.index <= end_date)]

#################### Plot the snowfall data###################
plt.figure(figsize=(20, 6))

# Plot for 'Snowfall' on the left-hand side
plt.plot(filtered_data.index, filtered_data['Snowfall'], label='Snowfall', color='blue', linewidth=0.5)
plt.axhline(y=parameter_full_day_snow, color='b', linestyle='--', label=f'Threshold (Snowfall): {parameter_full_day_snow}')
plt.title('Snowdays from {} to {}'.format(start_date, end_date))
plt.xlabel('Date')
plt.ylabel('Snowfall sum along the day [kg/m2]', color='blue')
plt.legend(loc='upper left')
# Create a twin Axes sharing the yaxis for 'Snow depth' on the right-hand side
ax2 = plt.gca().twinx()
ax2.plot(filtered_data_avg.index, filtered_data_avg['Snow depth'], label='Snow depth', color='green', linewidth=0.5)
ax2.axhline(y=parameter_full_day_snow_depth, color='g', linestyle='--', label=f'Threshold (Snow depth): {parameter_full_day_snow_depth}')
ax2.set_ylabel('Snow depth daily average [m]', color='green')
ax2.legend()
# Create a twin Axes sharing the yaxis

plt.grid(True)

plt.savefig('snow.pdf')

##################   snowing days   #########################
# Create a dictionary to store snow days count for each year-month
snow_days = {}
snow_depth_days = {}

# Iterate over rows in the DataFrame
for index, row in filtered_data.iterrows():
    if row['Snowfall'] > parameter_full_day_snow:
        # Extract the year and month from the index
        year_month = (index.year, index.month)

        # Increment the snow_days count for the corresponding year-month
        snow_days[year_month] = snow_days.get(year_month, 0) + 1


# Iterate over rows in the DataFrame
for index, row in filtered_data_avg.iterrows():
    if row['Snow depth'] > parameter_full_day_snow_depth:
        # Extract the year and month from the index
        year_month = (index.year, index.month)

        # Increment the snow_days count for the corresponding year-month
        snow_depth_days[year_month] = snow_depth_days.get(year_month, 0) + 1

# Display the snow_days dictionary

# Save the snow_days dictionary to a text file
all_year_months = set(snow_days.keys()).union(set(snow_depth_days.keys()))
# Define the file path for the output text file
output_file_path = 'snow_days_table.txt'

# Open the file in write mode
with open(output_file_path, 'w') as output_file:
    # Write the header
    output_file.write(f"Station:{station}\n")
    output_file.write("Year-Month\tSnow Days\tSnow Depth Days\n")
    output_file.write(f"Threshold\t{parameter_full_day_snow}[kg/m2]\t{parameter_full_day_snow_depth}[m]\n")
    # Iterate over each year-month
    for year_month in sorted(all_year_months):
        # Get the count from snow_days dictionary, default to 0 if not present
        snow_days_count = snow_days.get(year_month, 0)

        # Get the count from snow_depth_days dictionary, default to 0 if not present
        snow_depth_days_count = snow_depth_days.get(year_month, 0)

        # Write the data to the file
        output_file.write(f"{year_month[0]}-{year_month[1]}     \t{snow_days_count}\t{snow_depth_days_count}\n")
###############################################################
print('ready!')
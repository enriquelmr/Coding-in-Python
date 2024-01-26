import pandas as pd

# Load CSV file into a DataFrame
file_path = '/home/shared/solar_ressource_assessment/offline_sources/HelioClim3/MGTER.csv'  # Replace with the actual file path
df = pd.read_csv(file_path, sep=";", comment="#", na_values=[-999, "-999"])

# Combine 'Date' and 'Time' columns into a single datetime column
df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'].replace('24:00', '00:00'), format='%Y-%m-%d %H:%M')  # Adjust the format based on your 'Time' column
df.set_index('Datetime', inplace=True)

# Columns to be resampled and formatted
columns_to_format = ['Global Horiz', 'Rainfall', 'Snowfall', 'Snow depth', 'Clear-Sky', 'Top of Atmosphere', 'Code', 'Temperature', 'Relative Humidity', 'Pressure', 'Wind speed', 'Wind direction']

# Resample the DataFrame by hour and format the output
df_resampled = df[columns_to_format].resample('H').mean()  # 'H' represents hourly frequency, you can adjust as needed

# Convert the resampled DataFrame to the desired format with headers
formatted_df = pd.DataFrame(index=df_resampled.index)
formatted_df['Datetime'] = formatted_df.index
formatted_df = formatted_df.apply(lambda row: f"{row['Datetime'].strftime('%Y-%m-%d;%H:%M')};" + ';'.join(f"{value:.4f}" for value in df_resampled.loc[row['Datetime']]), axis=1)

# Save the formatted DataFrame to a new CSV file
formatted_df.to_csv('formatted_output.csv', index=False, header=True)

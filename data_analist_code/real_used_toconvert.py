import os
import pandas as pd

def process_excel(input_path, output_path):
    for file_name in os.listdir(input_path):
        if file_name.endswith(".xlsx") and file_name.startswith("Wms REPORT"):
            full_path = os.path.join(input_path, file_name)
            
            df = pd.read_excel(full_path, sheet_name=0, header=5)
            
            if df.isnull().all(axis=1).any():
                empty_row_index = df.index[df.isnull().all(axis=1)].tolist()[0]
                df = df.iloc[:empty_row_index]
            else: 
                pass
            
            date = pd.read_excel(full_path, sheet_name=0, header=None, usecols="B", nrows=4).iloc[3, 0]
            date = pd.to_datetime(date, format='%d/%m/%Y').date()

            # Add a new column 'date' as the first column
            df.insert(0, 'date', date)

            df = df.rename(columns={'Time': 'time'})
    
            # Save the DataFrame to a CSV file with the date as the file name
            output_file_name = f'{date}.csv'
            output_file_path = os.path.join(output_path, output_file_name)
            df.to_csv(output_file_path, index=False)

# Define input and output paths
input_path = "/Users/luis.martinez/Documents/practica/data"
output_path = "/Users/luis.martinez/Documents/practica/newdata"
# Save the DataFrame to a CSV file with the date as the file name
# execute the transformation from excel to csv files, this is adjusted to paramenters in files of noorIV 
process_excel(input_path, output_path)

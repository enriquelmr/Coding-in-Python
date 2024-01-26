import os
import pandas as pd

def process_excel(input_path, output_path):
        for month in range(1, 13):  # 1 to 12 for months
            subfolder = os.path.join(input_path, str(month))
            
            if not os.path.exists(subfolder):
                continue

            for file_name in os.listdir(subfolder):
                full_path = os.path.join(subfolder, file_name)
                
                # Read the Excel file with header starting from row 5
                df = pd.read_excel(full_path, sheet_name=0, header=5)

                # drop after empty lines
                if df.isnull().all(axis=1).any():
                    empty_row_index = df.index[df.isnull().all(axis=1)].tolist()[0]
                    df = df.iloc[:empty_row_index]
                else: 
                    pass
                
                date = pd.read_excel(full_path, sheet_name=0, header=None, usecols="B", nrows=4).iloc[3, 0]
                date = pd.to_datetime(date, format='%d/%m/%Y').date()

                df.insert(0, 'date', date)
                df = df.rename(columns={'Time': 'time'})
                
                # Save the DataFrame to a CSV file with the date as the file name
                output_file_name = f'{date}.csv'
                output_file_path = os.path.join(output_path, output_file_name)
                df.to_csv(output_file_path, index=False)

# Define input and output paths
input_path = "/home/luis.martinez/prac/data/2020/"
output_path = "/data/meteodb/input/type=ground/format=Blueberry_V1/id=NOOR1"


# execute the transformation from excel to csv files, this is adjusted to paramenters in files of noorIV 
process_excel(input_path, output_path)

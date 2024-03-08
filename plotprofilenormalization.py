import os
import pandas as pd
from tkinter import filedialog

# Select directory containing the folders
dirPath = filedialog.askdirectory(title='Select directory containing folders')
print(f"Selected directory: {dirPath}")

# Initialize an empty dataframe
df = pd.DataFrame()
print("Initialized empty dataframe.")

# Loop through each folder in the directory
for foldername in os.listdir(dirPath):
    folderPath = os.path.join(dirPath, foldername)
    print(f"Processing folder: {folderPath}")
    
    # Loop through each CSV file in the folder
    for filename in os.listdir(folderPath):
        if filename.endswith('.csv'):
            filePath = os.path.join(folderPath, filename)
            print(f"Processing CSV file: {filePath}")
            
            # Import data from CSV file
            data = pd.read_csv(filePath)
            Y1 = data.iloc[:, 1]
            
            # Normalize Y-values
            Ynorm = (Y1 - Y1.min()) / (Y1.max() - Y1.min())
            
            # Add normalized Y-values to the dataframe as a new column
            column_name = f"{foldername}_{os.path.splitext(filename)[0]}"
            df[column_name] = Ynorm
            print(f"Added column '{column_name}' to dataframe.")

# Write the dataframe to an Excel file
excelFilePath = os.path.join(dirPath, 'normalized_data.xlsx')
df.to_excel(excelFilePath, index=False)
print(f"Dataframe saved to Excel file: {excelFilePath}")

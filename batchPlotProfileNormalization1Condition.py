import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tkinter import filedialog

# Select directory containing the folders
dirPath = filedialog.askdirectory(title='Select directory containing folders')
print(f"Selected directory: {dirPath}")

# Initialize an empty dataframe
df = pd.DataFrame()
print("Initialized empty dataframe.")

# Number of points after normalization
num_points = 100

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
            X1 = data.iloc[:, 0]
            Y1 = data.iloc[:, 1]
            
            # Normalize X-values
            Xnorm = (X1 - X1.min()) / (X1.max() - X1.min())
            
            # Normalize Y-values
            Ynorm = (Y1 - Y1.min()) / (Y1.max() - Y1.min())
            
            # Interpolate to ensure exactly num_points values
            Xnorm_interp = np.linspace(0, 1, num_points)
            Ynorm_interp = np.interp(Xnorm_interp, Xnorm, Ynorm)
            
            # Add normalized Y-values to the dataframe as a new column
            column_name = f"{foldername}_{os.path.splitext(filename)[0]}"
            df[column_name] = Ynorm_interp
            print(f"Added column '{column_name}' to dataframe.")

# Save the dataframe to an Excel file in the selected directory
excelFilePath = os.path.join(dirPath, 'normalized_data.xlsx')
df.to_excel(excelFilePath, index=False)
print(f"Dataframe saved to Excel file: {excelFilePath}")

# Compute mean and 95% CI
mean_intensity = df.mean(axis=1)  # Mean across different cells
std_intensity = df.std(axis=1)     # Standard deviation across different cells
n = df.shape[1]                    # Number of cells
ci = 1.96 * (std_intensity / np.sqrt(n))  # 95% CI

# Plot mean signal intensity with error bars and a connecting line
plt.figure(figsize=(10, 6))  # Adjust figure size
plt.errorbar(df.index, mean_intensity, yerr=ci, fmt='o-', capsize=5, markersize=5)
plt.xlabel('Distance (0-100)', fontsize=14, fontweight='bold')
plt.ylabel('Signal Intensity', fontsize=14, fontweight='bold')
plt.title('Signal Intensity along Axon with 95% CI', fontsize=16, fontweight='bold')
plt.xticks(fontsize=12)  # Increase x-axis tick font size
plt.yticks(fontsize=12)  # Increase y-axis tick font size
plt.grid(True)
plt.xlim(0)  # Set x-axis to start at 0

# Save the plot as a vector image file (EPS) in the same directory as the Excel file
plotFilePath = os.path.join(dirPath, 'signal_intensity_plot.eps')
plt.savefig(plotFilePath, format='eps')
print(f"Plot saved as vector image file (EPS): {plotFilePath}")


plt.show()


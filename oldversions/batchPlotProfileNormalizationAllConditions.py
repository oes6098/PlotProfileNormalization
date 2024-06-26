import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tkinter import filedialog

# Select directory containing the folders
dirPath = filedialog.askdirectory(title='Select directory containing folders')
print(f"Selected directory: {dirPath}")

# Get a list of directories (folders) in the selected directory
condition_folders = [folder for folder in os.listdir(dirPath) if os.path.isdir(os.path.join(dirPath, folder))]

# Number of points after normalization
num_points = 100

# Initialize an empty dictionary to store DataFrames for each condition folder
dfs = {}

# Loop through each condition folder in the directory
for i, condition_folder in enumerate(condition_folders):
    conditionFolderPath = os.path.join(dirPath, condition_folder)
    print(f"Processing condition folder: {conditionFolderPath}")

    # Initialize an empty dataframe for the current condition folder
    df = pd.DataFrame()
    print("Initialized empty dataframe.")

    # Initialize an empty list to store 95th percentile values for each file in the current condition folder
    percentile_list = []

    # Loop through each folder in the condition folder
    for foldername in os.listdir(conditionFolderPath):
        folderPath = os.path.join(conditionFolderPath, foldername)
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

                # Calculate the 95th percentile
                ninety_fifth_percentile = np.percentile(Ynorm_interp, 95)
                
                # Append the filename and 95th percentile to the list
                percentile_list.append({'File': filename, '95th Percentile': ninety_fifth_percentile})


    # Save the dataframe to an Excel file in the condition folder
    excelFilePath = os.path.join(conditionFolderPath, f'normalized_data_condition_{i}.xlsx')
    df.to_excel(excelFilePath, index=False)
    print(f"Dataframe saved to Excel file: {excelFilePath}")

    # Convert the list of dictionaries to a DataFrame
    percentile_df = pd.DataFrame(percentile_list)

    # Save the dataframe with individual file percentiles to a CSV file
    percentile_df.to_excel(os.path.join(conditionFolderPath, f'individual_95percentiles_{i}.xlsx'), index=False)
    print(f"Individual percentiles saved to Excel file: {excelFilePath}")

    # Store the dataframe in the dictionary with the condition folder name as key
    dfs[condition_folder] = df

    # Compute mean and 95% CI
    mean_intensity = df.mean(axis=1)  # Mean across different cells
    std_intensity = df.std(axis=1)     # Standard deviation across different cells
    n = df.shape[1]                    # Number of cells
    ci = 1.96 * (std_intensity / np.sqrt(n))  # 95% CI

    # Plot mean signal intensity with error bars and a connecting line
    plt.figure(figsize=(10, 6))  # Adjust figure size
    plt.errorbar(df.index, mean_intensity, yerr=ci, fmt='o-', capsize=5, markersize=5, label=condition_folder)
    plt.xlabel('Distance (0-100)', fontsize=14, fontweight='bold')
    plt.ylabel('Signal Intensity', fontsize=14, fontweight='bold')
    plt.title('Signal Intensity along Axon with 95% CI', fontsize=16, fontweight='bold')
    plt.xticks(fontsize=12)  # Increase x-axis tick font size
    plt.yticks(fontsize=12)  # Increase y-axis tick font size
    plt.grid(True)
    plt.legend()  # Show legend

    # Save the plot as a vector image file (EPS) in the same directory as the Excel file
    plotFilePath = os.path.join(conditionFolderPath, f'signal_intensity_plot_condition_{i}.eps')
    plt.savefig(plotFilePath, format='eps')
    print(f"Plot saved as vector image file (EPS): {plotFilePath}")

    plt.show()

plt.figure(figsize=(10, 6))  # Adjust figure size

# Plot each condition's mean signal intensity with 95% CI and different colors
for condition, df in dfs.items():
    mean_intensity = df.mean(axis=1)
    std_intensity = df.std(axis=1)
    n = df.shape[1]
    ci = 1.96 * (std_intensity / np.sqrt(n))  # 95% CI
    plt.errorbar(df.index, mean_intensity, yerr=ci, fmt='o-', capsize=5, markersize=5, label=condition)

plt.xlabel('Distance from Soma', fontsize=14, fontweight='bold')
plt.ylabel('Mean Signal Intensity', fontsize=14, fontweight='bold')
plt.xticks(fontsize=12)  # Increase x-axis tick font size
plt.yticks(fontsize=12)  # Increase y-axis tick font size
plt.legend()  # Show legend

# Set limits for x and y axes
plt.xlim(0, None)  # Set x-axis lower limit to 0
plt.ylim(0, None)  # Set y-axis lower limit to 0

plt.grid(True)  # Bring back the grid

# Save the plot as a PDF file
plotFilePath = os.path.join(dirPath, f'combined_signal_intensity_plot_condition.pdf')
plt.savefig(plotFilePath, format='pdf')
print(f"Plot saved as vector image file (PDF): {plotFilePath}")

plt.show()
# PlotProfileNormalization_CompileResults

Batch normalize and compile plot profile outputs from Fiji


1. Trace plot profile on Fiji and save data in individual folder
2. Run batchPlotProfileNormalization script which will ask for desired directory, then iterate through each folder within the directory, opening the plot profile results file, normalizing data and compiling normalized y axis data onto a new excel sheet, saved in the same directory. Additionally, the 95% of the normalized data for each individual folder is calculated.
3. Now you have a compilation of normalized signal/pixel intensity with the same amount of X values and a compilation of the 95% for individual files

Y values are normalized by subtracting minimum Y value from all Y-values then dividing by the range of Y (difference between the maximum and minimum values of Y). The same process is down for X. Then interpolation is performed to ensure both X and Y data points have exactly 100 points

batchPlotProfileNormalization1Condition is for 1 condition of data, expected to be in 1 folder
batchPlotProfileNormalizationAllConditions is for all conditions of data (expected to be in different folders)

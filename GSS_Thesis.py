import arcpy
# To allow overwriting outputs, change overwriteOutput option to True.
arcpy.env.overwriteOutput = True
# Check out any necessary licenses.
arcpy.CheckOutExtension("GeoStats")

import arcpy

# To allow overwriting outputs, change overwriteOutput option to True.
arcpy.env.overwriteOutput = True

# Check out any necessary licenses.
arcpy.CheckOutExtension("GeoStats")

# Input parameters
errorNM_Clip = r"F:\Miami\Miami_dade_county\Default.gdb\errorNM_Clip"  # Your clipped error data
output_workspace = "F:\\Miami\\Miami_dade_county\\Default.gdb"  # Output workspace

# Process: Exploratory Interpolation
SK = "F:\\Miami\\Miami_dade_county\\Default.gdb\\MB_OK0"
SK1 = "MB_OK10"
arcpy.ga.ExploratoryInterpolation(
    in_features=errorNM_Clip,
    value_field="Error",
    out_cv_table=SK,
    out_geostat_layer=SK1,
    interp_methods=["SIMPLE_KRIGING"]
)

# Process: Create Geostatistical Layer with Spatial Key (SK)
out_layer = "GAC_SK1"
arcpy.ga.GACreateGeostatisticalLayer(
    in_ga_model_source=SK1,
    in_datasets=f"{errorNM_Clip} F1=Error",
    out_layer=out_layer
)


# Name: GaussianGeostatisticalSimulations_Example_02.py
# Description: This script performs conditional or unconditional geostatistical
#              simulation based on a Simple Kriging model.
# Requirements: Geostatistical Analyst Extension

# Import system modules
import arcpy

# Set environment settings
arcpy.env.workspace = "F:\\Miami\\Miami_dade_county\\Default.gdb"

# Set local variables
inLayer = out_layer
numRealizations = 500
outWorkspace = r"F:\Miami\Miami_dade_county\Simulations"
cellSize = 150
prefix = "ggs"
rasstatType = "MEAN"
conFeatures = "errorNM_Clip"
conField = "Error"
boundingData = ""
savesimRasters = "SAVE_SIMULATIONS"
quantile = ""
threshold = ""
statsPolygons = ""
errorField = ""

# Execute GaussianGeostatisticalSimulations
arcpy.GaussianGeostatisticalSimulations_ga(
    in_geostat_layer=inLayer,
    number_of_realizations=numRealizations,
    output_workspace=outWorkspace,
    output_simulation_prefix=prefix,
    in_conditioning_features=conFeatures,
    conditioning_field=conField,
    cell_size=cellSize,
    in_bounding_dataset=boundingData,
    save_simulated_rasters=savesimRasters,
    quantile=quantile,
    threshold=threshold,
    in_stats_polygons=statsPolygons,
    raster_stat_type=rasstatType,
    conditioning_measurement_error_field=errorField
)


# Name: AddSimulationsToDem.py
# Description: This script adds each simulated raster to the DEM raster.
# Requirements: ArcGIS Spatial Analyst Extension

# Import system modules
import arcpy
from arcpy import env
from arcpy.sa import *
import os

# Set environment settings
arcpy.env.workspace = r"F:\Miami\Miami_dade_county\Simulations"

arcpy.env.overwriteOutput = True
# Set local variables
demRaster = r"F:\Miami\Miami_dade_county\Default.gdb\DEM_2021_5FT_Clip"  # Update with your DEM raster path
demRaster = r"F:\Miami\Miami_dade_county\Default.gdb\DEM_2021_5FT_Clip"
simulationsFolder = r"F:\Miami\Miami_dade_county\Simulations"
outputFolder = r"F:\Miami\Miami_dade_county\dem_correction"

# Create the output folder if it doesn't exist
if not arcpy.Exists(outputFolder):
    os.makedirs(outputFolder)

# List all the simulation rasters in the simulations folder
simulationsList = arcpy.ListRasters()
simulationsList



arcpy.env.overwriteOutput = True
# Iterate through each simulation raster and add it to the DEM raster
for simulationRaster in simulationsList:
    simulationRasterPath = os.path.join(simulationsFolder, simulationRaster)

    # Check if the simulation raster exists
    if arcpy.Exists(simulationRasterPath):
        # Add the simulation raster to the DEM raster
        outputRaster = os.path.join(outputFolder, f"{os.path.splitext(simulationRaster)[0]}_correction.tif")
        arcpy.sa.Plus(demRaster, simulationRasterPath).save(outputRaster)
        print(f"Raster correction saved: {outputRaster}")
    else:
        print(f"Skipping {simulationRaster} - does not exist or is not supported")

print("Correction process complete.")



# Import system modules
import arcpy
from arcpy import env
from arcpy.sa import *
import os

# Set environment settings
arcpy.env.workspace =  r"F:\Miami\Miami_dade_county\dem_correction"

arcpy.env.overwriteOutput = True

# Set local variables
inputFolder = r"F:\Miami\Miami_dade_county\dem_correction"
outputFolder = r"F:\Miami\Miami_dade_county\raster_calculations"

# Create the output folder if it doesn't exist
if not arcpy.Exists(outputFolder):
    os.makedirs(outputFolder)

# List all the raster datasets in the input folder
rasters = arcpy.ListRasters()
rasters


#Use of Raster Calculator for finding flood inundation using simple bathtub hydrolgically connected approach
import numpy as np

arcpy.env.overwriteOutput = True
# Iterate through each raster and perform the calculation (6.693 - raster)
for raster in rasters:
    inputRaster = os.path.join(inputFolder, raster)
    outputRaster = os.path.join(outputFolder, f"{os.path.splitext(raster)[0]}_calculation.tif")
    
    # Load the input raster as a Raster object
    input_raster = Raster(inputRaster)
    
    # Perform the raster calculation
    output_raster = 6.693 - input_raster
    
    # Save the result to the output raster
    output_raster.save(outputRaster)
    
    print(f"Raster calculation saved: {outputRaster}")

print("Raster calculation process complete.")


#Calculations of Probabilty of flood
import arcpy
import numpy as np
import os

# Assuming you have a list of output raster paths from the previous step
output_raster_folder = r"F:\Miami\Miami_dade_county\raster_calculations"
output_raster_paths = [os.path.join(output_raster_folder, raster) for raster in os.listdir(output_raster_folder) if raster.endswith(".tif")]

# Initialize an empty NumPy array to store inundation counts for each grid cell
first_raster = arcpy.Raster(output_raster_paths[0])
inundation_counts = np.zeros((first_raster.height, first_raster.width))

# Iterate through the output rasters and count inundation occurrences
for output_raster_path in output_raster_paths:
    output_raster = arcpy.Raster(output_raster_path)
    # Use arcpy.RasterToNumPyArray to convert the raster to a NumPy array
    conditional_array = arcpy.RasterToNumPyArray(output_raster, nodata_to_value=0)
    # Apply the condition (output_raster > 0) to create a boolean array
    condition_mask = conditional_array > 0
    # Increment count for inundated cells
    inundation_counts[condition_mask] += 1

# Calculate probability of inundation for each grid cell
probability_of_inundation = inundation_counts / len(output_raster_paths)
probability_of_inundation

# Convert NumPy array to raster
output_raster = arcpy.NumPyArrayToRaster(probability_of_inundation, lower_left_corner=arcpy.Point(first_raster.extent.XMin, first_raster.extent.YMin),
                                          x_cell_size=first_raster.meanCellWidth, y_cell_size=first_raster.meanCellHeight)

# Save the raster to a new file
output_raster.save(r"F:\Miami\Miami_dade_county\probability_of_inundation.tif")

import matplotlib.pyplot as plt

# Assuming probability_of_inundation is a 2D NumPy array
plt.imshow(probability_of_inundation, cmap='viridis', extent=(first_raster.extent.XMin, first_raster.extent.XMax, first_raster.extent.YMin, first_raster.extent.YMax))
plt.colorbar(label='Probability of Inundation')
plt.title('Probability of Inundation')
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')
plt.show()


import arcpy
import numpy as np
import os

# Assuming you have a list of output raster paths from the previous step
output_raster_folder = r"F:\Miami\Miami_dade_county\raster_calculations"
output_raster_paths = [os.path.join(output_raster_folder, raster) for raster in os.listdir(output_raster_folder) if raster.endswith(".tif")]

# Initialize an empty NumPy array to store inundation counts for each grid cell
first_raster = arcpy.Raster(output_raster_paths[0])
inundation_counts = np.zeros((first_raster.height, first_raster.width))

# Iterate through the output rasters and count inundation occurrences
for output_raster_path in output_raster_paths:
    output_raster = arcpy.Raster(output_raster_path)
    # Use arcpy.RasterToNumPyArray to convert the raster to a NumPy array
    conditional_array = arcpy.RasterToNumPyArray(output_raster, nodata_to_value=0)
    # Apply the condition (output_raster > 0) to create a boolean array
    condition_mask = conditional_array > 0
    # Increment count for inundated cells
    inundation_counts[condition_mask] += 1

# Calculate probability of inundation for each grid cell
total_rasters = len(output_raster_paths)
probability_of_inundation = (inundation_counts / total_rasters) * 100  # Scale to the range 0 to 100

# Convert NumPy array to raster
output_raster1 = arcpy.NumPyArrayToRaster(probability_of_inundation, lower_left_corner=arcpy.Point(first_raster.extent.XMin, first_raster.extent.YMin),
                                          x_cell_size=first_raster.meanCellWidth, y_cell_size=first_raster.meanCellHeight)

# Save the raster to a new file
output_raster1.save(r"F:\Miami\Miami_dade_county\probability_of_inundation_0_to_100.tif")


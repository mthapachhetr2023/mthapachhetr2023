# Import necessary libraries
import arcpy
Name = "level1"
# Set the workspace and other environmental settings
arcpy.env.workspace = "F:\\Thesis_Data\\Data_Preparation\\Data_Preparation.gdb"
arcpy.env.scratchWorkspace = "F:\\Thesis_Data\\Data_Preparation\\Data_Preparation.gdb"
arcpy.env.overwriteOutput = True
#arcpy.env.addOutputToDisplay = False

# Load input data
DEMft = arcpy.Raster("Clip_DEMft")
lulc = "Statewide_Land_Use__Dissolve"


# Iterate through the input data
with arcpy.da.SearchCursor(lulc, ["SHAPE@",Name]) as cursor:
    for row in cursor:
        # Define the output raster name based on the feature's attribute
        output_name = f"F:\\Thesis_Data\\Final Data\\Individual_lc_raster\\c_{row[1].replace(' ','_')}.tif"

        # Process: Clip Raster (Clip Raster) (management)
        arcpy.management.Clip(in_raster=DEMft, 
                              rectangle=f"{row[0].extent.XMin} {row[0].extent.YMin} {row[0].extent.XMax} {row[0].extent.YMax}",
                              out_raster=output_name, 
                              in_template_dataset=row[0],
                              nodata_value = "9999", 
                              clipping_geometry="ClippingGeometry", 
                              maintain_clipping_extent="MAINTAIN_EXTENT")

# Import necessary libraries
import arcpy
from arcpy.sa import ExtractByMask

# Set the workspace and other environmental settings
arcpy.env.workspace = "F:\\Thesis_Data\\Data_Preparation\\Data_Preparation.gdb"
arcpy.env.scratchWorkspace = "F:\\Thesis_Data\\Data_Preparation\\Data_Preparation.gdb"
arcpy.env.overwriteOutput = True

# Load input data
DEMft = arcpy.Raster("Clip_DEMft")
lulc = "Statewide_Land_Use__Dissolve"
Name = "level1"  # Assuming "level1" is the name of the field you want to use

# Iterate through the input data
with arcpy.da.SearchCursor(lulc, ["SHAPE@", Name]) as cursor:
    for row in cursor:
        # Define the output raster name based on the feature's attribute
        output_name = f"F:\\Thesis_Data\\Final Data\\extractbymask\\c_{row[1].replace(' ', '_')}.tif"

        # Perform ExtractByMask operation
        out_raster = ExtractByMask(DEMft, row[0])

        # Save the output raster
        out_raster.save(output_name)

        print(f"Raster extracted and saved to: {output_name}")



import arcpy
import os
from arcpy.sa import Raster

# Set up workspace
arcpy.env.workspace = r"F:\Thesis_Data\Final Data\extractbymask"
arcpy.env.overwriteOutput = True
# Specify map frame
map_frame = "Map"

# List all raster datasets in the workspace
raster_list = arcpy.ListRasters()

# Print the list of raster datasets
if raster_list:
    for raster in raster_list:
        print(raster)
else:
    print("No raster datasets found in the workspace.")


try:
    if arcpy.CheckExtension("Spatial") == "Available":
        arcpy.CheckOutExtension("Spatial")
        print ("Checked out \"Spatial\" Extension")
    else:
        raise LicenseError
except LicenseError:
    print ("Spatial Analyst license is unavailable")
except:
    print (arcpy.GetMessages(2))

# Specify the list of selected rasters and their corresponding RMSE values
selected_rasters = ["c_Barren_Land.tif", "c_Rangeland.tif", "c_Transportation,_Communication,_and_Utilities.tif", 
                    "c_Upland_Forest.tif", "c_Urban_and_Built-Up.tif", "c_Water.tif", "c_Wetlands.tif"]
rmse_values = {"c_Barren_Land.tif": 1.28, "c_Rangeland.tif": 0.0, "c_Transportation,_Communication,_and_Utilities.tif": 0.95, 
               "c_Upland_Forest.tif": 1.38, "c_Urban_and_Built-Up.tif": 0.76, "c_Water.tif": 0.35, "c_Wetlands.tif": 1.57}

# Perform raster calculation for each selected raster
for raster_name in selected_rasters:
    # Load the raster
    ras = Raster(raster_name)
    
    # Get the corresponding RMSE value
    rmse_value = rmse_values[raster_name]
    
    # Perform raster calculation: raster + rmse_value
    result_raster = ras + rmse_value
    
    # Save the result raster to the output directory
    output_filename = r"F:\Thesis_Data\Final Data\incorporated_rmse" + "\\" + raster_name
    result_raster.save(output_filename)

    print(f"Raster calculation performed for {raster_name} with RMSE value {rmse_value}. Result saved to {output_filename}.")

# Import necessary libraries
import arcpy
from arcpy.sa import Raster

# Specify the list of selected rasters and their corresponding RMSE values
selected_rasters = ["c_Barren_Land.tif", "c_Rangeland.tif", "c_Transportation,_Communication,_and_Utilities.tif", 
                    "c_Upland_Forest.tif", "c_Urban_and_Built-Up.tif", "c_Water.tif", "c_Wetlands.tif"]
rmse_values = {"c_Barren_Land.tif": 1.28, "c_Rangeland.tif": 0.0, "c_Transportation,_Communication,_and_Utilities.tif": 0.95, 
               "c_Upland_Forest.tif": 1.38, "c_Urban_and_Built-Up.tif": 0.76, "c_Water.tif": 0.35, "c_Wetlands.tif": 1.57}

# Perform raster calculation for each selected raster
result_rasters = []
for raster_name in selected_rasters:
    # Load the raster
    ras = Raster(raster_name)
    
    # Get the corresponding RMSE value
    rmse_value = rmse_values[raster_name]
    
    # Perform raster calculation: raster + rmse_value
    result_raster = ras + rmse_value
    
    # Save the result raster to the output directory
    output_filename = r"F:\Thesis_Data\Final Data\incorporated" + "\\" + raster_name 
    result_raster.save(output_filename)

    result_rasters.append(output_filename)
    print(f"Raster calculation performed for {raster_name} with RMSE value {rmse_value}. Result saved to {output_filename}.")

# Specify the output mosaic dataset location (folder path)
output_mosaic_folder = r"F:\Thesis_Data\Final Data\mosaic"

# Mosaic the result rasters together
output_mosaic = "mosaic_output.tif"  # Output mosaic dataset name
arcpy.management.MosaicToNewRaster(result_rasters, output_mosaic_folder, output_mosaic, pixel_type="32_BIT_FLOAT", number_of_bands=1)





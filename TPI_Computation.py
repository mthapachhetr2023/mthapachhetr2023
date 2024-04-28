# Import system modules
import arcpy
from arcpy import env
from arcpy.sa import *

# Set environment settings
env.workspace = r"F:\Miami\Miami_dade_county\Default.gdb"

# Set overwriteOutput to True
arcpy.env.overwriteOutput = True
arcpy.env.addOutputsToMap = False

# Set local variables
inRaster = r"F:\Miami\Miami_dade_county\Default.gdb\dem_Northmiami_ft"
neighborhood = NbrRectangle(9, 9, "CELL")

# Execute FocalStatistics
outFocal_mean = FocalStatistics(inRaster, neighborhood, "MEAN",
                                     "")
outFocal_min = FocalStatistics(inRaster, neighborhood, "MINIMUM",
                                     "")
outFocal_max = FocalStatistics(inRaster, neighborhood, "MAXIMUM",
                                     "")
# Save the output 
outFocal_mean.save(r"F:\Miami\Miami_dade_county\Focal Statistics/focal_mean.tif")
outFocal_min.save(r"F:\Miami\Miami_dade_county\Focal Statistics/focal_min.tif")
outFocal_max.save(r"F:\Miami\Miami_dade_county\Focal Statistics/focal_max.tif")

# Set environment settings
env.workspace = r"F:\Miami\Miami_dade_county\Focal Statistics"

rasters = arcpy.ListRasters("*","tif")
for raster in rasters:
    print(raster)


import arcpy
from arcpy.sa import *

# Set environment settings
arcpy.env.workspace = r"F:\Miami\Miami_dade_county\Focal Statistics"

# List all TIFF raster files in the workspace
rasters = arcpy.ListRasters("*", "tif")
in_raster1 = rasters[0]
in_raster2 = rasters[1]
in_raster3 = rasters[2]

# Perform the calculation
OUT_TRI = RasterCalculator([in_raster1, in_raster2, in_raster3], ["x", "y", "z"],
                              "float((x - y) / (z - y))")
OUT_TRI.save(r"F:\Miami\Miami_dade_county\Focal Statistics\TRI\tri1.tif")


# Import system modules
import arcpy
from arcpy import env
from arcpy.sa import *

# Set environment settings
env.workspace = r"F:\Miami\Miami_dade_county\Default.gdb"

# Set overwriteOutput to True
arcpy.env.overwriteOutput = True
arcpy.env.addOutputsToMap = False

# Set local variables
inRaster = r"F:\Miami\Miami_dade_county\Default.gdb\dem_Northmiami_ft"
neighborhood = NbrRectangle(33, 33, "CELL")

# Execute FocalStatistics
outFocal_TPI = FocalStatistics(inRaster, neighborhood, "MEAN",
                                     "")

# Save the output 
outFocal_TPI.save(r"F:\Miami\Miami_dade_county\Focal Statistics/focal_mean_tpi.tif")


import arcpy
from arcpy.sa import *

# Set environment settings
arcpy.env.workspace = r"F:\Miami\Miami_dade_county\Focal Statistics"

# List raster files in the workspace

in_raster1 = r"F:\Miami\Miami_dade_county\Default.gdb\dem_Northmiami_ft"
in_raster2 = r"F:\Miami\Miami_dade_county\Focal Statistics/focal_mean_tpi.tif"

# Perform the calculation
OUT_TPI = RasterCalculator([in_raster1, in_raster2], ["x", "y"],
                              "float((x - y))")
OUT_TPI.save(r"F:\Miami\Miami_dade_county\Focal Statistics\TPI\tpi1.tif")



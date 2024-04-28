import arcpy

# Select features based on attribute (previous code)
arcpy.management.SelectLayerByAttribute(
    in_layer_or_view="Statewide_Land_Use_Land_Cover_20042013",
    selection_type="NEW_SELECTION",
    where_clause="LEVEL1_L_1 = 'Upland Forest'",
    invert_where_clause=None
)

# Perform spatial selection
arcpy.management.SelectLayerByLocation(
    in_layer="Extracted_for_class",
    overlap_type="INTERSECT",
    select_features="Statewide_Land_Use_Land_Cover_20042013",
    search_distance=None,
    selection_type="SUBSET_SELECTION",
    invert_spatial_relationship="NOT_INVERT"
)


# Import system modules
import arcpy

# Set environment settings
arcpy.env.workspace = "F:\\Miami\\Miami_dade_county\\Default.gdb"

# Import system modules
import arcpy
from arcpy import env
from arcpy.sa import *

# Set environment settings
env.workspace = r"F:\\Miami\\Miami_dade_county\\Default.gdb"

# Set local variables
inRaster = r"F:\Miami\Miami_dade_county\Default.gdb\dem_correction_mean"
reclassField = "VALUE"
remap_ranges = RemapRange([[-35.6349, 0, 0],
                          [0, 15.0196, 1]])
#remap_ranges = RemapRange([[0, 0.5, 1],
                          #[0.5, 0.6, 2], [0.6, 0.7, 3], [0.7, 0.8, 4], [0.8, 0.9, 5],
                                               #  [0.9, 0.95, 6], [0.95, 1, 7]])
# Execute Reclassify
out_GS1 = Reclassify(inRaster, reclassField, remap_ranges, "NODATA")

# Save the output 
out_GS1.save(r"F:\Miami\Miami_dade_county\Reclassify\gss_re1.tif")


# Description: Converts a raster dataset to polygon features.

# Import system modules
import arcpy

# Set environment settings
arcpy.env.workspace = r"F:\\Miami\\Miami_dade_county\\Default.gdb"

# Set local variables
inRaster = r"F:\Miami\Miami_dade_county\Reclassify\FAU_reclass.tif"
outPolygons = r"F:\Miami\Miami_dade_county\Reclassify\Gss_reclass.shp"
field = "VALUE"

# Run RasterToPolygon
arcpy.conversion.RasterToPolygon(inRaster, outPolygons, "NO_SIMPLIFY", field)



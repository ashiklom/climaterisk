#!/usr/bin/env python

from pathlib import Path

import rasterio

import geopandas as gpd
import pyproj

target_dir = Path("./clipped")
target_dir.mkdir(exist_ok = True)

# Read shapefile
md_shape = gpd.read_file("nasa-md-shapefile/MD_bourndary.shp")
md_shape_wgs84 = md_shape.to_crs("epsg:4326")

# md_shape_wgs84.bounds
# Bounds are 81W to 73.9W; 36N to 41N
# That puts Maryland in the MERIT box: w090n60
data_dir = Path("/discover/nobackup/projects/lis/LS_PARAMETERS/topo_parms/MERIT/")
merit_str = "merit_w090n60"
demfile = data_dir / (merit_str + ".dem")

dem = rasterio.open(demfile)
dem_masked, dem_transform = rasterio.mask.mask(dem, md_shape_wgs84.geometry, crop=True)

result_meta = dem.meta.copy()
result_meta.update({
    "driver": "GTiff",
    "height": dem_masked.shape[1],
    "width": dem_masked.shape[2],
    "transform": dem_transform,
    "crs": pyproj.CRS("epsg:4326")
})

with rasterio.open("./clipped/MERIT_DEM.tif", "w", **result_meta) as f:
    f.write(dem_masked)

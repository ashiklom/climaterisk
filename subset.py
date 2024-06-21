#!/usr/bin/env python

from pathlib import Path
from multiprocessing import Pool

import xarray as xr
import rioxarray

import geopandas as gpd

def process_file(fname):
    target_dir = Path("./clipped")
    target_dir.mkdir(exist_ok = True)

    # Read shapefile
    md_shape = gpd.read_file("nasa-md-shapefile/MD_bourndary.shp")
    md_shape_wgs84 = md_shape.to_crs("epsg:4326")

    outfile = target_dir / fname.name
    if outfile.exists():
        print(f"{outfile} exists. Skipping.")
        return outfile

    print(f"Processing {fname} --> {outfile}")

    # Read dataset and set spatial stuff
    dat = xr.open_dataset(fname, engine = "h5netcdf")
    dat.rio.write_crs("epsg:4326", inplace=True)
    dat.rio.set_spatial_dims("lon", "lat", inplace=True)

    md = dat.rio.clip(md_shape_wgs84.geometry.values, drop = True)
    md.to_netcdf(outfile)
    return outfile

if __name__ == '__main__':
    data_dir = Path("/discover/nobackup/smahanam/forMukul/")
    assert data_dir.exists()

    # All history files
    histfiles = sorted(data_dir.glob("HISTORICAL_*.nc4"))
    ssp245 = sorted(data_dir.glob("SSP245_*.nc4"))
    ssp585 = sorted(data_dir.glob("SSP585_*.nc4"))
    allfiles = histfiles + ssp245 + ssp585

    with Pool() as pool:
        pool.map(process_file, allfiles)

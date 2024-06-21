best_fname = "/discover/nobackup/smahanam/forMukul/Best5_CMIP6_model.nc4"




# Integer code
best5 = xr.open_dataset(best_fname, engine = "h5netcdf")

best1 = xr.open_dataset("/discover/nobackup/smahanam/forMukul/Best_CMIP6_model.nc4", engine = "h5netcdf")

best1.best_model.min()

best1.best_model.values

# Upload to testbucket cmip6

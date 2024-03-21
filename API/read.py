import rasterio
#Testing code to process the raster file which has been downloaded.
raster = rasterio.open("./API/raster_data.tif")
print(raster.meta)
library(gblidar)
library(sf)
options(gblidar.progress = FALSE)
#> Linking to GEOS 3.12.1, GDAL 3.8.3, PROJ 9.3.1; sf_use_s2() is TRUE
if (rlang::is_installed("terra")) {
  library(terra)
  options(gblidar.out_raster_type = "SpatRaster")
}
#> terra 1.7.71
args = commandArgs(trailingOnly=TRUE)
x <- as.numeric(args[1])
y <- as.numeric(args[2])

reqBox <- st_point(c(x, y)) |>
  st_buffer(2000) |>
  st_sfc() |>
  st_set_crs(27700)

catalog <- eng_search(reqBox)

DTM_catalog <- catalog |>
  filter_catalog(
    product == "LIDAR Composite DTM",
    resolution == 2,
    year == 2022
  )

#print(DTM_catalog)
#> Data Catalog
#> # A tibble: 1 × 5
#>   product             resolution  year filenames urls     
#>   <chr>                    <dbl> <int> <list>    <list>   
#> 1 LIDAR Composite DTM          2  2022 <chr [9]> <chr [9]>
#> AOI Geometry
#> Geometry set for 1 feature 
#> Geometry type: POLYGON
#> Dimension:     XY
#> Bounding box:  xmin: 319633 ymin: 505181 xmax: 323633 ymax: 509181
#> Projected CRS: OSGB36 / British National Grid
#> POLYGON ((323633 507181, 323630.3 507076.3, 323...
#> Tile Names
#> [1] "NY10NE" "NY20NW"
raster <- merge_assets(DTM_catalog, mask = TRUE)
rf <- writeRaster(raster, filename=file.path("./API/raster_data.tif"), datatype='INT4S', overwrite=TRUE)
print(rf)
#plot(scafell_raster, col = grDevices::hcl.colors(50, palette = "Sunset"))
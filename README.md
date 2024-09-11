# CSVMappy
Takes 2 column CSV (long,lat) from my GMapsJSONtoCSV project (or any 2 column csv with long,lat) and makes a map using Python and QGIS.

<img src="https://i.imgur.com/mYvV8Y2.png" alt="Completed Map" title="Completed Map">

# How to use:
  1. Download this version of QGIS: https://www.qgis.org/downloads/QGIS-OSGeo4W-3.34.10-1.msi
      * Express installation is fine
  2. File setup should be as seen here:
      *  ```C:\\MapProject\\``` is the root
      *  Either use my GMapsJSONtoCSV script or get 2 column lat/long CSV and name it either latlongdata.csv or latlongdata_no_duplicates.csv (or don't, or use my other script, or whatever)
      *  ```C:\\MapProject\\shapefiles``` is the next folder you'll need
          *  add a 'counties', 'roads', and 'states' folder inside shapefiles
          *  inside the appropriate folder, download and place the following files: ```ne_10m_admin_2_counties, ne_10m_roads, ne_10m_admin_1_states_provinces``` (Need all: cpg, dbf, prj, shp, shx)
          *  GitHub link: https://github.com/nvkelso/natural-earth-vector/tree/master
  3. Navigate to your ```C:\OSGeo4W\bin``` folder and edit ```python-qgis-ltr.bat```
      * Remove the ```python %*``` and change it to:
          ```
          python "C:\OSGeo4W\mapbuilder.py"
          pause
          ```
  4. Run the batch file
  5. Wow now you have an ugly map!

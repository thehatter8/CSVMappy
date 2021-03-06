import sys
import timeit

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QColor
from qgis.core import QgsApplication,QgsProject,QgsMapSettings,QgsVectorLayer,QgsMapRendererParallelJob,QgsSimpleFillSymbolLayer,QgsSymbol,QgsRendererCategory,QgsCategorizedSymbolRenderer,QgsGeometry

start = timeit.default_timer()
# Initiate Application
QgsApplication.setPrefixPath("C:\\OSGeo4W\\apps\\qgis", True)
qgs = QgsApplication([], False)
qgs.initQgis()
print("Application initiated")

# Start project instance
project = QgsProject.instance()

# Build layer from CSV and check validity
uri = 'file:///C:\\{SOMEDIr}\\MapProject\\finalNoDupes.csv?delimiter={}&xField={}&yField={}&crs={}'.format(',', 'longitude', 'latitude',{'epsg:4326'})
csvLayer = QgsVectorLayer(uri, 'Locations', 'delimitedtext')
roadLayer = QgsVectorLayer('C:\\{SOMEDIR}\\MapProject\\shapefiles\\roads\\ne_10m_roads.shp', 'Roads', 'ogr')
countyLayer = QgsVectorLayer('C:\\{SOMEDIR}\\MapProject\\shapefiles\\counties\\ne_10m_admin_2_counties.shp', 'Counties' ,'ogr')
stateLayer = QgsVectorLayer('C:\\{SOMEDIR}\\MapProject\\shapefiles\\states\\ne_10m_admin_1_states_provinces.shp', 'States', 'ogr')

if csvLayer.isValid():
    print('CSV Layer successfully imported')
else:
    print('CSV Import failed')
if roadLayer.isValid():
    print('Roads successfully imported')
else:
    print('Roads Import failed')  
if stateLayer.isValid():
    print('States successfully imported')
else:
    print('States Import failed')  
if countyLayer.isValid():
    print('Counties successfully imported')
else:
    print('Counties Import failed')

# Adding map layers
project.addMapLayer(csvLayer)
project.addMapLayer(roadLayer)
project.addMapLayer(stateLayer)
project.addMapLayer(countyLayer)


# Building county layer with one renderer before it gets locked below
# This makes every county transparent before visited counties get added as black below

countyLine = QgsSimpleFillSymbolLayer.create({'outline_color':'0,0,0', 'outline_width':'0.25'})
countySymbols = countyLayer.renderer().symbol()
countySymbols.appendSymbolLayer(countyLine)
countySymbols.setColor(QColor('transparent'))
countyLayer.triggerRepaint()

# Finding intersects between CSV and County layers - Takes ~155+ seconds

# Check for points contained within specific counties
overlaps = []
alloverlaps = []
for countyFeature in countyLayer.getFeatures():
    for pointFeature in csvLayer.getFeatures():
        if countyFeature.geometry().contains(pointFeature.geometry()):
            if countyFeature[2] in overlaps:
                alloverlaps.append(countyFeature[2])
                continue
            overlaps.insert(0,countyFeature[2])
alloverlaps.sort()
overlap = []
outs = dict((i, alloverlaps.count(i)) for i in alloverlaps)
print(outs)

# Paint counties which contain a point from csvLayer
categories = []
fni = countyLayer.fields().indexFromName('ADM2_CODE')
uniquevals = countyLayer.uniqueValues(fni)
for uniqueVal in uniquevals:
    if uniqueVal in overlaps:
        symbol = QgsSymbol.defaultSymbol(countyLayer.geometryType())
        layer_style = {}
        layer_style['color'] = '0, 255, 0'
        symbol_layer = QgsSimpleFillSymbolLayer.create(layer_style)
        if symbol_layer is not None:
            symbol.changeSymbolLayer(0, symbol_layer)
        category = QgsRendererCategory(uniqueVal, symbol, str(uniqueVal))
        categories.append(category)
renderer = QgsCategorizedSymbolRenderer('ADM2_CODE', categories)
countyLayer.setRenderer(renderer)
countyLayer.triggerRepaint()

# Set layer colors and create some outlines
csvSymbols = csvLayer.renderer().symbol()
csvSymbols.setColor(QColor('red'))
csvLayer.triggerRepaint()

roadSymbols = roadLayer.renderer().symbol()
roadSymbols.setColor(QColor('blue'))
roadLayer.triggerRepaint()

stateLine = QgsSimpleFillSymbolLayer.create({'outline_color':'0,0,0', 'outline_width':'1'})
stateSymbols = stateLayer.renderer().symbol()
stateSymbols.appendSymbolLayer(stateLine)
stateSymbols.setColor(QColor(254,232,200))
stateLayer.triggerRepaint()

# Set layer order and output options

options = QgsMapSettings()
options.setLayers([csvLayer, roadLayer, countyLayer, stateLayer])
options.setBackgroundColor(QColor("transparent"))
options.setOutputSize(QSize(3840, 2160))
options.setExtent(csvLayer.extent())

mapLayers = project.mapLayers()
for x, y in enumerate(mapLayers): print('Layer ' + str(x+1) + ': '+ str(y.split('_')[0]))

# Start image render

render = QgsMapRendererParallelJob(options)
image_location = 'C:\\{SOMEDIR}\\MapProject\\file.png'
render.start()
render.waitForFinished()
img = render.renderedImage()
img.save(image_location, 'png')
print('Map has been rendered to: ' + image_location)

stop = timeit.default_timer()
print('Runtime: ',stop-start)

# End of project code
qgs.exitQgis()
print("Exiting")

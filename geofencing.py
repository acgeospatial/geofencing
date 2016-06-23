
### Program to model geofences in QGIS!
### Written / Complied together by Andrew Cutts www.acgeospatial.co.uk
### Python 2.7
### Stopwatch method adapted from http://codereview.stackexchange.com/questions/26534/is-there-a-better-way-to-count-seconds-in-python
### Createpoint method adapted from http://gis.stackexchange.com/questions/86812/how-to-draw-polygons-from-the-python-console
### point_in_poly method apated from http://geospatialpython.com/2011/01/point-in-polygon.html
### Many thanks!

### Usage
### 1. Open blank QGIS project
### 2. Open python console
### 3. Set projection to British grid, EPSG code 277000
### 4. Use the map to x = 512915 y = 120728 (first coordinate to be plotted), I use Openstreetmap to zoom out a bit shots will increment 12.5m
### 5. Run the script (you could add the shapefile boundary if you want)

import time
def stopwatch(seconds,d,lspoint):
	start = time.time()
	time.clock()    
	elapsed = 0
	flag = False
	num = 0
	while elapsed < seconds:
		elapsed = time.time() - start
		print "%02d" % elapsed
		if elapsed > d[num] and elapsed < d[num+1] and flag == False:
			x = lspoint[num][0]
			y = lspoint[num][1]
			createpoint(x,y)
			flag = True
			print "Shot Taken"
			print point_in_poly(x,y,polygon)
		if elapsed > d[num+1]:
			print "Shot Taken"
			flag == False
			num = num+1
			x = lspoint[num][0]
			y = lspoint[num][1]
			createpoint(x,y) 
			print point_in_poly(x,y,polygon)	
		time.sleep(1)  

def createpoint(x,y):
    crs = "point?crs=epsg:27700&field=id:integer"
    layer =  QgsVectorLayer(crs, 'points' , "memory")
    pr = layer.dataProvider() 	
    pt = QgsFeature()
    point1 = QgsPoint(x,y)
    pt.setGeometry(QgsGeometry.fromPoint(point1))
    pr.addFeatures([pt])
    # update extent of the layer
    layer.updateExtents()
    # add the second point
    pt = QgsFeature()
    QgsMapLayerRegistry.instance().addMapLayers([layer])

def point_in_poly(x,y,poly):

    n = len(poly)
    inside = False

    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x,p1y = p2x,p2y

    return inside


#### define the polygon
polygon = [(512882.78819722467,120811.83924772343),(512960.84437170526,120809.7007223952),(512960.84437170526,120809.7007223952),(512959.77510904113,120754.09906386107),(512882.78819722467,120756.2375891893)]
	
#### set how long the script will run (70 seconds will get you in and out of geofence)
time_seconds = 70
#### first coordinate
x = 512915
y = 120728
#### time intervals, 10 seconds between shots / or points
intervals = int(time_seconds / 10)
lspoint = []
#### build the list of coordinates to be plotted
for i in range(0,intervals+1):
	y1 = y + (i*12.5)
	lspoint.append([x,y1])

#### to build the blocks of time in intervals, so we know the number of intervals (default is 7), 
#### we need a list of time intervals [0,10,20,30 etc] to check against the clock this list is d, f is the gap ie 10 seconds, a is starting point (0)
### b is the number of intervals + 1 becuase the code will check the the next in the list
f = 10
a = 0
b = intervals+1
d = [x * f for x in range(a, b)]

### Run the stopwatch, or start the program!
stopwatch(time_seconds,d,lspoint)

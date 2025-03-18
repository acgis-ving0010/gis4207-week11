import sys
import time
import arcpy
import os

# create a new polyline feature class 
# read coordinates from text file
# make it a cli script

# in_txt filepath (to read in)
# out_shp filepath (to write to)



# use strip or rstrip to remove \n

# do not use IDs in txt.file to set OID -- just use it as a flag that a new line is about to begin

# read in txt file
# get x and y coordinates

# use arcpy.Array and arcpy.Point to construct arcpy.Polyline geometres
# use arcpy.da.InsertCursor to add polylines to new feature class

# for each polyline create an array of points

# in_txt = r"C:\ACGIS\gis4207_prog\data\test_canada.txt"
# out_fc = r"C:\ACGIS\gis4207_prog\data\test_output_canada.shp"

def main():
    arcpy.env.overwriteOutput = True
    wkid = 4326
    n= len(sys.argv)

    if n!=3:
        print("Usage:   geom_obj01.py <in_txt> <out_shp>")
        sys.exit()

    in_txt = sys.argv[1]
    out_fc = sys.argv[2]

    create_polyline_fc(in_txt, out_fc, wkid)

def create_polyline_fc(input, output, sr):
    with open(input, 'r') as f:
        lines = f.readlines()
        stripped = [l.rstrip('\n') for l in lines]
        stripped_split = [l.split(' ') for l in stripped]
    
    # parse txt file
    # use IDs as a flag that a new line is about to begin

    stored_pts = {}
    id = 0
    for l in stripped_split:

        if len(l) == 1:
            # flag new polyline
            id = l[0]
            stored_pts[id] = []

        elif len(l) == 2:
            # create arcpy.Point from these coordinates
            pt = arcpy.Point(l[0], l[1])
            stored_pts[id].append(pt)

        else:
            print("unexpected")
            # skip and move on?? 
            continue

    
    # create an array for each ID in dictionary from list of points
    polylines = []
    for key,value in stored_pts.items():
        print(f"Creating polyline for ID {key}")
        new_polyline = arcpy.Polyline(arcpy.Array(value))
        polylines.append(new_polyline)

    # save polylines in list of polylines to out shp file
    sr = arcpy.SpatialReference(sr)

    ws = os.path.dirname(output)
    arcpy.env.workspace = ws
    if not arcpy.Exists(os.path.dirname(output)):
        os.mkdir(os.path.dirname(output))
    if not arcpy.Exists(output):
        arcpy.management.CreateFeatureclass(os.path.dirname(output), os.path.basename(output), "POLYLINE")


    arcpy.management.CreateFeatureclass("C:/ACGIS/gis4207_prog/data/test_output", "test_canada.shp", "POLYLINE")

    with arcpy.da.InsertCursor(output, ["SHAPE@"]) as cursor:
        for p in polylines:
            cursor.insertRow([p])

if __name__ == "__main__":
    main()
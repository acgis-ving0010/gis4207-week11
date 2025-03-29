import sys
import time
import arcpy
import os

def main():
    arcpy.env.overwriteOutput = True
    wkid = 4326
    n= len(sys.argv)

    if n!=3:
        print("Usage:   geom_obj01.py <in_txt> <out_shp>")
        sys.exit()

    in_txt = sys.argv[1]
    out_fc = sys.argv[2]

    start = time.perf_counter()
    create_polyline_fc(in_txt, out_fc, wkid)
    print(f"Time elapsed: {time.perf_counter() - start:.1f} s")
    
def create_polyline_fc(input, output, sr):
    with open(input, 'r') as f:
        lines = f.readlines()
        stripped = [l.rstrip('\n') for l in lines]
        stripped_split = [l.split(' ') for l in stripped]
    
    # parse txt file
    # use IDs as a flag that a new line is about to begin
    stored_pts = {}
    for l in stripped_split:
        if len(l) == 1:
            # flag new polyline
            id = l[0]
            stored_pts[id] = []
        elif len(l) == 2:
            # create arcpy.Point from these coordinates
            # add to the value for key of last known ID in dictionary
            pt = f"{l[0]} {l[1]}"
            stored_pts[id].append(pt)
        else:
            print("unexpected")
            # skip and move on?? 
            continue

    # create a polyline for each ID using array from list of line ID points
    polylines = []
    
    sp_ref = arcpy.SpatialReference(sr)

    for key,value in stored_pts.items():
        print(f"Creating wkt linestring for ID {key}")
        pts_list = value
        new_linestring = f"LINESTRING ({', '.join(pts_list)})"
        new_polyline = arcpy.FromWKT(new_linestring)
        polylines.append(new_polyline)

    # save polylines in list of polylines to out shp file
    ws = os.path.dirname(output)
    arcpy.env.workspace = ws
    if not arcpy.Exists(os.path.dirname(output)):
        os.mkdir(os.path.dirname(output))
    if not arcpy.Exists(output):
        arcpy.management.CreateFeatureclass(os.path.dirname(output), 
                                            os.path.basename(output), 
                                            geometry_type = "POLYLINE", 
                                            spatial_reference=sp_ref)

    with arcpy.da.InsertCursor(output, ["SHAPE@"]) as cursor:
        for p in polylines:
            cursor.insertRow([p])

if __name__ == "__main__":
    main()
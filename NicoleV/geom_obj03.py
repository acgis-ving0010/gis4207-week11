import arcpy
import pandas as pd

stops_workspace = None
stop_name = None
stop_id_fc = None
dissemination_area_fc = None
da_population_field = None

def get_stop_id_to_da_data():
    stop_id_to_buffer = {}
    stop_id_field = arcpy.AddFieldDelimiters(stops_workspace, 'stop_id')
    stop_name_field = arcpy.AddFieldDelimiters(stops_workspace, 'stop_name')
    where_clause = f"{stop_id_field}='CI380'"
    where_clause = f"{stop_name_field} LIKE '%{stop_name}%'"
    arcpy.env.workspace = stops_workspace

# select bus stops where stop_id is CI380 and stop_name is GLADSTONE
    with arcpy.da.SearchCursor(stop_id_fc, 
                           ['stop_id','SHAPE@', 'stop_name'], 
                           where_clause=where_clause) as cursor:
        for row in cursor:
            stopid = row[0]
            shape = row[1]
        # create a 150m bugger for each stop id
            stop_id_to_buffer[stopid] = shape.buffer(150)

    stop_id_to_DA_data = {}
    for stopid in stop_id_to_buffer:
        stop_buffer = stop_id_to_buffer[stopid]
        intersected_da_data = []
        ws = r'C:\ACGIS\gis4207_prog\data\Ottawa\OttawaDA_UTM'
        arcpy.env.workspace = ws
    # for each of the buffered stops, determine what DAs it overlaps with
    # keep DACODE, the population, the area of the intersection, and the area of the DA
        with arcpy.da.SearchCursor(dissemination_area_fc, ['DACODE', da_population_field,'SHAPE@']) as cursor:
            for row in cursor:            
                da_code = row[0]   
                population = row[1]
                da_poly = row[2] 
                dimension = 4  # Resulting geometry is a polygon
                if stop_buffer.overlaps(da_poly) == True:
                    intersect_poly = stop_buffer.intersect(da_poly, 
                                                       dimension)
                    data = (da_code, 
                        population, 
                        int(intersect_poly.area),
                        int(da_poly.area))
                    intersected_da_data.append(data)
        stop_id_to_DA_data[stopid] = intersected_da_data

    for stop_id in stop_id_to_DA_data:
        for data in stop_id_to_DA_data[stop_id]:
            print(stop_id, data)

    return stop_id_to_DA_data   

def write_report(out_csv):   
    data_dict = get_stop_id_to_da_data()
    df = pd.DataFrame(columns=["STOP ID", "DACODE", "DA_POPULATION", "%DA AREA", "STOP_POP"])

    for stop_id in data_dict:
        for data in data_dict[stop_id]:
            da_area_prop = data[2]/data[3]
            stop_pop = data[1] * da_area_prop
            new_row = pd.DataFrame({"STOP ID":[stop_id], 
                                    "DACODE": [data[0]], 
                                    "DA_POPULATION" : [data[1]], 
                                    "%DA AREA" : [da_area_prop*100], 
                                    "STOP_POP" :[int(stop_pop)]})
            df = pd.concat([df, new_row], ignore_index=True)

    df.to_csv(out_csv, index=False)
import geom_obj03 as g3

g3.stops_workspace = r'C:\ACGIS\gis4207_prog\data\Ottawa\Stops'
g3.stop_name = 'GLADSTONE'
g3.stop_id_fc = 'STOPS_UTM'
g3.dissemination_area_fc = 'OttawaDA_UTM'
g3.da_population_field = 'POP_2016'

def test_get_stop_id_to_da_data():    
    expected = [('1708', 837, 32171, 115926), ('1709', 1387, 38465, 105071), ('1710', 622, 47, 53334)]
    results = g3.get_stop_id_to_da_data()
    actual = results["CH080"]
    assert actual == expected
import geom_obj03 as g3

g3.stops_workspace = r'..\..\..\..\data\Ottawa\Stops'
g3.stop_name = 'GLADSTONE'
g3.stop_id_fc = 'STOPS_UTM'
g3.dissemination_area_fc = 'OttawaDA_UTM'
g3.da_population_field = 'POP_2016'

def test_get_stop_id_to_da_data():    
    expected = [('0367', 570, 7529, 76511), ('0368', 538, 59343, 92688), ('0313', 525, 3813, 111857)]
    results = g3.get_stop_id_to_da_data()
    actual = results["CI380"]
    assert actual == expected
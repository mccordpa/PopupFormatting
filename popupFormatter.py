import arcpy
import feature_dictionary

# get_layer returns the feature class of interest - Run when formatting feature classes
def get_layer(project_location, map_name, layer_name):
    project_obj = arcpy.mp.ArcGISProject(project_location)
    map_obj = project_obj.listMaps(map_name)[0]
    layer_lst = map_obj.listLayers()
    for lyr in layer_lst:
        if lyr.name == layer_name:
            return lyr

# get_table_layer returns the table of interest - Run when formatting tables
def get_table_layer(project_location, map_name, layer_name):
    project_obj = arcpy.mp.ArcGISProject(project_location)
    map_obj = project_obj.listMaps(map_name)[0]
    table_lst = map_obj.listTables()
    for lyr in table_lst:
        if lyr.name == layer_name:
            return lyr

def get_fields(in_fc, fields_to_include):
    """ Gets field name and field alias for the provided feature class

    Arguments:
        in_fc {feature class} -- input feature class
        fields_to_exclude {Dictionary} -- idictionary where the key is the field name to include and the value is the order it should appear in popup

    Returns:
        dictionary -- field names, field aliases, and order in which field should appear in popup. dictionary[field name] = [field alias, popup order] --> {'Field Name': 'Field Alias', 'Popup Order'}
    """
    field_dict = {}
    for field in arcpy.ListFields(in_fc):
        for key, value in fields_to_include.items():
            if field.name == key:
                field_dict[field.name] = [field.aliasName]
                #append the popup order value as a second value (within a list) in key, value pair
                field_dict[field.name] += [value]
    for key, value in field_dict.items():
        if key == "diameter":
            value[0] = "Diameter"
    for key, value in field_dict.items():
        if key == "Shape__Length":
            value[0] = "Pipe Length (ft)"
    for key, value in field_dict.items():
        if key == "US_Manhole":
            value[0] = "Upstream Manhole"
    for key, value in field_dict.items():
        if key == "DS_Manhole":
            value[0] = "Downstream Manhole"
    for key, value in field_dict.items():
        if key == "INV_IN1":
            value[0] = "Invert - In" 
    for key, value in field_dict.items():
        if key == "INV_OUT1":
            value[0] = "Invert - Out"
    for key, value in field_dict.items():
        if key == "assetid":
            value[0] = "Asset ID"
    for key, value in field_dict.items():
        if key == "material":
            value[0] = "Material"
    for key, value in field_dict.items():
        if key == "lifecyclestatus":
            value[0] = "Lifecycle Status"
    for key, value in field_dict.items():
        if key == "ownedby":
            value[0] = "Owned By"
    for key, value in field_dict.items():
        if key == "rimelev":
            value[0] = "Rim Elevation"
    for key, value in field_dict.items():
        if key == "invertelev":
            value[0] = "Invert ELevation"
    #sort dictionary in ascending order by popup order value
    #*Note: sorted function returns a list, which then needs to be converted back to a dictionary
    #* RESOURCE: https://stackoverflow.com/questions/21992842/sorting-a-dictionary-by-second-value
    sorted_list = sorted(field_dict.items(), key=lambda x:x[1][1])
    sorted_field_dict = dict(sorted_list)

    return sorted_field_dict

def format_popup(field_dict, color):
    """iterate throught dictionary of field alias, field names, and popup order and parses them into table row
    html format

    Arguments:
        field_dict {[dictionary]} -- [field alias as keys, field names as values, popup order as values]
    """
    popup_start = """
    <div>
    <table>
    <tbody>
    """

    popup_finish = """
    </tbody>
    </table>
    </div>
    """

    odd_row = """
    <tr>
        <td style="text-align: left; padding: 5px;">{f_alias}</td>
        <td style="text-align: left; font-weight: bold; width: 160px; padding: 5px;">{{{f_name}}}</td>
     </tr>
    """
    even_row = """<tr style="background-color: {color}">
        <td style="text-align: left; padding: 5px;">{f_alias}</td>
        <td style="text-align: left; font-weight: bold; width: 160px; padding: 5px;">{{{f_name}}}</td>
    </tr>
    """
    print(popup_start)
    for index, fld_name in enumerate(field_dict.keys()):
        
        if index % 2 == 0:
            print(
                even_row.format(
                    color=color, f_alias=field_dict[fld_name][0], f_name=fld_name
                )
            )
        else:
            print(odd_row.format(f_alias=field_dict[fld_name][0], f_name=fld_name))
    print(popup_finish)


if __name__ == "__main__":
    input_project = r"P:\8000_8100\8015220010_North_Ridgeville_GIS_Phase_2\_GIS\_Working\McCord\CleaningUpPopups\CleaningUpPopups\CleaningUpPopups.aprx"
    map_name = "Storm"
    dk_grey = "#3b3a3a"
    lt_grey = "#f2f2f2"
    layer_name = "Retention Basins"
    # If feature class, use get_layer function
    layer_object = get_layer(input_project, map_name, layer_name)

    # If table, use get_table_layer function
    #layer_object = get_table_layer(input_project, map_name, layer_name)
    #gets dictionary of field names and popup order from separate file within same folder called feature_dictionary.py
    #the dictionary within this file is called feature_dict
    keep_dict = feature_dictionary.feature_dict[layer_name]
    flds_dict = get_fields(layer_object, keep_dict)
    format_popup(flds_dict, lt_grey)

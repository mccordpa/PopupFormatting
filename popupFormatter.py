import arcpy

# get_layer returns the feature class of interest - Run when formatting feature classes
def get_layer(project_location, map_name, layer_name):
    project_obj = arcpy.mp.ArcGISProject(project_location)
    map_obj = project_obj.listMaps(map_name)[0]
    layer_lst = map_obj.listLayers()
    table_lst = map_obj.listTables()
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


def get_fields(in_fc, fields_to_exclude):
    """ Gets field name and field alias for the provided feature class

    Arguments:
        in_fc {feature class} -- input feature class
        fields_to_exclude {List} -- list of fields to exclude in pop up

    Returns:
        dictionary -- field names and field alias. dictionary[field name] = field alias --> {'Field Name': 'Field Alias'}
    """
    field_dict = {}
    for field in arcpy.ListFields(in_fc):
        if field.name not in fields_to_exclude:
            field_dict[field.name] = field.aliasName
    return field_dict


def format_popup(field_dict, color):
    """iterate throught dictionary of field alias and field names and parses them into table row
    html format

    Arguments:
        field_dict {[dictionary]} -- [field alias as keys, field names as values]
    """
    start_tags = """
    <div>
        <table>
            <tbody>
    """

    end_tags = """
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
    print(start_tags)

    for index, fld_name in enumerate(field_dict.keys()):
        
        if index % 2 == 0:
            print(
                even_row.format(
                    color=color, f_alias=field_dict[fld_name], f_name=fld_name
                )
            )
        else:
            print(odd_row.format(f_alias=field_dict[fld_name], f_name=fld_name))

    print(end_tags)

if __name__ == "__main__":
    input_project = r"P:\0166_0200\0190220030_RH_Asset_Mgmt_Data_Integration\_GIS\_Working\McCord\RH_MACP_PACP\RH_MACP_PACP.aprx"
    map_name = "Utility Viewer - Map"
    dk_grey = "#3b3a3a"
    lt_grey = "#f2f2f2"
    layer_name = "SewerManhole - MACP_RehabRecommendation"
    # If feature class, use get_layer function
    #layer_object = get_layer(input_project, map_name, layer_name)

    # If table, use get_table_layer function
    layer_object = get_table_layer(input_project, map_name, layer_name)
    # exclude_fields = ['OBJECTID', 'OBJECTID_1', 'GlobalID', 'ESRIGNSS_RECEIVER', 'ESRIGNSS_H_RMS', 'ESRIGNSS_V_RMS', 'ESRIGNSS_LATITUDE', 'ESRIGNSS_LONGITUDE', 'ESRIGNSS_ALTITUDE', 'ESRIGNSS_PDOP', 'ESRIGNSS_HDOP', 'ESRIGNSS_VDOP', 'ESRIGNSS_FIXTYPE', 'ESRIGNSS_CORRECTIONAGE', 'ESRIGNSS_STATIONID', 'ESRIGNSS_NUMSATS', 'ESRIGNSS_FIXDATETIME', 'ESRIGNSS_AVG_H_RMS', 'ESRIGNSS_AVG_V_RMS', 'ESRIGNSS_AVG_POSITIONS', 'ESRIGNSS_H_STDDEV', 'EOSLASER_METHOD', 'EOS_ORTHO_HEIGHT', 'EOS_UNDULATION', 'EOS_GEOID_MODEL', 'EOSLASER_DEVICE', 'EOSLASER_GNSSANTH', 'EOSLASER_DEVICEH', 'EOSLASER_MAGDEC', 'EOSLASER_CTL1_LAT', 'EOSLASER_CTL1_LON', 'EOSLASER_CTL1_ALT', 'EOSLASER_CTL1_HRMS', 'EOSLASER_CTL1_SATS', 'EOSLASER_CTL1_FIXTYPE', 'EOSLASER_CTL1_AGE', 'EOSLASER_CTL1_DIFFID', 'EOSLASER_CTL1_AVG', 'EOSLASER_CTL1_SLDIST', 'EOSLASER_CTL1_AZI', 'EOSLASER_CTL1_SL', 'EOSLASER_BS_LAT', 'EOSLASER_BS_LON', 'EOSLASER_BS_ALT', 'EOSLASER_BS_HRMS', 'EOSLASER_BS_SATS', 'EOSLASER_BS_FIXTYPE', 'EOSLASER_BS_AGE', 'EOSLASER_BS_DIFFID', 'EOSLASER_BS_AVG', 'EOSLASER_BS_SLDIST', 'EOSLASER_BS_AZI', 'EOSLASER_BS_SL', 'EOSLASER_BS_TRUEAZI', 'EOSLASER_BS_AZICORR', 'EOSLASER_CTL2_LAT', 'EOSLASER_CTL2_LON', 'EOSLASER_CTL2_ALT', 'EOSLASER_CTL2_HRMS', 'EOSLASER_CTL2_SATS', 'EOSLASER_CTL2_FIXTYPE', 'EOSLASER_CTL2_AGE', 'EOSLASER_CTL2_DIFFID', 'EOSLASER_CTL2_AVG', 'EOSLASER_CTL2_SLDIST', 'EOSLASER_CTL2_AZI', 'EOSLASER_CTL2_SL', 'Shape']
    #exclude_fields = ['OBJECTID', 'Shape', 'InvCreated_user', 'InvCreated_date', 'InvLast_edited_user', 'InvLast_edited_date', 'InvOBJECTID', 'InspCreated_user', 'InspCreated_date', 'InspLast_edited_user', 'created_user', 'created_date', 'last_edited_user', 'last_edited_date']
    exclude_fields = ['objectid', 'globalid', 'created_user', 'created_date', 'last_edited_user', 'last_edited_date', 'shape', 'parentguid', 'parentguid__']
    flds_dict = get_fields(layer_object, exclude_fields)
    format_popup(flds_dict, lt_grey)




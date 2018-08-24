from __future__ import print_function
from __future__ import division
import os
import argparse
import folium
import pandas as pd
import geopandas as gpd
from geopandas import GeoDataFrame
import matplotlib as mpl
import matplotlib.cm as cm
from shapely.geometry import Point
from branca.colormap import linear


__author__ = 'Colin Anthony'


def csv_to_geo_dataframe(infile):
    csv_file = pd.read_csv(infile, sep=',', header=0)
    # process dataframes
    geo_df = pd.DataFrame(csv_file)
    geo_df.fillna(method='ffill', inplace=True)
    geometry_infile = [Point(xy) for xy in
                       zip(geo_df["longitude"], geo_df["latitude"])]
    geo_df = geo_df.drop(['longitude', 'latitude'], axis=1)
    crs = {'init': 'epsg:4326'}
    geo_df = GeoDataFrame(geo_df, crs=crs, geometry=geometry_infile)
    geo_df["geoid"] = geo_df.index.astype(str)

    return geo_df


def clr(x, min, max, clr):
    """
    Apply colour map onto numerical values
    :param x: pandas series
    :param min: (digit) minimum value form the dataframe column
    :param max: (digit) maxium value form the dataframe column
    :return: pandas series
    """

    cmap = cm.get_cmap(clr)
    norm = mpl.colors.Normalize(vmin=min, vmax=max)
    c = cm.ScalarMappable(norm=norm, cmap=cmap)
    colrmap =c.to_rgba(x)

    return colrmap


def add_point_markers(mapobj, gdf, type):
    """
    add point data onto folium map object
    :param mapobj: folium map object
    :param gdf: geopandas dataframe
    :param type: dataframe type (Police Stations, Clinics, Courts and Shelters)
    :return: updated folium map object
    """

    colr = {'Clinic': '#ef6548', 'Police Station': '#9ecae1', 'Sexual Offence Court': "#fed976", 'Shelter': '#addd8e'}
    pt_lyr1 = folium.FeatureGroup(name='Clinic')
    pt_lyr2 = folium.FeatureGroup(name='Police Station')
    pt_lyr3 = folium.FeatureGroup(name='Sexual Offence Court')
    pt_lyr4 = folium.FeatureGroup(name='Shelter')
    layer = {'Clinic': pt_lyr1, 'Police Station': pt_lyr2, 'Sexual Offence Court': pt_lyr3, 'Shelter': pt_lyr4}
    icon = {'Clinic': pt_lyr1, 'Police Station': pt_lyr2, 'Sexual Offence Court': pt_lyr3, 'Shelter': pt_lyr4}
    icon_types = {'Clinic': "hospital", 'Police Station': "shield-alt", 'Sexual Offence Court': "balance-scale", 'Shelter': "hands-helping"}
    # Create a Folium feature group for this layer, since we will be displaying multiple layers
    pt_lyr = layer[type]

    for i, row in gdf.iterrows():
        # Append lat and long coordinates to "coords" list
        long = row.geometry.y
        lat = row.geometry.x
        name_tag = row.Name
        if type == "Shelter":
            if "Shelter" not in name_tag:
                name_tag = name_tag + " Shelter"
            size = 8
            label = folium.Popup('{}'.format(name_tag), parse_html=True)
            alpha=0.9
        elif type == "Sexual Offence Court":
            size = 6
            court_type = row.Type
            label = folium.Popup('{} {}'.format(name_tag, court_type), parse_html=True)
            alpha = 1
        elif type == "Clinic":
            size = 6
            name_tag = name_tag.replace("Clinic Clinic", "Clinic")
            label = folium.Popup('{}'.format(name_tag), parse_html=True)
            alpha = 1
        else:
            size = 6
            label = folium.Popup('{} {}'.format(name_tag, type), parse_html=True)
            alpha = 1

        folium.CircleMarker(location=[long, lat],
                            popup=label,
                            radius=size,
                            fill=True,
                            fill_color=colr[type],
                            fill_opacity=alpha,
                            color=colr[type]).add_to(pt_lyr)

    # Add this point layer to the map object
    mapobj.add_child(pt_lyr)

    return mapobj


def convert_to_hex(rgba_color) :
    red = int(rgba_color[0]*255)
    green = int(rgba_color[1]*255)
    blue = int(rgba_color[2]*255)
    return '0x{r:02x}{g:02x}{b:02x}'.format(r=red,g=green,b=blue)


def add_choropleth(mapobj, json_data, label, colormap, data_2_dict_4_clrmap, data):
    pt_lyr = folium.FeatureGroup(name=label)

    # print(colormap.colors)
    # print(data_2_dict_4_clrmap["Western Cape"])
    # input("enter")
    folium.GeoJson(json_data,
                   name=label,
                   style_function=lambda feature: {
                       'fillColor': colormap(data_2_dict_4_clrmap[int(feature['id'])]),
                       'keyOn': "id",
                       'color': 'k',
                       'weight': 1,
                       'dashArray': '5, 5',
                       'fillOpacity': 0.9,
                       'lineOpacity': 1,
                       'line_weight': 1.0,
                       'lineColor': 'black',
                       'legendName': label,
                       'highlight': True,
                       'smoothFactor': 1.0,
                       'columns': ['geoid', label],
                   },
                   overlay=True,
                   control=True,
                   tooltip=None
                   ).add_to(pt_lyr)

    # mapobj.choropleth(geo_data=json_data, data=data, columns=['geoid', label], key_on="feature.id",
    #              fill_color='Reds', fill_opacity=0.9, line_opacity=1, line_color='k', line_weight=1.0,
    #              legend_name=label, highlight=True, smooth_factor=1.0)

    mapobj.add_child(pt_lyr)

    return mapobj


def plot_folium(province_df, geo_points_data_police_df, geo_points_data_clinics_df,
                   geo_points_data_courts_df, geo_points_data_shelters_df, outfile):
    """
    draw interactive map using geopandas dataframes
    :param province_df: dataframe containing province shapes and incidence data by province
    :param geo_points_data_police_df: dataframe containing police station coordinates
    :param geo_points_data_clinics_df: dataframe containing clinic/hospitals coordinates
    :param geo_points_data_courts_df: dataframe containing court coordinates
    :param geo_points_data_shelters_df: dataframe containing shelter coordinates
    :param outfile: an html file of an interactive map
    :return: None
    """

    labels = ['rate_sexual_crimes (%) (x1000)', 'percent_capacity_for_victim_domestic',
              'Total number of shelters', 'Total Number of beds']

    # generate geojson object of province geodataframe
    province_df_headings_to_use = ['geoid', 'rate_sexual_crimes (%) (x1000)', 'percent_capacity_for_victim_domestic',
                        'Total number of shelters', 'Total Number of beds', 'geometry']
    data = province_df[province_df_headings_to_use]
    jsontxt = data.to_json()

    # create the base map
    m = folium.Map(location=[-30.559483, 22.937506], tiles='openstreetmap',
                   zoom_start=6, control_scale=True, prefer_canvas=True)

    # add the incidence data layers to the map
    for i, item in enumerate(labels):
        data_2_dict_4_clrmap = province_df.set_index('Province')[item] #.to_dict()
        min_val = min(province_df[item])
        max_val = max(province_df[item])

        if i == 1:
            colormap = linear.Oranges_09.scale(min_val, max_val)
        elif i == 2:
            colormap = linear.Blues_09.scale(min_val, max_val)
        elif i ==3:
            colormap = linear.Greens_09.scale(min_val, max_val)
        else:
            # colormap = clr(province_df[item], min_val, max_val, "Reds")
            # colormap = [convert_to_hex(x) for x in colormap]
            colormap = linear.Reds_09.scale(min_val, max_val)

        add_choropleth(m, jsontxt, item, colormap, data_2_dict_4_clrmap, data)


    # add the point data to the map
    add_point_markers(m, geo_points_data_clinics_df, "Clinic")
    add_point_markers(m, geo_points_data_police_df, "Police Station")
    add_point_markers(m, geo_points_data_courts_df, "Sexual Offence Court")
    add_point_markers(m, geo_points_data_shelters_df, "Shelter")

    # add layer control
    folium.LayerControl().add_to(m)

    # save output
    m.save(outfile)


def main(police, clinics, courts, shelters, province, crime_data, outpath, name):
    """
    methods to plot public resources (courts, police stations, clinics, shelters...
    onto a province shape file with sexual crime incidence data
    :param police: (str) path and name for csv file with police coordinates (needs province, name, long, lat)
    :param clinics: (str) path and name for csv file with clinics coordinates (needs province, name, long, lat)
    :param courts: (str) path and name for csv file with courts coordinates (needs province, name, long, lat)
    :param shelters: (str) path and name for csv file with shelters coordinates (needs province, name, long, lat)
    :param province: (str) path and name for province shape file
    :param crime_data: (str) path and name for csv file with crime data per province
    :param outpath: (str) path to outfile location
    :param name: (str) prefix for outfile
    :return: None
    """

    # get_script_path = os.path.realpath(__file__)
    # script_folder = os.path.split(get_script_path)[0]
    # script_folder = os.path.abspath(script_folder)

    # set in and out-file paths and names
    police = os.path.abspath(police)
    clinics = os.path.abspath(clinics)
    courts = os.path.abspath(courts)
    shelters = os.path.abspath(shelters)
    province = os.path.abspath(province)
    crime_data = os.path.abspath(crime_data)

    outpath = os.path.abspath(outpath)
    name = name + "_folium_map.html"
    outfile = os.path.join(outpath, name)

    # process csv_infiles to dataframes
    geo_points_data_police_df = csv_to_geo_dataframe(police)
    geo_points_data_clinics_df = csv_to_geo_dataframe(clinics)
    geo_points_data_courts_df = csv_to_geo_dataframe(courts)
    geo_points_data_shelters_df = csv_to_geo_dataframe(shelters)

    outpath = os.path.abspath(outpath)
    name = name + "_folium_map.html"
    outfile = os.path.join(outpath, name)

    # combine crime stats and province dataframes
    crime_data = pd.read_csv(crime_data, sep=',', header=0)
    crime_data_df = pd.DataFrame(crime_data)
    crime_data_df.fillna(method='ffill', inplace=True)

    province_shape_df = gpd.read_file(province)
    province_shape_df.rename(columns={'PROVINCE': 'Province'}, inplace=True)
    province_shapes_incidence_gdf = pd.merge(province_shape_df, crime_data_df, how='inner', on="Province")
    province_shapes_incidence_gdf["geoid"] = province_shapes_incidence_gdf.index.astype(str)

    # plot the data
    plot_folium(province_shapes_incidence_gdf, geo_points_data_police_df, geo_points_data_clinics_df,
                geo_points_data_courts_df, geo_points_data_shelters_df, outfile)

    print("we are done here")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='This script will plot an interactive map of clinics, hospitals, '
                                                 'courts and places of saftey, over incidence data for different '
                                                 'provinces' ,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-p', '--police', default=argparse.SUPPRESS, type=str,
                        help='The input csv file with long and lat coordinates for police stations', required=True)
    parser.add_argument('-m', '--medical', default=False, type=str,
                        help='The input csv file with long and lat coordinates for hospitals and clinics', required=False)
    parser.add_argument('-l', '--legal', default=False, type=str,
                        help='The input csv file with long and lat coordinates for courts', required=False)
    parser.add_argument('-s', '--shelters', default=False, type=str,
                        help='The input csv file with long and lat coordinates for shelters', required=False)
    parser.add_argument('-c', '--crime_data', default=argparse.SUPPRESS, type=str,
                        help='The input csv file with crime data per province', required=True)
    parser.add_argument('-prov', '--province', default=argparse.SUPPRESS, type=str,
                        help='The shapefile for the provinces', required=True)
    parser.add_argument('-o', '--outpath', default=argparse.SUPPRESS, type=str,
                        help='The path for the output file', required=True)
    parser.add_argument('-n', '--name', default=argparse.SUPPRESS, type=str,
                        help='The name prefix for the output file', required=True)

    args = parser.parse_args()
    police = args.police
    medical = args.medical
    legal = args.legal
    shelters = args.shelters
    province = args.province
    crime_data = args.crime_data
    outpath = args.outpath
    name = args.name

    main(police, medical, legal, shelters, province, crime_data, outpath, name)

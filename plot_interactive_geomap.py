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


__author__ = 'Colin Anthony'


def clr(x):
    """
    Apply colour map onto numerical values
    :param x: pandas series
    :return: pandas series
    """
    cmap = cm.Reds
    norm = mpl.colors.Normalize(vmin=0, vmax=10)
    c = cm.ScalarMappable(norm=norm, cmap=cmap)
    ans =c.to_rgba(x)

    return ans


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
            label = folium.Popup('{}'.format(name_tag), parse_html=True)
            alpha=1
        elif type == "Sexual Offence Court":
            court_type = row.Type
            label = folium.Popup('{} {}'.format(name_tag, court_type), parse_html=True)
            alpha = 1
        elif type == "Clinic":
            name_tag = name_tag.replace("Clinic Clinic", "Clinic")
            label = folium.Popup('{}'.format(name_tag), parse_html=True)
            alpha = 1
        else:
            label = folium.Popup('{} {}'.format(name_tag, type), parse_html=True)
            alpha = 1

        folium.CircleMarker(location=[long, lat],
                            popup=label,
                            radius=6,
                            fill=True,
                            fill_color=colr[type],
                            fill_opacity=alpha,
                            color=colr[type]).add_to(pt_lyr)

    # Add this point layer to the map object
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

    province_df["colr"] = province_df["rate_sexual_crimes (%) (x1000)"].apply(lambda x: clr(x))

    m = folium.Map(location=[-30.559483, 22.937506], tiles='openstreetmap',
                   zoom_start=6, control_scale=True, prefer_canvas=True)

    data = province_df[['geoid', 'rate_sexual_crimes (%) (x1000)', 'geometry']]
    jsontxt = data.to_json()

    # pt_lyr1 = folium.FeatureGroup(name='Sexual offences')
    m.choropleth(geo_data=jsontxt, data=data, columns=['geoid', 'rate_sexual_crimes (%) (x1000)'], key_on="feature.id",
                       fill_color='Reds', fill_opacity=0.9, line_opacity=1, line_color='k', line_weight=1.0,
                       legend_name='Prevalence of Sexual Crimes (per 1000 adult women)', highlight=True, smooth_factor=1.0)

    # m.add_child(pt_lyr1)
    # pt_lyr2 = folium.FeatureGroup(name='Capacity')
    # m.choropleth(geo_data=jsontxt, data=data, columns=['geoid', ''], key_on="feature.id",
    #              fill_color='Reds', fill_opacity=0.9, line_opacity=1, line_color='k', line_weight=1.0,
    #              legend_name='Sexual crime prevalence/capacity', highlight=False, smooth_factor=1.0)

    add_point_markers(m, geo_points_data_clinics_df, "Clinic")
    add_point_markers(m, geo_points_data_police_df, "Police Station")
    add_point_markers(m, geo_points_data_courts_df, "Sexual Offence Court")
    add_point_markers(m, geo_points_data_shelters_df, "Shelter")

    # colormap = bcm.linear.Set1.scale(0, 35).to_step(10)
    folium.LayerControl().add_to(m)

    m.save(outfile)


def main(police, clinics, courts, shelters, province, crime_data, outpath, name):

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

    # read in the data points and shape file
    geo_points_data_police = pd.read_csv(police, sep=',', header=0)
    geo_points_data_clinics = pd.read_csv(clinics, sep=',', header=0)
    geo_points_data_courts = pd.read_csv(courts, sep=',', header=0)
    geo_points_data_shelters = pd.read_csv(shelters, sep=',', header=0)

    # process dataframes
    geo_points_data_police_df = pd.DataFrame(geo_points_data_police)
    geo_points_data_police_df.fillna(method='ffill', inplace=True)
    geometry_police = [Point(xy) for xy in zip(geo_points_data_police_df["longitude"], geo_points_data_police_df["latitude"])]
    geo_points_data_police_df = geo_points_data_police_df.drop(['longitude', 'latitude'], axis=1)
    crs = {'init': 'epsg:4326'}
    geo_points_data_police_df = GeoDataFrame(geo_points_data_police_df, crs=crs, geometry=geometry_police)
    geo_points_data_police_df["geoid"] = geo_points_data_police_df.index.astype(str)

    geo_points_data_clinics_df = pd.DataFrame(geo_points_data_clinics)
    geo_points_data_clinics_df.fillna(method='ffill', inplace=True)
    geometry_clinics = [Point(xy) for xy in zip(geo_points_data_clinics_df["longitude"], geo_points_data_clinics_df["latitude"])]
    geo_points_data_clinics_df = geo_points_data_clinics_df.drop(['longitude', 'latitude'], axis=1)
    crs = {'init': 'epsg:4326'}
    geo_points_data_clinics_df = GeoDataFrame(geo_points_data_clinics_df, crs=crs, geometry=geometry_clinics)
    geo_points_data_clinics_df["geoid"] = geo_points_data_clinics_df.index.astype(str)

    geo_points_data_courts_df = pd.DataFrame(geo_points_data_courts)
    geo_points_data_courts_df.fillna(method='ffill', inplace=True)
    geo_points_data_courts_df["longitude"] = geo_points_data_courts_df["longitude"].astype(float)
    geo_points_data_courts_df["latitude"] = geo_points_data_courts_df["latitude"].astype(float)
    geometry_courts = [Point(xy) for xy in zip(geo_points_data_courts_df["longitude"], geo_points_data_courts_df["latitude"])]
    # geo_points_data_clinics_df = geo_points_data_clinics_df.drop(['longitude', 'latitude'], axis=1)
    crs = {'init': 'epsg:4326'}
    geo_points_data_courts_df = GeoDataFrame(geo_points_data_courts_df, crs=crs, geometry=geometry_courts)
    geo_points_data_courts_df["geoid"] = geo_points_data_courts_df.index.astype(str)

    geo_points_data_shelters_df = pd.DataFrame(geo_points_data_shelters)
    geo_points_data_shelters_df.fillna(method='ffill', inplace=True)
    geometry_shelters = [Point(xy) for xy in zip(geo_points_data_shelters_df["longitude"], geo_points_data_shelters_df["latitude"])]
    geo_points_data_shelters_df = geo_points_data_shelters_df.drop(['longitude', 'latitude'], axis=1)
    crs = {'init': 'epsg:4326'}
    geo_points_data_shelters_df = GeoDataFrame(geo_points_data_shelters_df, crs=crs, geometry=geometry_shelters)
    geo_points_data_shelters_df["geoid"] = geo_points_data_shelters_df.index.astype(str)

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

import plot_interactive_geomap

# Data files

police = 'curated_data/points/police.csv'
medical = 'curated_data/points/clinics.csv'
legal = 'curated_data/points/courts.csv'
shelters = 'curated_data/points/shelters_low_res.csv'
crime_data = 'curated_data/incidence/1sexual_crimes_Incidence_sheltes_beds_per_province.csv'
province = 'curated_data/province_shape/Province_New_SANeighbours.shp'

# Output file

outpath = './'
name = 'index'


def main():
    plot_interactive_geomap.main(police, medical, legal, shelters, province, crime_data, outpath, name)

if __name__ == '__main__':
    main()

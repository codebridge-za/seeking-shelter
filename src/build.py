import plot_interactive_geomap
from jinja2 import Template, Environment, FileSystemLoader
import re

# Data files

police = 'curated_data/points/police.csv'
medical = 'curated_data/points/clinics.csv'
legal = 'curated_data/points/courts.csv'
shelters = 'curated_data/points/shelters_low_res.csv'
crime_data = 'curated_data/incidence/1sexual_crimes_Incidence_sheltes_beds_per_province.csv'
province = 'curated_data/province_shape/Province_New_SANeighbours.shp'

# Output files

raw_maps_path = 'src/raw_maps'

def write_map_page(name, map):
    map_id = 'map_' + map.to_dict()['id']
    html = map.get_root().render()
    body_tag_index = html.find('<body>')
    folium_head = '<!-- Folium generated requirements - not used. -->\n' + html[:body_tag_index]
    with open("src/folium_head_requirements.html", "w") as file:
        file.write(folium_head)
    map_content = html[body_tag_index:]
    map_content = re.sub(r'<body>', '', map_content)
    map_content = re.sub(r'<\/body>', '', map_content)
    env = Environment(loader=FileSystemLoader('src/templates'))
    template = env.get_template('map.html');
    template.stream(map=map_content, map_id=map_id, page=name).dump(name + '.html')
    print(name + '.html written')

def write_about_page():
    env = Environment(loader=FileSystemLoader('src/templates'))
    template = env.get_template('about.html');
    template.stream(page='about').dump('about.html')
    print('about.html written')

def main():
    basic_map = plot_interactive_geomap.main(police, medical, legal, shelters, province, crime_data, raw_maps_path, 'basic')
    write_map_page('index', basic_map)
    advanced_map = plot_interactive_geomap.main(police, medical, legal, shelters, province, crime_data, raw_maps_path, 'advanced')
    write_map_page('advanced', advanced_map)
    write_about_page()

if __name__ == '__main__':
    main()

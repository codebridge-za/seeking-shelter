import plot_interactive_geomap
from jinja2 import Template, Environment, FileSystemLoader
import re
import utilities
import markdown as md
import codecs

# Data files

police = 'curated_data/points/police.csv'
medical = 'curated_data/points/clinics.csv'
legal = 'curated_data/points/courts.csv'
shelters = 'curated_data/points/shelters.csv'
crime_data = 'curated_data/incidence/1sexual_crimes_Incidence_sheltes_beds_per_province.csv'
province = 'curated_data/province_shape/Province_New_SANeighbours.shp'

# Output files

raw_maps_path = 'src/raw_maps'

def write_map_page(name, map):
    map_id = 'map_' + map.to_dict()['id']
    html = map.get_root().render()
    body_tag_index = html.find('<body>')
    folium_head = '<!-- Folium generated requirements - not used. -->\n' + html[:body_tag_index]
    folium_head = re.sub(r'map_\w*', 'map', folium_head)
    with open("src/folium_head_requirements.html", "w") as file:
        file.write(folium_head)
    map_content = html[body_tag_index:]
    map_content = re.sub(r'<body>', '', map_content)
    map_content = re.sub(r'<\/body>', '', map_content)

    # Make legend responsive by using 'viewBox' attribute:
    # Would be much better to do this via folium, but it looks like it is hard-coded:
    # https://github.com/python-visualization/branca/blob/a2e22815eea5a96d9bf3b08fd0cfb10c6f3c3de6/branca/templates/color_scale.js
    map_content = map_content.replace('.attr("width", 450)', '.attr("viewBox", "0 0 450 40");')
    map_content = map_content.replace('.attr("height", 40);', '')

    env = Environment(loader=FileSystemLoader('src/templates'))
    template = env.get_template('map.html');
    template.stream(map=map_content, map_id=map_id, page=name).dump(name + '.html')
    print(name + '.html written')

def write_about_page():
    with codecs.open("README.md", mode="r", encoding="utf-8") as file:
        markdown = file.read()
        start_comment = '<!-- START_EXCLUDE -->'
        end_comment = '<!-- END_EXCLUDE -->'
        exclusions = markdown.count(start_comment)
        for i in range(exclusions):
            start_exclude_index = markdown.find(start_comment)
            end_exclude_index = markdown.find(end_comment)
            if end_exclude_index == -1:
                markdown = markdown[:start_exclude_index]
            else:
                markdown = markdown[:start_exclude_index] + markdown[end_exclude_index + len(end_comment):]
        html = md.markdown(markdown)
        env = Environment(loader=FileSystemLoader('src/templates'))
        template = env.get_template('about.html');
        template.stream(page='about', content=html).dump('about.html')
        print('about.html written')

def write_near_page():
    rows = []
    for data_file in [police, medical, legal, shelters]:
        rows += utilities.get_places(data_file)
    env = Environment(loader=FileSystemLoader('src/templates'))
    template = env.get_template('near.html');
    template.stream(page='near', places=rows).dump('near.html')
    print('near.html written')

def write_api_page():
    env = Environment(loader=FileSystemLoader('src/templates'))
    template = env.get_template('api.html');
    template.stream(page='api').dump('api.html')
    print('api.html written')

def main():
    basic_map = plot_interactive_geomap.main(police, medical, legal, shelters, province, crime_data, raw_maps_path, 'basic')
    write_map_page('index', basic_map)
    advanced_map = plot_interactive_geomap.main(police, medical, legal, shelters, province, crime_data, raw_maps_path, 'advanced')
    write_map_page('advanced', advanced_map)
    write_about_page()
    write_near_page()
    write_api_page()

if __name__ == '__main__':
    main()

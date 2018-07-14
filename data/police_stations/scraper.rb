require 'HTTParty'
require 'Nokogiri'

class Scraper
  def get_links(uri)
    root = 'https://www.saps.gov.za/contacts'
    doc = HTTParty.get("#{root}/#{uri}")
    parse_page = Nokogiri::HTML(doc)
    parse_page.css('body > div:nth-child(5) > div > div > div > div.panel-body > table:nth-child(3) li a:nth-child(1)')
  end

  def get_data(uri)
    root = 'https://www.saps.gov.za/contacts'
    doc = HTTParty.get("#{root}/#{uri}")
    parse_page = Nokogiri::HTML(doc)
    parse_page.css('body > div:nth-child(5) > div > div > div > div.panel-body > table:nth-child(2)').text
  end
end

scraper = Scraper.new
provinces = [
  {name: 'Gauteng', uri: 'provdetails.php?pid=1', links: []},
  {name: 'Limpopo', uri: 'provdetails.php?pid=2', links: []},
  {name: 'Kwazulu-Natal', uri: 'provdetails.php?pid=3', links: []},
  {name: 'Free State', uri: 'provdetails.php?pid=4', links: []},
  {name: 'Eastern Cape', uri: 'provdetails.php?pid=5', links: []},
  {name: 'Mpumalanga', uri: 'provdetails.php?pid=6', links: []},
  {name: 'Northern Cape', uri: 'provdetails.php?pid=7', links: []},
  {name: 'North West', uri: 'provdetails.php?pid=8', links: []},
  {name: 'Western Cape', uri: 'provdetails.php?pid=9', links: []},
]

provinces.each do |province|
  province.tap do |prov|
    prov[:links] = scraper.get_links(prov[:uri]).map(&:values).flatten
  end
end

# Export Provinces to CSC
# CSV.open('provinces.csv', 'wb') do |csv|
#   provinces.each do |province|
#     csv << [province]
#   end
# end

CSV.open('stations.csv', 'wb') do |csv|
  provinces.each do |province|
    puts province[:name]
    province[:links].flatten.each do |link|
      csv << ["Province:#{province[:name]} #{scraper.get_data(link)}"]
    end
  end
end

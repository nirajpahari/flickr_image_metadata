from bs4 import BeautifulSoup
from urllib.request import urlopen
import csv

# coordinates for Pokhara lat = 28.2380, lon = 83.9956
url = "https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=<secret_key>&per_page=250&has_geo=1&lat=28.2380&lon=83.9956&extras=geo,tags,description"
soup = BeautifulSoup(urlopen(url), "lxml")

# photo_url_template = https://farm{farm-id}.staticflickr.com/{server-id}/{id}_{secret}.jpg
photo_url_template = "https://farm{0}.staticflickr.com/{1}/{2}_{3}.jpg"
final = []


with open('tourism_pkr.csv', mode='w') as csv_file:
    fieldnames = ['id', 'photo', 'latitude', 'longitude', 'description', 'tags', 'userID']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for data in soup.find_all('photo'): #iterate through the XML Document

        user_id = data.get("owner")
        description = data.find('description').text
        latitude = data.get("latitude")
        longitude = data.get("longitude")
        tags = data.get("tag")

        farm_id = data.get("farm")
        server_id = data.get("server")
        image_id = data.get("id")
        secret = data.get("secret")
        photo_url = photo_url_template.format(farm_id, server_id, image_id, secret)
        writer.writerow({'id': image_id, 'photo': photo_url, 'latitude': latitude, 'longitude': longitude, 'description': description, 'tags': tags, 'userID': user_id})

print ("Process Finished")


# References
# https://stackoverflow.com/questions/24845410/how-to-extract-image-geodata-out-of-flickr-xml-image-data-with-python
# https://www.flickr.com/services/api/flickr.photos.search.html
# https://www.flickr.com/services/api/misc.urls.html
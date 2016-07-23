import json
import urllib
import random

def get(starting_lat, starting_lon, ending_lat, ending_lon):
    fh = urllib.urlopen("https://maps.googleapis.com/maps/api/distancematrix/json?origins=%s,%s&destinations=%s,%s&units=imperial&key=AIzaSyD9Cyy79DLP-pvlVVYB1rBCkZwNfojOhG0"
         % (starting_lat, starting_lon, ending_lat, ending_lon))
    read = fh.read()
    load = json.loads(read)
    return load["rows"][0]["elements"][0]["duration"]["text"]

def name_to_coord(name):
    name.replace(" ", "")
    fh = urllib.urlopen("http://maps.googleapis.com/maps/api/geocode/json?components=country:US&address=%s" % name)
    read = fh.read()
    load = json.loads(read)
    if (load["results"] == []):
        return ""
    return load["results"][0]["geometry"]["location"]["lat"], load["results"][0]["geometry"]["location"]["lng"]

def coord_to_name(lat, lon):
    fh = urllib.urlopen("https://maps.googleapis.com/maps/api/geocode/json?latlng=%s,%s&key=AIzaSyD9Cyy79DLP-pvlVVYB1rBCkZwNfojOhG0"
                        %(lat, lon))
    read = fh.read()
    load = json.loads(read)
    name = load["results"][0]["formatted_address"]
    return name
 #format_name(name)
 
def generate_code(numbers):
    total = int(random.uniform(1, 10))
    for h in range(1, numbers):
        num = int(random.random() * 10)
        total *= 10
        total += num
    return total
    
def format_name(name):
    index = name.find(",")
    part_1 = name[:index+1]
    part_2 = name[index+1:]
    second = part_2.find(",")
    return part_1 + part_2[:second]
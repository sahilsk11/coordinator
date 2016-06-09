import json
import urllib
import shelve

def get(starting_lat, starting_lon, ending_lat, ending_lon):
    fh = urllib.urlopen("https://maps.googleapis.com/maps/api/distancematrix/json?origins=%s,%s&destinations=%s,%s&units=imperial&key=AIzaSyD9Cyy79DLP-pvlVVYB1rBCkZwNfojOhG0"
         % (starting_lat, starting_lon, ending_lat, ending_lon))
    read = fh.read()
    load = json.loads(read)
    return load["rows"][0]["elements"][0]["duration"]["text"]

def name_to_coord(name):
    name.replace(" ", "")
    fh = urllib.urlopen("http://maps.googleapis.com/maps/api/geocode/json?address=%s" % name)
    read = fh.read()
    load = json.loads(read)
    return load["results"][0]["geometry"]["location"]["lat"], load["results"][0]["geometry"]["location"]["lng"]

def coord_to_name(lat, lon):
    fh = urllib.urlopen("https://maps.googleapis.com/maps/api/geocode/json?latlng=%s,%s&key=AIzaSyD9Cyy79DLP-pvlVVYB1rBCkZwNfojOhG0"
                        %(lat, lon))
    read = fh.read()
    load = json.loads(read)
    name = load["results"][0]["formatted_address"]
    return format_name(name)
    
def format_name(name):
    index = name.find(",")
    short_name = name[index+1:]
    second = short_name.find(",") + len(short_name)-2
    return name[:second]
print name_to_coord("Mountain View Ave, Los Altos")
#y= name_to_coord("500 Saratoga Ave, San Jose")
#print get(x[0], x[1], y[0], y[1])
#print coord_to_name(37.293414, -121.775932)
#37.293414, -121.775932, 37.3179792, -121.9715838
#print get(37.293414, -121.775932, 37.3179792, -121.9715838)
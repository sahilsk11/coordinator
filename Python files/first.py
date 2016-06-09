import json
import urllib
import datetime
from time import sleep



def get():
    fh = urllib.urlopen("https://maps.googleapis.com/maps/api/directions/json?origin=2222BentleyRidgeDr&destination=500SaratogaAve&traffic_model=pessimistic&departure_time=now")
    read = fh.read()
    load = json.loads(read)
    return load["routes"][0]["legs"][0]["duration"]["text"], load["routes"][0]["legs"][0]["duration"]["value"]

#returns the time if one leaves now
def time():
    date = datetime.datetime.today()
    t = date + datetime.timedelta(seconds=get())
    print t
    
    
def departureHour():
    arrival = datetime.datetime(2016, 3, 10, 7, 50)
    departureTime =  arrival - datetime.timedelta(seconds=get()[1]) - datetime.timedelta(seconds=300)
    return departureTime

#return true if one should leave now
def onTime(): 
    now = datetime.datetime.today()
    shouldGo = (now >= departureHour())
    return shouldGo
    
def check():
    now = datetime.datetime.today()
    first = datetime.datetime(2016, 3, 10, 6, 00)
    if (now + datetime.timedelta(seconds=300) < first):
        time = first - now
        sleep(time)
    if (onTime()):
        return True
    else:
        time = departureHour()
        now = datetime.datetime.today()
        find = time - now
        sleep(find)
        
    return True
print get()[0]


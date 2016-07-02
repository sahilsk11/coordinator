#!/usr/bin/python

print "Content-type: application/json\n\n"

import operations
import cgi
import json

#cgitb.enable(display=0, logdir="/tmp/logfile")
operations.init("information.shelve")

form = cgi.FieldStorage()
command = form.getfirst("command", "")
new_user = form.getfirst("new_user", "")
old_user = form.getfirst("old_user", "")
user = form.getfirst("user", "")
lat = (form.getfirst("lat", ""))
lon = (form.getfirst("lon", ""))
destination = form.getfirst("destination", "")

if (lat != ""):
    lat = float(lat)
 
if (lon != ""):
    lon = float(lon)
    

if (command == 'change_user'):
    if (new_user == old_user):
        d = {"complete":"True"}
    else:
        cmplt = operations.change_user(old_user, new_user)
        if (cmplt == 2):
            d = {"complete":"True"}
        elif (cmplt == 0):
            d = {"complete":"Notfound"}
        else:
            d = {"complete":"Used"}
    j = json.dumps(d)
    print j
    
if (command == "update_user"):
    if (operations.update_user(user, lat, lon) == 0):
        d = {"complete":"Incomplete"}
    if (operations.update_user(user, lat, lon) == 1):
        d = {"complete":"Destination"}
    else:
        d = {"complete":"True"}
    j = json.dumps(d)
    print j

if (command == "add_user"):
    d = {}
    cmplt = operations.add_user(user, lat, lon)
    if (cmplt == 0):
        d = {"complete":"Used"}
    elif (cmplt == 1):
        d = {"complete":"Incomplete"}
    else:
        d = {"complete":"True"}
    j = json.dumps(d)
    print j

if (command == "change_destination"):
    valid = operations.change_destination(destination)
    d = {}
    if (valid != ""):
        d = {"complete":"True", "name":valid}
    else:
        d = {"complete":"Invalid"}
    j = json.dumps(d)
    print j

if (command == "show"):
    print operations.convert_json()

if (command == "update"):
    cmplt = operations.update_user(user, lat, lon)
    d = {}
    if (cmplt == 1):
        d = {"complete":"Location"}
    elif (cmplt == 0):
        d = {"complete":"Incomplete"}
    else:
        d = {"complete":"True"}
    j = json.dumps(d)
    print j
        

if (command == "delete"):
    operations.delete_shelve()
    
operations.close()

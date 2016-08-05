#!/usr/bin/python

print "Content-type: application/json\n\n"

import operations
import cgi
import json
import datetime

#cgitb.enable(display=0, logdir="/tmp/logfile")

operations =  operations.operations()
operations.init("information.shelve")
form = cgi.FieldStorage()
command = form.getfirst("command", "")
new_user = form.getfirst("new_user", "")
old_user = form.getfirst("old_user", "")
user = form.getfirst("user", "")
lat = (form.getfirst("lat", ""))
lon = (form.getfirst("lon", ""))
destination = form.getfirst("destination", "")
code = form.getfirst("code", "")
lat = form.getfirst("lat", "")
lon = form.getfirst("lon", "")
uid = form.getfirst("uid", "")
elat = form.getfirst("elat", "")
elon = form.getfirst("elon", "")


if (lat != ""):
    lat = float(lat)
 
if (lon != ""):
    lon = float(lon)

if (code != ""):
    code = int(code)
    
if (elat != ""):
    elat = float(elat)
    
if (elon != ""):
    elon = float(elon)
    
if (command == 'change_user'):
    if (new_user == old_user):
        d = {"valid":"True"}
    else:
        cmplt = operations.change_user(old_user, new_user, code)
        if (cmplt == 2):
            d = {"valid":"True"}
        elif (cmplt == 0):
            d = {"valid":"Notfound"}
        else:
            d = {"valid":"UserTaken"}
    j = json.dumps(d)
    print j
    
if (command == "update_user"):
    cmplt = operations.update_user(user, lat, lon, code)
    if (cmplt == 0):
        d = {"complete":"Incomplete"}
    elif (cmplt == 1):
        d = {"complete":"Destination"}
    else:
        d = {"complete":"True"}
    j = json.dumps(d)
    print j

if (command == "add_user"):
    d = {}
    cmplt = operations.add_user(user, lat, lon, code, uid)
    if (cmplt == 0):
        d = {"valid":"UserTaken"}
    elif (cmplt == 2):
        d = {"valid":"True"}
    else:
        d = {"valid":"CodeWrong"}
    j = json.dumps(d)
    print j

if (command == "change_destination"):
    valid = operations.change_destination(destination, lat, lon, code)
    d = {}
    if (valid != ""):
        d = {"valid":"True"}
    else:
        d = {"valid":"False"}
    j = json.dumps(d)
    print j

if (command == "show"):
    cmplt = operations.convert_json(code)
    if (cmplt == ""):
        d = {"valid":"False"}
        j = json.dumps(d)
        print j
    else:
        print cmplt

if (command == "check_event"):
    d = {}
    cmplt = operations.check_destination(destination)
    if (cmplt == ""):
        d = {"complete":"Invalid"}
    else:
        d = {"complete":"True", "name":cmplt}
    j = json.dumps(d)
    print j
    
if (command == "new_event"):
    valid = operations.new_event(destination, elat, elon)
    code = valid[1]
    cmplt = operations.add_user(user, lat, lon, code, uid)
    d = {}
    if (valid[0] != ""):
        d = {"complete":"True", "name":valid[0], "code":code}
    else:
        d = {"complete":"Invalid"}
    j = json.dumps(d)
    print j
    
if (command == "check_event_code"):
    if (operations.check_user_code(code)):
        d = {"valid":"true"}
    else:
        d = {"valid":"false"}
    j = json.dumps(d)
    print j
        
if (command == "delete"):
    operations.delete_shelve()
    
operations.close()

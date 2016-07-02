import coordinator
import shelve
import json
 
#file = information.py
def init(name):
    global sh
    sh = shelve.open(name, writeback= True)
    if (not sh.has_key("people")):
        sh["people"] = []
    if (not sh.has_key("destination")):
        sh["destination"] = {}
        sh["destination"]["set"] = "no"
    if (not sh.has_key("users")):
        sh["users"] = 0
    if (not sh.has_key("takenusers")):
        sh["takenusers"] = {}
    
#0 - destination set, 1 - destination not found 2 -success
def update_user(user, new_lat, new_lon):
    if (not sh["destination"].has_key("name")):
        return 0
    number = sh["takenusers"][user]
    sh["people"][number]["lat"] = new_lat
    sh["people"][number]["lon"] = new_lon
    success = coordinator.get(new_lat, new_lon, sh["destination"]["lat"], sh["destination"]["lon"])
    if (success == ""):
        return 1;
    else:
        sh["people"][number]["time"] = success
        return 2;

#0 - old user not found, 1 - user taken, 2 - success
def change_user(olduser, newuser):
    if (not sh["takenusers"].has_key(olduser)):
        return 0
    if (sh["takenusers"].has_key(newuser)):
        return 1
    number = sh["takenusers"][olduser]
    del sh["takenusers"][olduser]
    sh["takenusers"][newuser] = number
    sh["people"][number]["name"] = newuser
    return 2

#0 - used 1 - destination 2 - works
def add_user(user, lat, lon):
    if (sh["takenusers"].has_key(user)):
        return 0;
    if (not sh["destination"].has_key("name")):
        return 1;
    sh["people"].append({})
    sh["people"][sh["users"]]["name"] = user
    sh["people"][sh["users"]]["lat"] = lat
    sh["people"][sh["users"]]["lon"] = lon
    sh["people"][sh["users"]]["time"] = coordinator.get(lat, lon, sh["destination"]["lat"], sh["destination"]["lon"])
    sh["takenusers"][user] = sh["users"]
    sh["users"] += 1
    return 2;

def change_destination(destination):
    coordinates = coordinator.name_to_coord(destination)
    if (coordinates == ""):
        return "";
    if (not sh.has_key("destination")):
        sh["destination"] = {}
    sh["destination"]["lat"] = coordinates[0]
    sh["destination"]["lon"] = coordinates[1]
    sh["destination"]["user_input"] = destination
    name = coordinator.coord_to_name(coordinates[0], coordinates[1])
    sh["destination"]["name"] = name
    sh["destination"]["set"] = "yes";
    return name;

def convert_json():
    d = dict(sh)
    data = json.dumps(d)
    return data
    
def delete_shelve():
    sh.clear()
    init("information.shelve")
    
def close():
    sh.close()

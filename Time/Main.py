import coordinator
import shelve

sh = shelve.open("information.py", writeback= True)

if (not sh.has_key("people")):
    sh["people"] = {}

def update_destination(new_lat, new_lon, name=""):
    if (not sh.has_key("destination")):
        sh["destination"] = {}
    sh["destination"]["lat"] = new_lat
    sh["destination"]["lon"] = new_lon
    sh["destination"]["name"] = coordinator.coord_to_name(new_lat, new_lon)
    
def update_user(user, new_lat, new_lon):
    if (not sh.has_key(user)):
        sh["people"][user] = {}
    sh["people"][user]["lat"] = new_lat
    sh["people"][user]["lon"] = new_lon
    sh["people"][user]["time"] = coordinator.get(new_lat, new_lon, sh["destination"]["lat"], sh["destination"]["lon"])

    
def delete_shelve():
    sh.clear()

user = "sahil"
update_destination(37.293414, -121.775932) #house
update_user(user, 37.3179792, -121.9715838) #school
print sh["people"][user]["time"]
print sh["destination"]["name"]

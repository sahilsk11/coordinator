import coordinator
import shelve
import json
 
 
 
#file = information.py

class operations():
    
    def init(self, name):
        self.file = shelve.open(name, writeback= True)
        if (not self.file.has_key("events")):
            self.file["events"] = {}

    def new_code(self, length):
        code = coordinator.generate_code(length)
        if (self.file["events"].has_key(code)):
            self.new_code(length)
        else:
            return code
        
    def new_event(self, destination, lat, lon):
        code = self.new_code(5)
        self.file["events"][code] = {}
        self.file["events"][code]["people"] = []
        self.file["events"][code]["takenusers"] = {}
        self.file["events"][code]["destination"] = {}
        self.file["events"][code]["destination"]["set"] = "no"
        self.file["events"][code]["uids"] = {}
        return self.change_destination(destination, lat, lon, code), code

        
    #0 - destination set, 1 - destination not found 2 -success 3 - user not found
    def update_user(self, user, new_lat, new_lon, code):
        if (not self.file["events"][code]["destination"].has_key("name")):
            return 0
        if (self.file["events"][code]["takenusers"].has_key(user)):
            number = self.file["events"][code]["takenusers"][user]
            self.file["events"][code]["people"][number]["lat"] = new_lat
            self.file["events"][code]["people"][number]["lon"] = new_lon
            success = coordinator.get(new_lat, new_lon, self.file["events"][code]["destination"]["lat"], self.file["events"][code]["destination"]["lon"])
            if (success == ""):
                return 1;
            else:
                self.file["events"][code]["people"][number]["time"] = success
                return 2;
        else:
            return 3
    
    #0 - old user not found, 1 - user taken, 2 - success
    def change_user(self, olduser, newuser, code):
        if (not self.file["events"][code]["takenusers"].has_key(olduser)):
            return 0
        if (olduser == newuser):
            return 2
        for name in self.file["events"][code]["takenusers"].keys():
            if (name.lower() == newuser.lower()):
                return 1
        number = self.file["events"][code]["takenusers"][olduser]
        del self.file["events"][code]["takenusers"][olduser]
        self.file["events"][code]["takenusers"][newuser] = number
        uid = self.file["events"][code]["people"][number]["UID"]
        self.file["events"][code]["uids"][uid] = newuser
        self.file["events"][code]["people"][number]["name"] = newuser
        return 2
    
    #0 - User taken
    #1 - Code not found
    #2 - Success
    def add_user(self, user, lat, lon, code, uid):
        if (not self.file["events"].has_key(code)):
            return 1
        for name in self.file["events"][code]["takenusers"].keys():
            if (name.lower() == user.lower()):
                return 0
        number = len(self.file["events"][code]["people"])
        self.file["events"][code]["people"].append({})
        self.file["events"][code]["uids"][uid] = user
        self.file["events"][code]["people"][number]["UID"] = uid
        self.file["events"][code]["people"][number]["name"] = user
        self.file["events"][code]["people"][number]["lat"] = lat
        self.file["events"][code]["people"][number]["lon"] = lon
        self.file["events"][code]["people"][number]["time"] = coordinator.get(lat, lon, self.file["events"][code]["destination"]["lat"], self.file["events"][code]["destination"]["lon"])
        self.file["events"][code]["takenusers"][user] = number
        return 2;
    
    def change_destination(self, destination, lat, lon, code):
        coordinates = (lat, lon)
        if (coordinates == ""):
            return "";
        if (not self.file["events"][code].has_key("destination")):
            self.file["events"][code]["destination"] = {}
        self.file["events"][code]["destination"]["lat"] = coordinates[0]
        self.file["events"][code]["destination"]["lon"] = coordinates[1]
        self.file["events"][code]["destination"]["name"] = destination
        self.file["events"][code]["destination"]["set"] = "yes";
        return destination;
    
    def check_destination(self, name):
        coordinates = coordinator.name_to_coord(name)
        if (coordinates == ""):
            return ""
        else:
            return coordinator.coord_to_name(coordinates[0], coordinates[1])
        
    def check_user_code(self, code):
        if (self.file["events"].has_key(code)):
            return True
        else:
            return False
    
    def convert_json(self, code):
        if (code == ""):
            d = dict(self.file)
            data = json.dumps(d)
            return data
        if (not self.file["events"].has_key(code)):
            return ""
        d = dict(self.file["events"][code])
        data = json.dumps(d)
        return data
        
    def clear_event(self, code):
        self.file["events"][code].clear()
        self.init("information.shelve")
        
    def delete_shelve(self):
        self.file.clear()
        
    def close(self):
        self.file.close()
      
 
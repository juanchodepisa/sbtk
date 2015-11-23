from src.interfacing.ogs.connect import Authentication
import codecs
import sys
import os
from time import sleep

def loadList(pNameFile):   
    iList = []
    with codecs.open(pNameFile, "r", "utf-8") as f:
        for line in f:
            iList.append(line)
    return iList
    
if __name__ == "__main__":
    a = Authentication("Kuksu League", "", testing=False);
    
    iGroupNames = loadList("E:/Project/OGS/OGS-League/group_names.txt");
    fGroupIDs = codecs.open("E:/Project/OGS/OGS-League/group_ids.txt", "w", "utf-8");
    
    nGroups = len(iGroupNames);
    
    for i in range(nGroups):
        iGroupNames[i] = iGroupNames[i].replace("\r\n", "")
        iGroupNames[i] = iGroupNames[i].replace("\n", "")
        iTournament = a.post(['tournaments'],{
            "name":"Kuksu Main Title Tournament 9th Cycle - Group %s" % iGroupNames[i],
            "group":515,
            "tournament_type":"roundrobin",
            "description":"Kuksu Main Title Tournament 9th Cycle - Group %s" % iGroupNames[i],
            "board_size":19,
            "handicap":0, #default -1 for auto
            "time_start": "2015-12-01T00:00:00Z",
            "time_control_parameters":{
            "time_control":"fischer",
            "initial_time":604800,
            "max_time":604800,
            "time_increment":86400
            },
            "rules": "korean",
            "exclusivity": "invite", # open, group.  default
            "exclude_provisional": False,  # default
            "auto_start_on_max": True,   # default
            "analysis_enabled": True, #default
            "settings":{
            "maximum_players":10,
            },
            "players_start": 10, #default
            "first_pairing_method": "slide",  #slaughter, random, slide, strength . default
            "subsequent_pairing_method": "slide",  # default
            "min_ranking":0,
            "max_ranking":36
        });
        
        print("Tournament %s with id %d created.\n" % (iGroupNames[i], iTournament["id"]));
        fGroupIDs.writelines("%d\n" % iTournament["id"]);
        sleep(2);
       
    fGroupIDs.close();
    
#a.put(['tournaments', 12650], {"description":"Test Test"});

# tourney id 7370
"""
iTournament = a.post(['tournaments'],{
  "id":12650,
  "name":"Test Tournament 2",
  "group":515,
  "tournament_type":"roundrobin",
  "description":"<b>Test 3</b>",
  "board_size":19,
  "handicap":0, #default -1 for auto
  "time_start": "2015-12-01T00:00:00Z",
  "time_control_parameters":{
    "time_control":"fischer",
    "initial_time":604800,
    "max_time":604800,
    "time_increment":86400
  },
  "rules": "korean",
  "exclusivity": "invite", # open, group.  default
  "exclude_provisional": False,  # default
  "auto_start_on_max": True,   # default
  "analysis_enabled": True, #default
  "settings":{
    "maximum_players":10,
  },
  "players_start": 6, #default
  "first_pairing_method": "slide",  #slaughter, random, slide, strength . default
  "subsequent_pairing_method": "slide",  # default
  "min_ranking":0,
  "max_ranking":36
});

#print("Hello");
print(iTournament["id"]);
"""
#print "Tournament %s is created." % iTournament["id"];

# r= a.post (['tournaments', 12642, 'players'], app_param= {"player_id":40318} )
# print (r)

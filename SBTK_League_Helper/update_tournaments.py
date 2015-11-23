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
    iGroupIDs = loadList("E:/Project/OGS/OGS-League/group_ids.txt");
    
    nGroups = len(iGroupNames);
    
    for i in range(nGroups):
        iGroupNames[i] = iGroupNames[i].replace("\r\n", "");
        iGroupNames[i] = iGroupNames[i].replace("\n", "");
        iGroupIDs[i] = iGroupIDs[i].replace("\r\n", "");
        iGroupIDs[i] = iGroupIDs[i].replace("\n", "");
        iGroupIDs[i] = int(iGroupIDs[i]);
        
        iDescription = """
Kuksu Main Title Tournament 9th Cycle Group %s

Title Holder: <a href='https://online-go.com/user/view/35184/vitality'>vitality (5d)</a>

Previous cycles:
<table style="text-align:center;" border='2'>
<tr><th rowspan=2>Cycle</th><td colspan=3><b>Title Match</b></td><td colspan=3><b>Title Tournament</b></td></tr>
<tr>
    <th>Winner</th><th>Score</th><th>Runner-up</th>
    <th>Winner<img src='https://a00ce0086bda2213e89f-570db0116da8eb5fdc3ce95006e46d28.ssl.cf1.rackcdn.com/4.2/img/trophies/gold_title_19.png' alt='Gold'></img></th>
    <th>Runner-up<img src='https://a00ce0086bda2213e89f-570db0116da8eb5fdc3ce95006e46d28.ssl.cf1.rackcdn.com/4.2/img/trophies/silver_title_19.png' alt='Silver'></img></th>
    <th>3rd Place<img src='https://a00ce0086bda2213e89f-570db0116da8eb5fdc3ce95006e46d28.ssl.cf1.rackcdn.com/4.2/img/trophies/bronze_title_19.png' alt='Bronze'></img></th>
</tr>
<tr>
    <td><a href='https://online-go.com/tournament/2375'>1</a></td>
    <td><b>luke</b></td><td></td><td></td>
    <td><b>luke (2d)</b></td><td>davos</td><td>gomad361</td>
</tr>
<tr>
    <td><a href='https://online-go.com/tournament/2384'>2</a></td>
    <td><b>gomad361</b></td><td>3-2</td><td>luke</td>
    <td><b>luke (2d)</b></td><td>gomad361</td><td>hotspur</td>
</tr>
<tr>
    <td><a href='https://online-go.com/tournament/2391'>3</a></td>
    <td><b>Uberdude</b></td><td>&lowast;</td><td>gomad361</td>
    <td><b>Uberdude (6d)</b></td><td>KyuT</td><td>marigo</td>
</tr>
<tr>
    <td><a href='https://online-go.com/tournament/2406'>4</a></td>
    <td><b>Uberdude</b></td><td>5-0</td><td>KyuT</td>
    <td><b>KyuT (4d)</b></td><td>quiller</td><td>morituri</td>
</tr>
<tr>
    <td><a href='https://online-go.com/tournament/2424'>5</a></td>
    <td><b>Uberdude</b></td><td>5-0</td><td>gomad361</td>
    <td><b>gomad361 (2d)</b></td><td>morituri</td><td>betterlife</td>
</tr>
<tr>
    <td><a href='https://online-go.com/tournament/2439'>6</a></td>
    <td><b>Uberdude</b></td><td>5-0</td><td>Elin</td>
    <td><b>Elin (3d)</b></td><td>gomad361</td><td>morituri</td>
</tr>
<tr>
    <td><a href='https://online-go.com/tournament/2460'>7</a></td>
    <td><b>Uberdude</b></td><td>3-2</td><td>vitality</td>
    <td><b>vitality (5d)</b></td><td>Elin</td><td>gomad361</td>
</tr>
<tr>
    <td><a href='https://online-go.com/tournament/2475'>8</a></td>
    <td><b>vitality</b></td><td>&lowast;</td><td>Uberdude</td>
    <td><b>vitality (5d)</b></td><td>nrx</td><td>gojohn</td>
</tr>    
<tr>
    <td rowspan=5><a href='#'>9</a></td>
    <td rowspan=5 colspan=3></td>
    <td colspan=3>
        <a href='https://online-go.com/tournament/12653'>[A]</a>
    </td>
</tr>
<tr>
    <td colspan=3>
        <a href='https://online-go.com/tournament/12654'>[B1]</a>
        <a href='https://online-go.com/tournament/12655'>[B2]</a>
    </td>
</tr>
<tr>
    <td colspan=3>
        <a href='https://online-go.com/tournament/12656'>[C1]</a>
        <a href='https://online-go.com/tournament/12657'>[C2]</a>
        <a href='https://online-go.com/tournament/12658'>[C3]</a>
        <a href='https://online-go.com/tournament/12659'>[C4]</a>
    </td>
</tr>
<tr>
    <td colspan=3>
        <a href='https://online-go.com/tournament/12660'>[D1]</a>
        <a href='https://online-go.com/tournament/12661'>[D2]</a>
        <a href='https://online-go.com/tournament/12662'>[D3]</a>
        <a href='https://online-go.com/tournament/12663'>[D4]</a>
        <a href='https://online-go.com/tournament/12664'>[D5]</a>
        <a href='https://online-go.com/tournament/12665'>[D6]</a>
        <a href='https://online-go.com/tournament/12666'>[D7]</a>
        <a href='https://online-go.com/tournament/12667'>[D8]</a>
    </td>
</tr>
<tr>
    <td colspan=3>
        <a href='https://online-go.com/tournament/12668'>[E1]</a>
        <a href='https://online-go.com/tournament/12669'>[E2]</a>
        <a href='https://online-go.com/tournament/12670'>[E3]</a>
        <a href='https://online-go.com/tournament/12671'>[E4]</a>
        <a href='https://online-go.com/tournament/12672'>[E5]</a>
        <a href='https://online-go.com/tournament/12673'>[E6]</a>
    </td>
</tr>
</table>

&lowast; means the games were finished by timeout or retiring.

Rules could be found <a href='https://forums.online-go.com/t/league-format-kuksu-title-tournament-rules-and-discussion/5191'>here</a>.

""" % iGroupNames[i];
        
        a.put(['tournaments', iGroupIDs[i]], {"description": iDescription
        });
        
        print("Tournament %s with id %d updated.\n" % (iGroupNames[i], iGroupIDs[i]));
        sleep(2);
       
    


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

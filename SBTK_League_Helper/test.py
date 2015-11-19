from src.interfacing.ogs.connect import Authentication

puppets = [1121, 1122, 1124, 1125]

a = Authentication("Leira", "Leira1234567890", testing=True)

# tourney id 7370

# a.post(['tournaments'],{
  # "name":"Test Tournament 3",
  # "group":9,
  # "tournament_type":"roundrobin",
  # "description":"A big grand tournament",
  # "board_size":5,
  # "handicap":0, #default -1 for auto
  # "time_start": "2015-10-24T18:40:00Z",
  # "time_control_parameters":{
    # "time_control":"fischer",
    # "initial_time":259200,
    # "max_time":604800,
    # "time_increment":86400
  # },
  # "exclusivity": "invite", # open, group.  default
  # "exclude_provisional": False,  # default
  # "auto_start_on_max": True,   # default
  # "analysis_enabled": False, #default
  # "settings":{
    # "maximum_players":10,
  # },
  # "players_start": 6, #default
  # "first_pairing_method": "slaughter",  #random, slide, strength . default
  # "subsequent_pairing_method": "random",  # default
  # "min_ranking":0,
  # "max_ranking":36
# })

# r= a.post (['tournaments', 7379, 'players'], app_param= {"player_id":1122} )
# print (r)

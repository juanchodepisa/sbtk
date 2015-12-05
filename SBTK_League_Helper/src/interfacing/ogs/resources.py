from src.tools.dictionaries import MarkedDict
from src.tools.markers import AdHocMarker
from src import class_initializer, log_entry

from .. import SUPPORTED_SERVERS


main_server_strings = dict (
    host_website            = "https://online-go.com",
    api_server              = "https://online-go.com",
    api_live_server         = "https://ggs.online-go.com",
    api_version             = "api/v1",
    authentication_standard = "OAuth 2.0",
    context                 = "Online Go Server (OGS)",
    context_short           = "OGS",       #must be url-safe, and filename-safe
    )
    
beta_server_strings = dict (main_server_strings,
    api_server              = "https://beta.online-go.com",
    api_live_server         = "https://ggsbeta.online-go.com",
    context                 = "Online Go (Beta) Server (OGS Beta)",
    context_short           = "OGS_Beta",       #must be url-safe, and filename-safe
    )

server_context_strings = {'main': main_server_strings, 'test': beta_server_strings}

GET, PUT, POST, PATCH, DELETE = 'GET', 'PUT', 'POST', 'PATCH', 'DELETE'


    
def get_context_str(s, mode = "main"):
    return server_context_strings[mode][s]

    

main_server = SUPPORTED_SERVERS[get_context_str('context_short')]
beta_server = SUPPORTED_SERVERS[get_context_str('context_short', 'test')]
    
    
    


__ref1 = log_entry ("Setting up %s resource tree...." % get_context_str("host_website"))


# Initializing custom tool:
__ref2 = log_entry ("Initializing custom dictionary tool....")

class ResourceDict(MarkedDict):
    """
    ''HACK'' FOR RETURNING A PRIORI UNRECOGNIZED ENTRIES LITERALLY:
    """
    #There is a __hack_title, field, not initialized on purpose
    
    def setup_hack(self, id_counter=0):
        if self.is_hack(): # initializes the __hack_title field, if it does not exist.
            pass # End of recursion!! (explicit for readability)
        else:
            # First check there's no ID marker in place
            id = self.ref_marker("id")
            sh = self.ref_marker("shortcut")
            if not (id in self) and not ((sh in self) and (id in self[sh])):
                new_format_string = '{{{}}}'.format(id_counter)
                self.add([ID],
                    default = self(unformatted =True)[0]+new_format_string,
                    title = self.__hack_title,
                    description = "What is not in the dictionary is parsed as is.",
                    dev_info= "#HACK# with a shortcut to self, and string appending as parsing function, it can be generalized for any iterable.\n"+
                            "Sending '/{}/somedirectory' should work, replacing {} with api version.")
                self.add_shortcut([ID, ID], [ID], parsing_function = lambda *args: list(args[:-2])+[str(args[-2])+str(args[-1])])
            
            # Whatever. What it really does is catching ID for every node, and then passing an ID shortcut back to itself
            # with a formatting trick, and the shorcut parsing already in place from parent Class, it can be forced to return
            # whatever is passed literally after it stops recognizing legitimate paths
            
            gen =(x for x in self if not self.is_any_marker(x, id = False))
            for key in gen:
                if key is id:
                    self[key].setup_hack(id_counter+1)
                else:
                    self[key].setup_hack()
    
    def is_hack(self): # All legitimate nodes must have a "methods" entry.
        try:
            return self([], "title", formatting_function = lambda x: x) is self.__hack_title
        except KeyError:
            return False
        except AttributeError: # This is first access
            type(self).__hack_title = AdHocMarker("Hack Node", type(self))
            return False
    
    def display_condition (self, key):
        return not self[key].is_hack()
    """
    END OF HACK.
    Must be set up after all other information has been filled.
    """ 
    __display_fields__ = ("default", "title", "methods")


ResourceDict.set_markers("default", "title", "description", "methods", "dev_info")
class_initializer (ResourceDict)
log_entry (__ref2, "Initialized!")


# Additional reference variables
ID = ResourceDict.ref_marker("id")
SHORTCUT = ResourceDict.ref_marker("shortcut")

def full_resource_url (*args, mode = "main"):
    return resources(args).format(**server_context_strings[mode])

def full_resource (*args, inquiry = "default", mode = "main"):
    return resources(args, inquiry=inquiry).format(**server_context_strings[mode])


# The dictionary:
resources = ResourceDict()


"""
HEADERS
"""
resources.add([],
    default = "{{api_server}}/",
    title = "{{context}}",
    description = "Host server.",
    dev_info = "The server itself.",
    methods=[])



"""
ACTUAL CONTENT:
"""

"""
ACCESS TOKEN
"""

resources.add(['access token'],
    default = '{{api_server}}/oauth2/access_token/',
    title = "Authentication",
    description = "Obtain 'access' and 'refresh' tokens to connect with {{api_server}} (Using {{authentication_standard}} standard).",
    methods = [POST])


"""
USER RESOURCES
"""

    # PROFILE & SETTINGS
    
resources.add(['user'],
    default = '{{api_server}}/{{api_version}}/me/',
    title = "User Profile",
    description = "User personal information and stats.",
    methods = [GET])
    #synonyms
resources.add_shortcut(['me'],['user'])
    
resources.add(['user', 'settings'],
    default = '{{api_server}}/{{api_version}}/me/settings/',
    title = "User Settings",
    description = "Manage user settings for their use of the {{api_server}} website.",
    methods = [GET, PUT])

    # FRIENDS
    
resources.add(['user', 'friends'],
    default = '{{api_server}}/{{api_version}}/me/friends/',
    title = "Friends",
    description = "Manage user friends within {{context_short}}.",
    methods = [GET, POST, DELETE])
    
resources.add(['user', 'friends', 'invitations'],
    default = '{{api_server}}/{{api_version}}/me/friends/invitations/',
    title = "Received Friend Requests",
    description = "Manage friend requests received by the user.",
    methods = [GET, POST, DELETE])
    
    # GAMES
    
resources.add(['user', 'games'],
    default = '{{api_server}}/{{api_version}}/me/games/',
    title = "User Games",
    description = "List of games in the user's {{context_short}} library.",
    dev_info = "Game detail can be viewed on /api/v1/games/{id}",
    methods = [GET])
    
resources.add(['user', 'games', 'upload sgf'],
    default = '{{api_server}}/{{api_version}}/me/games/sgf/',
    title = "Game Upload",
    description = "Upload a game file in SGF format to the user's {{context_short}} library.",
    dev_info = "You can use this endpoints to send multiple files using multipart form data",
    methods = [POST])
    
    # GROUPS
    
resources.add(['user', 'groups'],
    default = '{{api_server}}/{{api_version}}/me/groups/',
    title = "User Groups",
    description = "List of {{context_short}} groups the user belongs to.",
    dev_info = "Group details can be viewed on the main groups resource/api/v1/groups/{id}",
    methods = [GET])
    
resources.add(['user', 'groups', 'invitations'],
    default = '{{api_server}}/{{api_version}}/me/groups/invitations/',
    title = " Received Group Invitations",
    description = "Manage group invitations received by the user.",
    methods = [GET, POST, DELETE])
    
    # TOURNAMENTS
    
resources.add(['user', 'tournaments'],
    default = '{{api_server}}/{{api_version}}/me/tournaments/',
    title = "User Tournaments",
    description = "List of tournaments held on {{context_short}} in which the user participates.",
    methods = [GET])
    
resources.add(['user', 'tournaments', 'invitations'],
    default = '{{api_server}}/{{api_version}}/me/tournaments/invitations/',
    title = "Received Tournament Invitations",
    description = "Manage tournament invitations received by the user.",
    methods = [GET, POST, DELETE])
    
    # CHALLENGES
    
resources.add(['user', 'challenges'],
    default = '{{api_server}}/{{api_version}}/me/challenges/',
    title = "Personal Game Challenges",
    description = "List of game invitations sent or received by the user (direct challenges).",
    dev_info = "here is an easy way to just get a list of items for which you are the challenger /api/v1/me/challenges/?challenger={your user id}",
    methods = [GET])
    
resources.add(['user', 'challenges', ID],
    default = '{{api_server}}/{{api_version}}/me/challenges/{0}/',
    title = "Personal Challenge Detail",
    description = "Manage game invitations sent or received by the user (direct challenges).",
    dev_info = "This endpoint returns a single item, with the same data structure as /me/challenges",
    methods = [GET, DELETE])
    
resources.add(['user', 'challenges', ID, 'accept'],
    default = '{{api_server}}/{{api_version}}/me/challenges/{0}/accept/',
    title = "Accept Personal Challenge",
    description = "Accept a personal game offer by another player.",
    dev_info = "This will only work if you are the recipient of the challenge. Otherwise a 403 will be returned. When successfull the result will contain the id of the game which will be live and can be viewed on the games detail resource {{api_server}}/{{api_version}}/games/{id}",
    methods = [POST])
    
    # MAIL
    
resources.add(['user', 'mail'],
    default = '{{api_server}}/{{api_version}}/me/mail/',
    title = "Mail Inbox",
    description = "Internal mail service provided by {{context}}.",
    methods = [GET, POST])
    
resources.add(['user', 'mail', 'sent'],
    default = '{{api_server}}/{{api_version}}/me/mail/',
    title = "Sent Mail",
    description = "List of sent messages.",
    methods = [GET])
    
resources.add(['user', 'mail', ID],
    default = '{{api_server}}/{{api_version}}/me/mail/{0}/',
    title = "Mail Message",
    description = "View or discard the content of specific messages.",
    methods = [GET, DELETE])
    
    # VACATION
    
resources.add(['user', 'vacation'],
    default = '{{api_server}}/{{api_version}}/me/vacation/',
    title = "Vacation Time",
    description = "Manage the time for the user's vacations.",
    dev_info = "Vacation amount quantity is displayed in seconds",
    methods = [GET, PUT, DELETE])
    #synonyms
resources.add_shortcut(['user', 'vacations'],['user', 'vacation'])
    
    # NOTIFICATIONS
    
resources.add(['user', 'notifications'],
    default = '{{api_server}}/{{api_version}}/me/vacation/',
    title = "Notifications",
    description = "View notifications received by the user.",
    methods = [GET])
    

"""
PLAYER RESOURCES
"""

    # LIST & DETAILS
    
resources.add(['players'],
    default = '{{api_server}}/{{api_version}}/players/',
    title = "Players List",
    description = "List of all {{context}} accounts.",
    methods = [GET])
resources.add_shortcut(['player'],['players'])
    
resources.add(['players', ID],
    default = '{{api_server}}/{{api_version}}/players/{0}/',
    title = "Player Profile",
    description = "Detailed view of the player info and stats.",
    methods = [GET])
    
    # CHALLENGES
    
resources.add(['players', ID, 'challenge'],
    default = '{{api_server}}/{{api_version}}/players/{0}/challenge/',
    title = "Challenge",
    description = "Issue a direct game challenge to a specific player.",
    methods = [POST])
    
    # GROUPS
    
resources.add(['players', ID, 'groups'],
    default = '{{api_server}}/{{api_version}}/players/{0}/groups/',
    title = "Player Groups",
    description = "View the list of groups a player belongs to.",
    methods = [GET])
    
    # GAMES
    
resources.add(['players', ID, 'games'],
    default = '{{api_server}}/{{api_version}}/players/{0}/games/',
    title = "Player Games",
    description = "View the list of games involving a player.",
    methods = [GET])
    
    # LADDERS
    
resources.add(['players', ID, 'ladders'],
    default = '{{api_server}}/{{api_version}}/players/{0}/ladders/',
    title = "Player Ladders",
    description = "View the list of ladders a player has participated in.",
    methods = [GET])
    
    # TOURNAMENTS
    
resources.add(['players', ID, 'tournaments'],
    default = '{{api_server}}/{{api_version}}/players/{0}/tournaments/',
    title = "Player Tournaments",
    description = "View the list of tournaments a player has participated in.",
    methods = [GET])
    
    # ICON
    
resources.add(['players', ID, 'icon'],
    default = '{{api_server}}/{{api_version}}/players/{0}/icon/',
    title = "Player Icon",
    description = "View the player icon.",
    dev_info = "possibly png format, not yet supported",
    methods = [GET])

"""
OPEN CHALLENGES
"""

    # LIST & NEW CHALLENGES
    
resources.add(['challenges'],
    default = '{{api_server}}/{{api_version}}/challenges/',
    title = "Waiting Room",
    description = "Manage challenges open to all {{context_short}} players (within the restrictions of the challenger).",
    methods = [GET, POST])
    
resources.add(['challenges', ID],
    default = '{{api_server}}/{{api_version}}/challenges/{0}/',
    title = "Challenge Details",
    description = "View the details and conditions of specific open challenges.",
    methods = [GET, DELETE])
    
resources.add(['challenges', ID, 'accept'],
    default = '{{api_server}}/{{api_version}}/challenges/{0}/accept/',
    title = "Accept Challenge",
    description = "Accept an open challenge posted by another player.",
    methods = [POST])
    

"""
GAMES
"""

    # LIST & DETAILS

resources.add(['games'],
    default = '{{api_server}}/{{api_version}}/games/',
    title = "Games",
    description = "List of all games played in the {{context}}.",
    methods = [GET])
    
resources.add(['games', ID],
    default = '{{api_server}}/{{api_version}}/games/{0}/',
    title = "Game Details",
    description = "Information and details of a game.",
    dev_info= "Not the content of the game itself. Old games may lack some data, or be formatted differently.",
    methods = [GET])
    
    # REVIEWS
    
resources.add(['games', ID, 'reviews'],
    default = '{{api_server}}/{{api_version}}/games/{0}/reviews/',
    title = "Game Reviews",
    description = "List of reviews made of a game.",
    methods = [GET])
    
    # GAME STATE
    
resources.add(['games', ID, 'get sgf'],
    default = '{{api_server}}/{{api_version}}/games/{0}/sgf/',
    title = "Game File",
    description = "See the contents of a game",
    dev_info = "Content-Type: application/x-go-sgf",
    methods = [GET])
    
    # PLAYING
    
resources.add(['games', ID, 'move'],
    default = '{{api_server}}/{{api_version}}/games/{0}/move/',
    title = "Make a Move",
    description = "Send a move for one of the user's games.",
    dev_info = "SGF format, aa to ss, top left origin",
    methods = [POST])
    
resources.add(['games', ID, 'pause'],
    default = '{{api_server}}/{{api_version}}/games/{0}/pause/',
    title = "Pause a Game",
    description = "Stop the clock in one of the user's games.",
    methods = [POST])
    
resources.add(['games', ID, 'resume'],
    default = '{{api_server}}/{{api_version}}/games/{0}/resume/',
    title = "Resume a Game",
    description = "Resume a stopped clock in one of the user's games.",
    methods = [POST])
    
resources.add(['games', ID, 'pass'],
    default = '{{api_server}}/{{api_version}}/games/{0}/pass/',
    title = "Passing",
    description = "Send a passing move for one of the user's games.",
    methods = [POST])
    
resources.add(['games', ID, 'resign'],
    default = '{{api_server}}/{{api_version}}/games/{0}/resign/',
    title = "Passing",
    description = "Send a passing move for one of the user's games.",
    methods = [POST])

"""
REVIEWS
"""
    
    # LIST & DETAILS
    
resources.add(['reviews'],
    default = '{{api_server}}/{{api_version}}/reviews/',
    title = "Reviews",
    description = "List of reviews made in the {{context}}.",
    methods = [GET])
    
resources.add(['reviews', ID],
    default = '{{api_server}}/{{api_version}}/reviews/{0}/',
    title = "Review Details",
    description = "Information and details of a review.",
    methods = [GET])
    
    # REVIEW GAME STATE
    
resources.add(['reviews', ID, 'get sgf'],
    default = '{{api_server}}/{{api_version}}/reviews/{0}/sgf',
    title = "Review File",
    description = "See the contents of a review.",
    methods = [GET])
    

"""
DEMOS
"""
    
    # LIST & DETAILS

resources.add(['demos'],
    default = '{{api_server}}/{{api_version}}/demos/',
    title = "Demonstration Games",
    description = "List of demonstrarion games (\"demos\") made in the {{context}}.",
    methods = [GET])
    
resources.add(['demos', ID],
    default = '{{api_server}}/{{api_version}}/demos/{0}/',
    title = "Demo Details",
    description = "Information and details of a review.",
    methods = [GET])

   
   
"""
GROUPS
"""   

    # LIST & DETAILS
    
resources.add(['groups'],
    default = '{{api_server}}/{{api_version}}/groups/',
    title = "Groups",
    description = "View the list of groups within {{context}}, or create a new one.",
    methods = [GET, POST])
    
resources.add(['groups', ID],
    default = '{{api_server}}/{{api_version}}/groups/{0}/',
    title = "Group Details",
    description = "View or edit the details of a particular group.",
    methods = [GET, PUT])
    
    # NEWS
    
resources.add(['groups', ID, 'news'],
    default = '{{api_server}}/{{api_version}}/groups/{0}/news/',
    title = "Group News",
    description = "Manage the news posted in the group page.",
    methods = [GET, POST, PUT, DELETE])
    
    # MEMBERSHIP
    
resources.add(['groups', ID, 'members'],
    default = '{{api_server}}/{{api_version}}/groups/{0}/members/',
    title = "Group Membership",
    description = "Manage membership and administration of a group.",
    dev_info = "post to join/invite, put to admin/unadmin.",
    methods = [GET, POST, PUT, DELETE])
    
    # LADDERS
    
resources.add(['groups', ID, 'ladders'],
    default = '{{api_server}}/{{api_version}}/groups/{0}/ladders/',
    title = "Group Ladders",
    description = "View the ladder tournaments of the group.",
    methods = [GET])
    
    # IMAGES
    
resources.add(['groups', ID, 'icon'],
    default = '{{api_server}}/{{api_version}}/groups/{0}/icon/',
    title = "Group Icon",
    description = "Manage the group icon image.",
    dev_info = "Content-Type: image/png.",
    methods = [GET, PUT])
    
resources.add(['groups', ID, 'banner'],
    default = '{{api_server}}/{{api_version}}/groups/{0}/banner/',
    title = "Group Banner",
    description = "Manage the group banner image.",
    dev_info = "Content-Type: image/png.",
    methods = [GET, PUT])
    
   
"""
TOURNAMENTS
"""   

    # LIST & DETAILS
    
resources.add(['tournaments'],
    default = '{{api_server}}/{{api_version}}/tournaments/',
    title = "Tournaments",
    description = "View the list of tournaments held on {{context}}, or create a new one.",
    methods = [GET, POST])
    
resources.add(['tournaments', ID],
    default = '{{api_server}}/{{api_version}}/tournaments/{0}/',
    title = "Tournament Details",
    description = "View or edit the details of a particular tournament.",
    methods = [GET, PUT, DELETE])
    
    # PARTICIPATION
    
resources.add(['tournaments', ID, 'participants'],
    default = '{{api_server}}/{{api_version}}/tournaments/{0}/players/',
    title = "Tournament Participants:",
    description = "View the list of participants of a particular tournament.",
    dev_info = "this is not in api docs. Delete to leave/disqualify?, post to join/invite, put to change gamepoints/disqualify?",
    methods = [GET, POST, PUT, DELETE])
    # synonyms
resources.add_shortcut(['tournaments', ID, 'players'], ['tournaments', ID, 'participants'])
    
    # MANUAL START
    
resources.add(['tournaments', ID, 'start'],
    default = '{{api_server}}/{{api_version}}/tournaments/{0}/start',
    title = "Start Tournament",
    description = "Start a tournament manually.",
    methods = [POST])
    
    # GAMES AND ROUNDS
    
resources.add(['tournaments', ID, 'rounds'],
    default = '{{api_server}}/{{api_version}}/tournaments/{0}/rounds/',
    title = "Tournament Rounds & Matches:",
    description = "View the list game matches, organized by rounds.",
    methods = [GET])
    # synonyms:
resources.add_shortcut(['tournaments', ID, 'matches'], ['tournaments', ID, 'rounds'])
resources.add_shortcut(['tournaments', ID, 'rounds & matches'], ['tournaments', ID, 'rounds'])
resources.add_shortcut(['tournaments', ID, 'rounds and matches'], ['tournaments', ID, 'rounds'])
resources.add_shortcut(['tournaments', ID, 'rounds/matches'], ['tournaments', ID, 'rounds'])
resources.add_shortcut(['tournaments', ID, 'rounds&matches'], ['tournaments', ID, 'rounds'])


"""
LADDERS
"""   

    # LIST & DETAILS
    
resources.add(['ladders'],
    default = '{{api_server}}/{{api_version}}/ladders/',
    title = "Ladder Tournaments",
    description = "View the list of ladders held on {{context}}.",
    methods = [GET])
    
resources.add(['ladders', ID],
    default = '{{api_server}}/{{api_version}}/ladders/{0}/',
    title = "Ladder Details",
    description = "View  the details of a particular ladder.",
    methods = [GET])
    
    # Participation
    
resources.add(['ladders', ID, 'participants'],
    default = '{{api_server}}/{{api_version}}/ladders/{0}/players/',
    title = "Ladder Tournament Participants",
    description = "View the participants of a particular ladder.",
    methods = [GET, POST, DELETE])
    # synonyms
resources.add_shortcut(['ladders', ID, 'players'], ['ladders', ID, 'participants'])
    
    
"""
PUZZLES
"""   

    # LIST & DETAILS
    
resources.add(['puzzles'],
    default = '{{api_server}}/{{api_version}}/puzzles/',
    title = "Problems/Tsumego Library",
    description = "View the list of puzzles in {{context_short}}'s problem library.",
    methods = [GET, POST])
    # synonyms
resources.add_shortcut(['problems'], ['puzzles'])
resources.add_shortcut(['tsumego'], ['puzzles'])
    
resources.add(['puzzles', ID],
    default = '{{api_server}}/{{api_version}}/puzzles/{0}/',
    title = "Problems Details",
    description = "View the details of a particular puzzle.",
    methods = [GET, PUT, DELETE])
    
    # COLLECTIONS
    
resources.add(['puzzles', 'collections'],
    default = '{{api_server}}/{{api_version}}/puzzles/collections/',
    title = "Problems Collections",
    description = "View the list of puzzle collections in {{context_short}}'s problem library.",
    methods = [GET, POST])
    

"""
THE LIVE SERVER
"""
    
resources.add(['live'],
    default = '{{api_live_server}}/',
    title = "{{context}} Live Connections",
    description = "Live host server.",
    dev_info = "Use this section for socket connections that require live interactions",
    methods = [GET, POST])


    

    
    
resources.setup_hack()
log_entry (__ref1, "Done. Ready!")

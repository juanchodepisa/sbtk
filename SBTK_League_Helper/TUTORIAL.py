##########################################################################
##                 A Comfortably Executable Walk-Through.               ##
##                                                                      ##
## I'll keep this file as clean as possible, so that it is literally &  ##
## straight-forwardly readable. For everything else:                    ##
                                                                        ##
import other_stuff as FOO                                               ##
                                                                        ##
## so that you can recognize what is not important                      ##
##########################################################################

## These are the variables we are going to need
username = None
client_id = None
client_secret = None
password = None
keys = None
my_password = None
id_card = None
result = None
my_id = 0
my_country = None
message = ""

try:

    FOO.title("WELCOME TO THE SBTK PROJECT")
    FOO.first_text("\n No ASCII-Arts this time, sorry :(",

    ###############
    ## SECTION 1 ##
    ###############
    """

    I. FIRST THINGS FIRST:


    1- You need to get your own CLIENT ID and CLIENT SECRET, so that you'll be logging in from your own copy of the script. \
    So go here https://online-go.com/developer and create one. Congratulations! you're "officially" a developer.

    2- You need your own client PASSWORD, also provided by OGS. So here https://online-go.com/user/settings there's \
    an Application Specific Password: you should create one. You've probably done this much so far.""""""\
    If you havent, go now, and get the three keys, and come back when you're ready. I'll be waiting for you...""")
    FOO.text("""\
    3- Now you'll store your keys.""","""Yeah, you heard it right, store them.""",
    """
    -- But what about that "not checking [the keys] in to source control" I read about in OGS Api? --""",
    """
    Well, tough luck, buddy!""",
    """Fortunately, we can get along just fine. I'll obfuscate the keys for you.
    It's a simple and very breakable XOR encryption, but since you'll only be storing your own, \
    and your custom chosen password you won't need to write down anywhere, this is as good as it gets.
    (Also Leira is telling me he hopes to come up with a better system later on)

    """,
    end ="")

    FOO.text("""
    We need to import the proper modules for this purpose:
    These files can be found at the src/security directory

    """)

    #############################
    ## imports are important

    from src.security.key_handling import get_keys_directory, set_keys_directory
    from src.security.exceptions import KeysDirectoryNotFound
    FOO.echo_import (get_keys_directory, set_keys_directory, KeysDirectoryNotFound)

    #############################

    ## Here be some console print-outs.
    ## You'll see some of those whenever you execute any
    ## of the functions mentioned here.

    ## Example:
    ## 1: @0 A reading operation begins...
    ## 2: @567 [1] You see? It took you about half a second to read the sentence in line [1].

    FOO.text("","""
    That nonsense over there is our very own event logging. Admittedly, this was programmed before becoming \
    aware that Python has logging functions on its own.
    Nevertheless this one suits our purposes: you get an entry number "n:", followed by a timestamp "@ms", \
    then an optional follow-up indicator [m] when the entry refers to a previous operation, and then the \
    explanation of whatever has just happened.""",
    """\
    Now, back to the keys: You'll notice that some keys_loc.json file was mentioned, this file contains an index \
    of the location of your key files, once they are created.
    """)

    ## Asking for username
    while not FOO.flow_control_is(True):
        username = FOO.question("""
        Now please enter your username: """)
        while not username:
            FOO.text("Name cannot be blank.", skip = True)
            username = FOO.question("""
            Now please enter your username: """)
        FOO.text("""
        Nice to meet you {username}.""".format(username = username), skip = True)
        if not FOO.ANNOYANCE:
            FOO.text("""\
            I am TUTORIAL, and as you can see, I'm a very basic user interface.""", skip = True)
            FOO.ANNOYANCE = True
        FOO.yn_question("""Are you sure your username is correct?""")


    FOO.text("""
    The next step is to attempt retrieving your keys using retrieve_keys(). This function automatically calls \
    the function that retrieves the keys location and does all the interpretation.""",
    """
    However for the purpose of this tutorial, I'll check step by step, which will be redundant but self explanatory.
    First I'll call

    >> get_keys_directory({username})

    which will look into keys_loc.json . Beware the possible KeysDirectoryNotFound.


    """.format(username = repr(username)), end = "")

    #############################
    ## This is a good way to start checking,
    ## although in most cases you'll know beforehand if the keys are there
    #############################
    try:
        directory = get_keys_directory(username)
        FOO.change_flow(True)
        FOO.text("\n\nSo, apparently, you've been here before. Good!")
    except KeysDirectoryNotFound:
        FOO.text("""\n
        Alas! I couldn't find any valid directory belonging to you.
        But don't you worry, we'll get there.""")


    #############################
    ## And thus we set the keys directory
    ## this can be anywhere on your disk
    #############################
    if not FOO.flow_control_is(True):
        directory = FOO.question("""
        Please type a valid directory where you want to store your keys.
        Full path: """)
        while not FOO.valid_directory(directory):
            directory = FOO.question("""
            That directory is not valid, please try again.
            Full path: """)

        FOO.text("""
        Right, I'll call

        >> set_keys_directory({username}, {directory})

        for ya. \
        Bear in mind this method makes no attemp at data validation.
        \n""".format(username = repr(username), directory = repr(directory)))

        set_keys_directory(username, directory)
        

    FOO.text("""\n
    The next step is to setup those keys we talked about at the beginning. \
    We need to put them in Python's dict format.
    """)

    def ask_for_keys(force_change = False): ## Asks for keys, what else?
        global client_id, client_secret, password, keys
        if force_change:
            FOO.change_flow(True)
        else:
            FOO.yn_question ("""\
            Do you want to set up new keys?""")
        while FOO.flow_control_is(True):
            FOO.text("""
            Please type in your keys as asked""", skip = True)
            client_id     = FOO.question ("... Client ID ..: ")
            client_secret = FOO.question (". Client Secret : ")
            password      = FOO.question ("... Password ...: ")
            keys = {'client_id': client_id, 'client_secret': client_secret, 'password': password}
            FOO.yn_question ("""\
            Do you want to make any changes to the previous keys?""")

        FOO.text("""
        Alright! It seems you have your keys ready and you're good to go!
        """)
    ask_for_keys()



    FOO.text("""
    And that was the first part. \
    You're lucky today, I found a piece of ASCII cake laying around, so you may have it :D
    
    """, skip = True)
    FOO.title(r"""
            _.-.             
          .' _  \            
        ,'  (_)  \_          
    _.-|`-._      \""--._    
  .' .-(=._ `-._   \""-. `.  
 /  /  |   `=.  `-._\   \  \ 
|  |    `-._  `=._  | .  |  |
 \  \  ;' .,`--._ `=| ' /  / 
  `._``--..._____`--'-''_.'  
hjw  `--.._________..--'     

    """, skip = True)
    FOO.text("""
    ... :/ uhmmmm, I know, it's not much, shall we continue? ...
    """)

    ###############
    ## SECTION 2 ##
    ###############
    FOO.text("""


    II. PASSWORD:""",
    """(alias not "password", "12345" or "asdf", I'll be watching you!)""",
    """

    1- This is a custom password, and will be used to rather obfuscate your keys, so that they mean nothing without it. \
    Please choose something easy to remember, you won't be needing to store this anywhere.

    2- The rules:
    * At least 10 characters long.
    * Only alphanumeric characters, "." and "-" are permitted.
    """,
    end ="")

    ## Asking for password
    def ask_for_password():
        global my_password
        FOO.change_flow(True)
        while FOO.flow_control_is(True):
            my_password = FOO.question("""
            Now please enter your custom password.
            Create a new one if you don't have one already.

            Password: """)
            if not FOO.ANNOYANCE and my_password:
                FOO.text("""
                Oops, sorry! That was plain-text. Don't worry, this is no error, it's just that \
                I can't help it, because there's no cross-platform Python \
                function that I know of which has predictable 'asterisk' behavior.""",
                """
                Also, you're the developer, it's up to you to create your desired behavior. I'm \
                but a humble automatic TUTORIAL.""", end = "")
                FOO.ANNOYANCE = True
            elif not my_password:
                if not FOO.ANNOYANCE2:
                    FOO.text("""
                    Really!? No password? Well, we've got a badass here, your call.""", end = "")
                    FOO.ANNOYANCE2 = True
                else:
                    FOO.text("<blank password>", end = "", skip = True)
            FOO.yn_question("""
            Do you want to change your password?""")
    FOO.ANNOYANCE = False
    ask_for_password()

    if my_password:
        FOO.text("""
        Now, let's validate your password.
        This is redundant again: you can directly try store_keys() or try retrieve_keys() and those \
        will raise the same exception.""",
        """\
        Let's import the appropriate functions. These are also found in the src/security directory.
        """)
        #############################
        ## imports are important

        from src.security.obfuscation import password2int
        from src.security.exceptions import PasswordError
        FOO.echo_import (password2int, PasswordError)

        #############################
        FOO.text("","""
        I will try the call

        >> password2int('{password}') # <- Your password goes here

        and this will raise a PasswordError if the password is inappropriate.""".format(password = "*"*len(my_password)))

        while True:
            try:
                if my_password:
                    password2int(my_password)
                    FOO.text("Excelent! Your password is good.")
                else:
                    FOO.text("No password also works I guess :(")
                break
            except PasswordError as e:
                FOO.text("""\
                Alas! Your password has a problem. I maneuvered quickly and caught it on the fly.""",
                """\
                PasswordError.description shall reveal the cause:""",
                e.description)
                FOO.ANNOYANCE = True
                ask_for_password()
    else:
        FOO.text("No password also works I guess :(")

    # Storing the keys
    def store_keys_routine():
        FOO.text("""
        So, we'll store the keys you provided.
        """)
        try:
            store_keys
        except NameError:
            FOO.text("""\
            First we need to import store_keys, which is found in src/security/key_handling.py
            """)
            
            ####################################
            ## imports are important

            from src.security.key_handling import store_keys
            FOO.echo_import (store_keys)
            FOO.text("", end = "")
            
            ####################################
            
        FOO.text("""
        Now I will call

        >> store_keys({username},{{...}},'***') # <- Your keys and password go here
        
        This function has other optional fields. Most relevantly context='OGS' is default \
        behavior, but it can be changed to 'OGS_Beta for testing.'""".format(username = repr(username)))
        
        while not FOO.flow_control_is(True):
            try:
                store_keys(username, keys, my_password)
                FOO.text("""
                We've successfully stored your keys. Now you can simply use your username and \
                password to retrieve them every time.
                """)
                FOO.change_flow(True)
            except ValueError as e:
                FOO.text("""
                Something about your keys doesn't look right...
                I got this error message: {error}
                """.format(error = e))
                ask_for_keys(force_change = True)
    if keys:
        store_keys_routine()
        
    
    FOO.text("""
    And along goes the second part.""",
    """
    What?, more ASCII cake?, sorry that was all I had.
    """,
    ###############
    ## SECTION 3 ##
    ###############
    """


    III. RETRIEVING THE KEYS:
    
    
    1- If you lost your keys you have no one to blame but yourself.
    
    2- It's the same as storing them but the other way around.
    
    3- Nothing too fancy, just import... you know what? I'll do that for you, because \
    Leira here is saying he's not even trying anymore:
    
    """,
    end ="")
    ####################################
    ## imports are important

    from src.security.key_handling import retrieve_keys
    from src.security.exceptions import KeysFileNotFound
    FOO.echo_import (retrieve_keys, KeysFileNotFound)
    
    ####################################
    FOO.text("","""
    You know how it goes, now I tell you the proper function call:
    
    >> keys = retrieve_keys({username},'***') # <- Your password goes here

    and that should be enough... unless there is an error, so try-except, y'know?\
    """.format(username = repr(username)),
    """Also, should you want to test on the Beta Server, you should add context='OGS_Beta' \
    as a keyword to the function.
    """,
    end = "")
    
    while not FOO.flow_control_is(True):
        try:
            keys = retrieve_keys(username, my_password)
            FOO.change_flow(True)
        except KeysFileNotFound as e:
            FOO.text("""
            Now, I had said you had your keys ready, but now I take it back. There was a KeysFileNotFound exception.
            
            As with other custom exceptions on this package, this one comes with a fancy description: \
            {error_message}
            """.format(error_message = e.description),
            "In other words: 'This is not the file you're looking for'.")
            ask_for_keys(force_change = True)
            store_keys_routine()

    FOO.text("""
    Your storage system is finally ready! Congratulations!
    """)

    
    FOO.text(
    ###############
    ## SECTION 4 ##
    ###############
    """

    IV. INTO OGS:
    (The fun part)
    
    
    1- You'll be pleased to discover that everything we did so far is unnecessary. Well, \
    to be fair, once you store the keys, you need one object and one object only:""",
    """
    >> Authentication
    ""","""
    2- Where's this located? 
    Something-something/src/interfacing/ogs/connect.py""",
    """\
    Why such a long path?
    Well, that would be because Leira is delusional.
    """,
    """\
    3- This object __init__s itself by connecting to the server, so that's out of the way. \
    It contains methods called head, get, options, put, post, delete; which mirror http requests \
    as required by OGS API.
    
    4- All paths provided by the API are hardcoded in a custom dictionary, which makes access fairly easy.
    
    
    So, shall we begin?""",
    end ="")
    ####################################
    ## imports are important

    from src.interfacing.ogs.connect import Authentication
    from urllib.error import URLError, HTTPError
    from src.interfacing.ogs.resources import resources
    FOO.echo_import (Authentication, URLError, HTTPError)
    
    ####################################
    FOO.text("","""
    We've also imported the variable 'resources' (from src/interfacing/ogs/resources.py). This is the dictionary that contains all recognizable paths.
    Moreover, you can try 'guessing' a path, and even if it is not registered and it will try to accomodate as \
    best it can.\
    ""","""\
    Now we just need to create an Authentication object, and we are good to go:
    
    >> id_card = Authentication({username},'***') # <- Your password goes here
    
    From now on, we'll be connecting to the OGS Server, and send requests from your account. \
    These requests WILL have an effect on the server, so, thread with care.""".format(username = repr(username)))
    
    FOO.change_flow(True)
    while FOO.flow_control_is(True):
        try:
            id_card = Authentication(username, my_password)
            FOO.text("""
            Success!!! You've been authenticated.
            That means you've been given an access token, and a refresh token, \
            and you need to specify the Bearer and ...""",
            """
            -- NOPE! I have my id_card! --
            """,
            """You're damn right! It'll do all that stuff for ya.
            ""","""
            You could also try on the Beta Server by calling:
            
            >> id_card = Authentication({username},'***', testing = True) # <- Your password goes here
            
            but bear in mind you would need to create an account there, and require a different set of keys.
            We will not be doing that today, because we are too cool for the Beta Server.
            """.format(username = repr(username)), end = "")
            FOO.flow_continue()
            
        except HTTPError as e:
            FOO.text("""
            I received an error while trying to authenticate your keys:
            ERROR {error.code}: {error.reason}
            """.format(error = e))
            FOO.custom_error_auth(e)
            FOO.yn_question("Do you want to try again?")
        except URLError as e:
            FOO.text("""
            I received an error while trying to connect to the web:
            {error}
            
            My limited knowledge tells me that something might be wrong with your internet \
            connection, but it might also be some other problem.
            """.format(error = e))
            FOO.yn_question("Do you want to try again?")
    

    if FOO.flow_continue():
        try:
            FOO.text("""
            Now let me show you the tree of those resources I talked about before:
            """)
            FOO.safe_print(str(resources))
            FOO.text("","""\
            Yeah, I know! It's quite large.
            """,end="")
        except Exception:
            FOO.text("""
            Alas! Some unknown error occured. Nevermind, let's just continue...
            """)        
    
        FOO.yn_question("Do you want to see the examples?")
        
    FOO.ANNOYANCE = 0
    FOO.ANNOYANCE2 = False
    while FOO.flow_control_is(True):
        try:
            if FOO.ANNOYANCE == 0:
                FOO.text("""
                All API requests are sent to specific addresses within the API Server. I suggest you take a good \
                read at http://docs.ogs.apiary.io/ to get the basic idea of the functionalities.""","""\
                You can also check the contents of src/interfacing/ogs/resources.py, which contains a more exhaustive \
                list than what appears in OGS documentation.
                """,
                """
                OK, first a fool's proof example (just GET from address):
                
                >> id_card.get(['user'])
                
                to retrieve your user information. This comes in json format, which our daemons will \
                easily take care of, and transform into Python built-ins.
                """,end = "")
                FOO.ANNOYANCE += 1
            elif FOO.ANNOYANCE == 1:
                FOO.text("""
                >> id_card.get(['user'])""")
                
            if FOO.ANNOYANCE == 1: 
                result = id_card.get(['user'])
                my_id = result['id']
                
                FOO.builtin(result)
                FOO.text("""\
                Another way to get information about yourself is using your id number:
                
                >> id_card.get(['player', {id}])
                
                Here the id could be any other number, our custom dictionary takes care of that.
                """.format(id = my_id),end = "")
                FOO.ANNOYANCE+=1
            elif FOO.ANNOYANCE == 2:
                FOO.text("""
                >> id_card.get(['player', {id}])""".format(id = my_id))
                
            if FOO.ANNOYANCE == 2: 
                result = id_card.get(['player', my_id])
                
                FOO.builtin(result)
                if result['supporter'] and not FOO.ANNOYANCE2:
                    FOO.text("Site supporter, huh? Good on you ;)")
                    FOO.ANNOYANCE2 = True
                    
                my_country = result["country"]
                
                FOO.text("""\
                Now on to a more complicated example. \
                GET requests may take query parameters to retrieve a more specific resource:
                
                >> id_card.get(['players'], query_param ={{'country':{country}, 'ordering':'-rating', 'numProvisional':0}})
                
                This will show you a list of the strongest players registered for your country.
                """.format(country = my_country),end = "")
                FOO.ANNOYANCE+=1
            elif FOO.ANNOYANCE == 3:
                FOO.text("""
                >> id_card.get(['players'], query_param ={{'country':{country}, 'ordering':'-rating', 'numProvisional':0}})\
                """.format(country = my_country))
            
            if FOO.ANNOYANCE == 3:
                result = id_card.get(['players'], {'country': my_country, 'ordering': '-rating', 'numProvisional': 0})
                
                FOO.builtin(result)
                
                FOO.text("""
                Most generic GET requests are possible even without authentication. This is because \
                they are not supposed to change the state of the server.""",
                """\
                Conversely, POST, PUT and DELETE requests (almost) always will require it. So we'll try \
                something harmless.
                You are going to send a message to yourself.""")
                
                message = FOO.question("Please type in a message: ")
                
                
                FOO.text("""
                POST requests have application parameters instead of query parameters, which are sent \
                within the message rather than the url. In our case we do it like this
                
                >> id_card.post(['user', 'mail'], 
                .............>> app_param = {{'recipients':[{username}],
                ..........................>> 'subject':'Auto message',
                ..........................>> 'body':"..."}})\
                """.format(username = repr(username)), end = "")
                FOO.ANNOYANCE+=1
            elif FOO.ANNOYANCE == 4:
                FOO.text("""
                >> id_card.post(['user', 'mail'], 
                .............>> app_param = {{'recipients':[{username}],
                ..........................>> 'subject':'Auto message',
                ..........................>> 'body':"..."}})\
                """.format(username = repr(username)))
            
            if FOO.ANNOYANCE == 4:
                id_card.post(['user', 'mail'], 
                             app_param = {'recipients': [username],
                                          'subject'   : 'Auto message',
                                          'body'      : FOO.arrange_automail(username, message)})
                
                
                FOO.text("""
                Done! Please check your OGS mail.""",
                """
                So, I hope this helped explain a bit how the whole system works. \
                I'll have more examples for you in the future.""", end = "")
        
        except HTTPError as e:
            FOO.text("""
            Hmmmmm, your request was met with an error:
            ERROR {error.code}: {error.reason}
            
            This is odd because it normally works. I'll refresh your credentials.""".format(error = e))
            try:
                id_card.refresh_auth()
                FOO.text("""Well, it seems that worked""", end = "")
            except (HTTPError, URLError):
                FOO.text("""No luck, it must be something else.""", end = "")
            FOO.yn_question("Do you want to try again?")
        except URLError as e:
            FOO.text("""
            Oh snap! The internet just tricked us buddy!
            
            I received this error:
            {error}
            
            Please check your connection.""".format(error = e))
            FOO.yn_question("Do you want to try again?")
    

    ####################################################################################################################
    FOO.text("""
    Finally, an 'Easter Egg', as a reward for completing this tutorial:
    You can (almost always) type 'skip' to jump to the next important part of the tutorial. \
    This way you can avoid repeating what you've already learned.\
    """,
    """\
    Even more awesome: you can pass strings as arguments from the Terminal, sit back, and watch it \
    as the input autocompletes :O
    """)
    print("""\
Hint: 
    
python {file} SKIP {username} Y SKIP N SKIP yourpassword SKIP N SKIP
""".format(file = FOO.FILENAME, username = username))
    FOO.text("", end ="")
    
    if not FOO.ANNOYANCE2:
        FOO.text("""\
        Oh! also you can leave 'Password' blank if you would rather store your keys in plain-text. \
        After all nobody cares about spying on our private documents, right?""",
        """\
        ... Right!? :S
        """)

    FOO.text("""
    And that's it! This was TUTORIAL, your friendly Turing test subject wannabe.
    I'll now fade into the oblivion of sys.exit().

    I wish you a nice day :)
    """)

except KeyboardInterrupt:
    FOO.separator()
    
    FOO.title(r"""
#######################################################
##   __    _   ____   _____   ______    __  __  __   ##
##  |  \  | | /    \ |  __ \ |  ____|  |  ||  ||  |  ##
##  |   \ | ||  /\  || |__) )| |___    |  ||  ||  |  ##
##  | |\ \| || |  | ||  ___/ |  ___|    \/  \/  \/   ##
##  | | \   ||  \/  || |     | |____    __  __  __   ##
##  |_|  \__| \____/ |_|     |______|  |__||__||__|  ##
##                                                   ##
##     KEYBOARD INTERRUPT IS THE DIGITAL VERSION     ##
##             OF A PUNCH TO THE FACE                ##
##                                                   ##
#######################################################
    """, skip = True)
    FOO.text("\n\n So you're leaving already?\n Well have a nice day :)\n")
    
    

except Exception as e:
    FOO.separator()
    FOO.text("""

    Aghck! I've got an uncaught Exception X(

    That... that didn't feel right... my bits are confused""",
    """
    The error looks like this:
    Error type: {error.__class__.__name__}
    Arguments: {error.args}""".format(error = e),
    """
    Leira is telling me that he's tired of tries and excepts, \
    even as he keeps writing me, \
    and that I should go some-unknown-word myself.""",
    """
    Must be a human thing, but it rhymes with 'luck'.

    Anyway, please start over and make sure you entered the correct user \
    and keys, and stuff. I'll go flush my memory.""", end = "")
    FOO.text("""

    Have a nice day :S
    """)
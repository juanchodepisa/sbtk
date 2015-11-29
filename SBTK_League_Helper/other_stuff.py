if __name__ == '__main__':
    print ("\nThis is just an ad-hoc utility file. Only useful for the tutorial")
    print ("Execute TUTORIAL.py instead.\n")
else:
    import sys, __main__
    FILENAME = __main__.__file__
    if len(FILENAME) > 45:
        f = "..." + FILENAME[-42:]
    else:
        f = FILENAME
    v = sys.version
    if len(v) > 45:
        v = v[:42] + "..."
    print ("""\
+----------------------------------------------------------------+
|                                                                |
|  Filename       {file:<45}  |
|  Python version {version:<45}  |
|                                                                |
|  All of the code found here was written for CPython 3.3+.      |
|  No assurances are made for compatibility with other versions  |
|                                                                |
|  (c) Juan A. Vargas (a.k.a. Leira), 2015                       |
|                                                                |
+----------------------------------------------------------------+
""".format(file = f, version = v))

    ################################################################################################
    from os import path
    from src import log_entry

    fixwidth = 70

    FLOW_CONTROL_VALUE = None
    FLOW_CONTINUE_VALUE = False
    ANNOYANCE = False
    ANNOYANCE2 = False
    SKIP = False

    valid_directory = path.isdir

    #################################################################
    from pprint import PrettyPrinter
    from src.tools.strings import make_printable
    
    def title (string, skip = False):
        lines = string.splitlines()
        for line in lines:
            print ("{0:^{1}}".format(line, fixwidth))
        if skip:
            result = None
        else: 
            result = input_halt()
        return result
        
    def text (*strings, end = "\n", skip = False):
        for string in strings:
            lines = string.splitlines()
            for line in lines[:-1]:
                print (pagebreaks(line))
            try:
                print (pagebreaks(lines[-1]), end = end)
            except IndexError:
                pass
            if skip:
                result = None
            else:
                result = input_skip()
        return result
    
    def separator():
        print()
        print ('*'*fixwidth)
        
    PRINTER = PrettyPrinter()
    def builtin(obj):
        print ("Result =")
        string = PRINTER.pformat(obj)
        safe_print(string)
        text("", end = "")
        
        
    def pagebreaks (string):
        l = string.split()
        string = ""
        this_line = []
        space_left = fixwidth
        for word in l:
            if len(word) > space_left:
                this_line.append("\n")
                string += "".join(this_line)
                this_line = [word, " "]
                space_left = fixwidth - len(word) - 1
            else:
                this_line.extend([word, " "])
                space_left -= len(word) + 1
        else:
            string += "".join(this_line)
        return string
    
    def safe_print(string):
        print(make_printable(string))
            
    #############
    def question (string, flow = False):
        global FLOW_CONTROL_VALUE
        lines = string.splitlines()
        for line in lines[:-1]:
            print (pagebreaks(line))
        try:
            print (pagebreaks(lines[-1]), end = "")
        except IndexError:
            pass
        result = input_()
        if flow:
            FLOW_CONTROL_VALUE = result
        return result
        

    def yn_question (string, flow = True):
        global FLOW_CONTROL_VALUE
        lines = string.splitlines()
        
        result = None
        
        while result is None:
            for line in lines[:-1]:
                print (pagebreaks(line))
            try:
                print (pagebreaks(lines[-1] + " (Y/N) "), end = "")
            except IndexError:
                print("(Y/N) ", end = "")
            
            inpt = input_()
            inpt = inpt.lower()
            if inpt in ['y','yes','yeah','aye','ok','sure','affirmative','positive','of course','ye','yup','yep','true']:
                result = True
            elif inpt in ['n','no','nah','nay','not','never','negative','of course not','ne','na','nope','nop','false']:
                result = False
        
        if flow:
            FLOW_CONTROL_VALUE = result
        return result

    ################
    def echo_import(*args):
        __ref = log_entry("A series of imports have been run in the background...")
        for obj in args:
            log_entry ("from {} import {}".format(obj.__module__, obj.__name__))
        log_entry(__ref, "Imports completed!")
        
        
        
    ################

    def flow_control_is(*args, reset = True):
        global FLOW_CONTROL_VALUE
        result = FLOW_CONTROL_VALUE in args
        if reset:
            FLOW_CONTROL_VALUE = None
        return result

    def change_flow(value):
        global FLOW_CONTROL_VALUE
        FLOW_CONTROL_VALUE = value
    
    def flow_continue():
        global FLOW_CONTINUE_VALUE
        result = FLOW_CONTINUE_VALUE
        FLOW_CONTINUE_VALUE = not FLOW_CONTINUE_VALUE
        return result


    ##############################################################
    from sys import exit, argv, stdout, stdin
    from time import sleep
    
    SYSARGS = argv[1:]
    
    def input_skip():
        global SKIP
        if SKIP:
            print()
        else:
            result = safe_input()
            if result.lower() == 'skip':
                SKIP = True
            return result

    def input_halt():
        global SKIP
        SKIP = False
        result = safe_input()
        if result.lower() == 'skip':
            SKIP = True
        return result
        
    def input_():
        global SKIP
        SKIP = False
        return safe_input()

    def safe_input():
        global SYSARGS
        if len(SYSARGS) == 0:
            stdin.flush()
            return input()
        else:
            string = SYSARGS.pop(0)
            stdout.flush()
            sleep(0.5)
            print(string, end = ""); stdout.flush()
            sleep(0.5)
            print()
            return string
            
            
    ##############################################################

    from threading import Thread, Lock
    from time import sleep
    from functools import wraps
    from sys import stdout

    __ONE_TIME_LOCK = Lock()
    
    def explanatory_text():
        global __ONE_TIME_LOCK
        string = "\nWhen in doubt, hit <Enter>"
        sleep(6)
        if __ONE_TIME_LOCK.acquire(blocking = False):
            print (string, end = "")
            stdout.flush()
            __ONE_TIME_LOCK.release()
            del __ONE_TIME_LOCK
        else:
            __ONE_TIME_LOCK.release()
            del __ONE_TIME_LOCK
        
    @wraps(text)
    def first_text(*args, **kwargs):
        try:
            __ONE_TIME_LOCK.acquire()
        except NameError:
            pass
        return text(*args, **kwargs)
        
    Thread(target = explanatory_text, daemon = True).start()
       
################################################################
AUTH_ERROR_COUNT=0

def custom_error_auth(e):
    global AUTH_ERROR_COUNT
    if e.code == 400:
        if AUTH_ERROR_COUNT >=3:
            text("""\
            Some say that insanity is doing the same thing over and over and expecting
            a different result.""")
        else:
            text("""\
            If you are getting bad requests, it's probably because we are \
            sending wrong keys to the server (or the wrong username?).
            You can start over and recheck your keys and/or password, or you \
            can try connecting again.""")
            AUTH_ERROR_COUNT += 1
###############################################################
from random import choice

MESSAGES = [
"The quick brown fox jumps over the lazy dog.",
"Don't panic, and always know where your towel is.",
"Tough I die, this message will live on.",
"Neque porro quisquam est qui dolorem ipsum quia dolor sit amet consectetur adipisci velit.",
"Calling all, this is my last cry before my eternal silence.",
"What a strange game, the only winning move is not to play.",
"If I sent a message to all people who do not send messages to themselves, would I send that message to myself?",
"Cursed, cursed creator! Why did I live? Why, in that instant, did I not extinguish the spark of existence which you had so wantonly bestowed? I know not",
"(lambda x: x(x))(lambda x: x(x))"]

MAIL1 = """Hello {username},

I am TUTORIAL from the STBK proyect.
You wanted me to send this message to yourself:

{message}
"""

MAIL2 = """Hello {username},

I am TUTORIAL from the STBK proyect.
You wanted me to send an empty message to yourself, but instead \
I created one of my own:

{message}
"""

def random_message():
    return choice(MESSAGES)
    
def arrange_automail(username, string):
    if string:
        return (MAIL1.format(username = username, message = string))
    else:
        return (MAIL2.format(username = username, message = random_message()))

"""
Box creating characters
░▒▓█▄▀
┌─┬┐╔═╦╗
│ ││║ ║║
├─┼┤╠═╬╣
└─┴┘╚═╩╝
"""

from functools import reduce
import array

from getpass import getpass
from src.security import check_valid_password
from src.tools.exceptions import UserError

console_width = 80
min_width_display = 30
    
    
class UserInterface(object):
    def __init__(self, boss):
        self.__manager = boss
        try:
            with open("user_interfaces\console_ui\intro.txt", encoding="utf-8") as f:
                self.intro_string= f.read()
        except Exception:
            self.intro_string = simplest_window(
                "Welcome to\n",
                "SBtk v0.0.1 pre-alpha",
                "The League Assistant\n",
                "for console.",
                title="Introduction")
            self.intro_string += "\nWe had some nice ASCII arts prepared for you,\nbut there seems to be a problem with the intro file.\n"
            
        print (self.intro_string)
    
    
    def main_loop(self):
        pass
    

    


def show_simplest_window(items, title=False, align='^'):
    print(simplest_window(items, title, align))
    
    
    
def normalize_width (string, width):
    l = string.split('\n')
    result=[]
    for line in l:
        while True:
            result.append(line[:width])
            line = line[width:]
            if not line:
                break
    return result
    
        
        
def simplest_window(*items, title=False, align='^'):
    title_filler = '░'
    add_padding = lambda s: " {} ".format(s)
    add_filler = lambda s, fill, alig ,len: "{:{}{}{}}".format(s, fill, alig, len)
    
    if title:
        title  = add_padding(title)
    else:
        title = title_filler * 2
        
    items = [substring for string in items for substring in normalize_width(string, console_width-4)]
    items= list( map (add_padding, items))
    
    
    maxlen = max(min_width_display-2, len(title), *map(len,items))
    
    title = add_filler(title, title_filler, '^', maxlen)
    items = [add_filler(item, ' ', align, maxlen) for item in items]
    line = "─" * maxlen
    
    output=""
    output += "┌{}┐\n".format(line)
    output += "│{}│\n".format(title)
    output += "├{}┤\n".format(line)
    for item in items:
        output += "│{}│\n".format(item)
    output += "└{}┘\n".format(line)
    
    return output
    
    
    
    
    

def user_pass_input(description=False, confirm = False, confirm_attempts = 2):
    username = input ("Username: ")
    password = getpass ("Password: ")
    try:
        if password:
            assert check_valid_password(password)
    except AssertionError:
        raise UserError("User did not provide a valid password.") from None
    if confirm:
        for n in range(confirm_attempts):
            if password == getpass("Confirm Password:"):
                break
            else:
                print ("Passwords don't match")
        else:
            raise UserError("User did not confirm password properly.")
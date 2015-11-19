from copy import copy
from math import log, ceil

from .exceptions import PasswordLengthError, PasswordCharacterError

minumum_accepted_lenght = 10


def transform(dict, pwd):
    k, b = password2int(pwd)
    dict = copy (dict)
    
    for key in dict:
        str = dict[key]
        l   = len(str)
        mod = 16**l
        n   = ceil(log(mod*(b-1)/k + 1, b))
        k2  = (k*(b**n-1)//(b-1)) % mod
        num = int(str, 16)
        num = num ^ k2
        
        str = hex(num).split('x',1)[1]
        str = "0"*(l - len(str))+str
        
        dict[key] = str
    
    return dict


def password2int(pwd):
    l = len(pwd)
    
    if l < minumum_accepted_lenght:
        raise PasswordLengthError(l, minumum_accepted_lenght)
    
    base=64**l
    result=0
    v=0 
    
    for char in pwd:
        try:
            v = char_value(char)
            result = 64*result + v
        except ValueError:
            raise PasswordCharacterError(char) from None
    
    return (result, base)
        

def char_value(char):
    n=ord(char)
    if n == 45 or n == 46:
        return n-45
    elif 48 <= n and n <= 57:
        return n-46
    elif 65 <= n and n <= 90:
        return n-53
    elif 97 <= n and n <= 122:
        return n-59
    else:
        raise ValueError("%s accepts only alphanumeric characters, %r or %r. Given %r" % (char_value.__name__, ".", "-", char))

from sys import stdout 
from getpass import getpass

class NonAsciiOrSpecialCodeError(Exception):
    def __init__(self, code, description):
        self.value = code
        self.description = description.format(code)
    
    def __str__(self):
        return self.description
    
getchar_proper_implementation = False


try:
    import msvcrt
    getchar_proper_implementation = True

    def ascii_catch():
        ch = msvcrt.getch ()
        special = False
        while msvcrt.kbhit():
            special = True
            special_code = msvcrt.getch()
            
        if ch == b'\x03' :
            raise KeyboardInterrupt # We want to keep this functionality
        elif special:
            raise NonAsciiOrSpecialCodeError(special_code, "Special keystroke. Code: {}")
        else:
            try:
                ch = ch.decode('ascii')
            except UnicodeDecodeError:
                raise NonAsciiOrSpecialCodeError(ch, "Keystroke was a non ascii character: {}") from None
        return ch
    
    def get_password (echo = True):
        result = ""
        while True:
            ch = getchar_ascii(echo = False)
            if ch == "\r" or ch == "\n":
                print()
                break
            elif ch == "\b":
                if result:
                    result = result[:-1]
                    if echo:
                        stdout.write("\b \b")
                        stdout.flush()
            elif 32 <= ord(ch):
                result += ch
                if echo:
                    stdout.write("*")
                    stdout.flush()
        return result
                    
# missing implementation for Linux

except ImportError:

    def ascii_catch():
        s = input()
        while not s:
            s = imput()
        ch = s[0]
        try:
            ch.encode('ascii')
        except UnicodeEncodeError:
            raise NonAsciiOrSpecialCodeError(ch, "Keystroke was a non ascii character: {}") from None
        
        return ch
    
    def get_password (echo = True): #echo has no effect whatsoever
        return getpass()
        
    


def getchar_ascii(echo = True, end = ""):
    while True:
        try:
            ch = ascii_catch()
            break
        except NonAsciiOrSpecialCodeError:
            if not getchar_proper_implementation:
                print("Must be an ASCII character:", end = " ")
    if echo:
        if ord(ch) < 32:
            stdout.write (" ") # This is for normalization
        else:
            stdout.write (ch)
        stdout.write(end)
        stdout.flush()
    return ch
    

if __name__ == "__main__":
# for testing
    getchar_ascii(True, " end")
    # print ('\u0003'.encode('ascii'))
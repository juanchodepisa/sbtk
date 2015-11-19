import sys

# Available error handling: 
#'strict'(not recommended, raises an error),
#'ignore'(not recommended, info loss),
#'replace'(recommended only when string-size matters, f.ex. table borders),
# No info loss:
#'xmlcharrefreplace',
#'backslashreplace'(preferred as it is shorter)

def shrink_to_encoding(string, encoding= 'ascii', errors = 'replace'):
    return string.encode(encoding = encoding, errors = errors).decode(encoding)
    
def make_printable(string, errors='replace'):
    encoding = sys.stdout.encoding
    return shrink_to_encoding(string, encoding=encoding, errors=errors)
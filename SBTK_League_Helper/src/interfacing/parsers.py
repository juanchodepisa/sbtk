from urllib import parse, error
import json

from .exceptions import TypeParseError, TypeUnparseError


encoding='utf-8'



###############
##  PARSING  ##
###############

def parse_application_parameters(parameters, content_type="application/x-www-form-urlencoded", method = 'POST'):
    if content_type == "application/x-www-form-urlencoded":
        return parse.urlencode(parameters).encode(encoding)
    elif content_type == "application/json":
        return json.dumps(parameters).encode(encoding)
    else:
        raise TypeParseError(content_type, method)


def parse_query_parameters(parameters):
    return parse.urlencode(parameters)
    

def parseappend_query_parameters(url, parameters):
        url_parts = (url).split('?', maxsplit=1)
        url = url_parts[0]
        
        if len(url_parts) == 2:
            query_param = url_parts[1] + "&" + parse.urlencode(parameters)
        else:
            query_param = parse.urlencode(parameters)
            
        if query_param:
            url += "?" + query_param
            
        return url
        
        
########################################################################
        

#################
##  UNPARSING  ##
#################
        
def interpret_response(raw_response):
    content_type = raw_response.getheader("Content-Type") # This seems sufficient, if it is case insensitive
    if content_type == "application/json":
        return json.loads(raw_response.read().decode(encoding))
    else:
        raise TypeUnparseError(content_type)
   

def uninterpreted_response(raw_response):
    return raw_response.read().decode(encoding)
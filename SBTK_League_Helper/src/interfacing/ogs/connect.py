from urllib import parse, request, error
import json

from src import log_entry, application_user_agent
from src.security.key_handling import retrieve_keys
from .resources import resources, full_resource_url, get_context_str
from ..exceptions import ParameterTypeError, TypeParseError, TypeUnparseError

encoding='utf-8'


def parse_form_parameters(parameters, content_type="application/x-www-form-urlencoded", method = 'POST'):
    if content_type == "application/x-www-form-urlencoded":
        return parse.urlencode(parameters).encode(encoding)
    elif content_type == "application/json":
        return json.dumps(parameters).encode(encoding)
    else:
        raise TypeParseError(content_type, method)

def _urlopen(req):
    ref = log_entry ("Sending %s request to %s...." % (req.get_method(), req._full_url))
    try:
        raw_resp = request.urlopen(req)
        log_entry (ref, "HTTP Status: {0} ({1})".format(raw_resp.status, raw_resp.reason))
    except error.HTTPError as e:
        log_entry (ref, "HTTP Status: {0} ({1})".format(e.code, e.reason))
        raise e from None
    return raw_resp
 
def interpret_response(raw_response):
    content_type = raw_response.getheader("Content-Type") # This seems sufficient, if it is case insensitive
    if content_type == "application/json":
        return json.loads(raw_response.read().decode(encoding))
    else:
        raise TypeUnparseError(content_type)
   
   
uninterpreted_response = lambda req: request.urlopen(req).read().decode(encoding)

    

class Authentication():
    def __init__(self, user, password, testing = False):
        self.is_tester = testing
        self.context_str = get_context_str("context", mode=self.__mode_str())
        self.context_short_str = get_context_str("context_short", mode=self.__mode_str())
        self.access_point = full_resource_url('access token', mode=self.__mode_str())
        self.param, self.location = retrieve_keys(user, password, context=self.context_short_str, return_location=True,)
        
        check_param = ["client_id", "client_secret", "password"]
        if not all(key in self.param for key in check_param) or len(self.param)!=len(check_param):
            raise ParameterTypeError ([key for key in self.param], check_param, location)
        
        self.param["grant_type"] = "password"
        self.param["username"]   = user
        
        ref = log_entry ("Connecting to %s...." % self.context_str)
        self.refresh_auth() #the name may seem inappropriate, but it's the same method
        log_entry (ref, "Connected!")
        
        self.param["grant_type"] = "refresh_token" #these two instructions make sure the fields are hereby updated correctly
        self.param.pop("password")
        
    def refresh_auth(self):
        data = parse_form_parameters(self.param)
        headers = {"Content-Type": "application/x-www-form-urlencoded", "User-Agent" : application_user_agent}
        req = request.Request(self.access_point, data=data, headers=headers)
        ref = log_entry ("Sending OAuth2 request to %s...." % self.context_short_str)
        raw_resp = _urlopen(req)
        response = interpret_response(raw_resp)
        
        self.access_token  = response["access_token"]
        self.refresh_token = response["refresh_token"]
        log_entry (ref, "Authenticated!")
        
        self.param["refresh_token"] = self.refresh_token
        self.bearer = {"Authorization": "Bearer %s" % self.access_token}
        self.user_agent = {"User-Agent" : application_user_agent}
        self.default_headers = dict(self.bearer, **self.user_agent)
        
    def get(self, resource, query_param = {}, headers={}, HEAD=False):
        url = full_resource_url(*resource, mode=self.__mode_str())
        
        # This ugly block allows handling query parameters coming
        # from both the resource url and the query_param argument
        url_parts = (url+"?").split('?')
        url = url_parts[0]
        qp1 = url_parts[1]
        qp2 = parse.urlencode(query_param)
        if not qp1:
            qp = qp2
        elif not qp2:
            qp = qp1
        else:
            qp = qp1+"&"+qp2
        if qp:
            url += "?" + qp
        
        req = request.Request(url, headers = dict(headers, **self.default_headers))
        raw_resp = _urlopen(req)
        response = interpret_response(raw_resp)
        
        if HEAD:
            return (response, raw_resp.info())
        else:
            return response
        
        
    def head(self, resource, headers={}):
        url = full_resource_url(*resource, mode=self.__mode_str())
        
        req = request.Request(url, headers = dict(headers, **self.user_agent))
        req.get_method = lambda : 'HEAD'
        raw_resp = _urlopen(req)
        return raw_resp.info()
        
        
    def options(self, resource, headers={}):
        url = full_resource_url(*resource, mode=self.__mode_str())
        
        req = request.Request(url, headers = dict(headers, **self.user_agent))
        req.get_method = lambda : 'OPTIONS'
        raw_resp = _urlopen(req)
        response = interpret_response(raw_resp)
        return response
        
    def __ppd_request(self, resource, app_param, headers={}, method='', content_type = "application/json"): # POST/PUT/DELETE
        url = full_resource_url(*resource, mode=self.__mode_str())
        headers = dict({"Content-Type": content_type},**dict(headers, **self.default_headers))
        data = parse_form_parameters(app_param, content_type=headers["Content-Type"], method=method)
        
        req = request.Request(url, data=data, headers=headers)
        if method:
            req.get_method = lambda : method
        raw_resp = _urlopen(req)
        response = interpret_response(raw_resp)
        return response
        
    def post(self, resource, app_param, headers={}, content_type = "application/json"):
        return self.__ppd_request(resource, app_param, headers={}, content_type = content_type)

    def put(self, resource, app_param, headers={}, content_type = "application/json"):
        return self.__ppd_request(resource, app_param, headers={}, method='PUT', content_type = content_type)

    def delete(self, resource, app_param={}, headers={}, content_type = "application/json"):
        return self.__ppd_request(resource, app_param, headers={}, method='DELETE', content_type = content_type)
        
    def __mode_str(self):
        if self.is_tester:
            return "test"
        else:
            return "main"
    
    def get_server_id(self):
        return self.context_short_str

from urllib import request as req_class, error

from src import log_entry



def raw_response(request):
    ref = log_entry ("Sending {} request to {}....".format(request.get_method(), request._full_url))
    try:
        raw_resp = req_class.urlopen(request)
        log_entry (ref, "HTTP Status: {0} ({1})".format(raw_resp.status, raw_resp.reason))
    except error.HTTPError as e:
        log_entry (ref, "HTTP Status: {0} ({1})".format(e.code, e.reason))
        raise e from None
    except error.URLError as e:
        reason = e.reason
        try:
            reason = "ERRNO {r.errno} ({r.strerror})".format(r = reason)
        except AttributeError:
            pass    
        log_entry (ref, "Not Connected: {reason}".format(reason = reason))
        raise e from None
    return raw_resp
    
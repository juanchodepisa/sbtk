from src.tools.strings import make_printable
from time import perf_counter, sleep

"""
This module should be accomodated to use the logging built-in module.

Calls to log_entry should be replaced by logging calls on later versions
"""



log_entries = 0

def log_entry(*args):
    # For now, just printing (and dumbed down for CMD, just in case)
    global log_entries
    log_entries += 1
    old_print("%d: @%d" % (log_entries, 1000*perf_counter()), end=" ")
    s_ref = "[%d]" % log_entries
    
    args = [make_printable(str(arg), errors='backslashreplace') for arg in args]
    
    print (*args)
            
    return s_ref

def waiting (n):
    global log_entries
    t = n/4
    log_entries += 1
    old_print("%d: @%d" % (log_entries, 1000*perf_counter()), end=" ")
    old_print ("Waiting", end = "")
    for i in range (4):
        old_print(".", end = "")
        sleep(t)
    old_print()
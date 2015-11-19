from src.tools.strings import make_printable
from time import perf_counter, sleep

log_entries = 0

old_print = print

def log_entry(*args):
    # For now, just printing (and dumbed down for CMD, just in case)
    global log_entries
    log_entries += 1
    old_print("%d: @%d" % (log_entries, 1000*perf_counter()), end=" ")
    s_ref = "[%d]" % log_entries
    try:
        old_print(*args)
    except UnicodeEncodeError:
        for elem in args[:-1]:
            try:
                old_print(elem, end=" ")
            except UnicodeEncodeError:
                for char in str(elem):
                    try:
                        old_print(char, end="")
                    except UnicodeEncodeError:
                        old_print("?", end="")
        elem = args[-1]
        try:
            old_print(elem)
        except UnicodeEncodeError:
            for char in str(elem):
                try:
                    old_print(char, end="")
                except UnicodeEncodeError:
                    old_print("?", end="")
            old_print()
            
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
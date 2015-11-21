from urllib.parse import quote
import json
import os

from src import log_entry
from .obfuscation import transform
from .exceptions import KeysDirectoryNotFound, KeysFileNotFound


user_index = os.path.join(os.path.dirname(__file__), "keys_loc.json")
default_context = "OGS"
obfuscated = "_obfuscated_"
plaintext = "_plaintext_"
no_directory_default = lambda usr: ""

def reset_index():
    with open (user_index, 'w') as f:
        json.dump({}, f)
        log_entry (user_index, "file reset to empty value.")

if not os.path.isfile(user_index):
    log_entry (user_index, "file does not exist.")
    __ref = log_entry ("Creating file %s...." % user_index)
    reset_index()
    log_entry(__ref, "File created. Ready!")
    del __ref
else:
    log_entry (user_index, "file exists. Ready!")


def get_keys_directory(user, on_fail = no_directory_default):
    with open(user_index, 'r+') as f:
        index_data = json.load(f)
        update =  False
        ref = log_entry("Searching %s's keys location from %s...." % (user, user_index))
        
        if user in index_data:
            dir = index_data[user]
        else:
            log_entry(ref, "Location not found.")
            dir = False
        
        if not (dir and os.path.isdir(dir)):
            if dir:
                log_entry (ref, "Location invalid.")
                index_data.pop(user)
                update = True
            
            ref = log_entry("Getting %s's keys location from backup method...." % user)
            dir = on_fail(user)
            
            try:
                if os.path.isdir(dir):
                    index_data[user] = dir
                    update = True
                else:
                    log_entry(ref, "Location not found or invalid.")
                    raise KeysDirectoryNotFound(user)
            finally:
                if update:
                    ref = log_entry ("Updating %s...." % user_index)
                    f.seek(0)
                    json.dump(index_data, f)
                    f.truncate()
                    log_entry (ref, "Updated!")
    
    log_entry (ref, "Location found!")
    return dir

def set_keys_directory(user, directory):
    with open(user_index, 'r+') as f:
        ref = log_entry ("Updating %s's keys location at %s...." % (user, user_index))
        index_data = json.load(f)
        index_data[user] = directory
        f.seek(0)
        json.dump(index_data, f)
        f.truncate()
        log_entry (ref, "Updated!")


def remove_keys_directory(user):
    with open(user_index, 'r+') as f:
        ref = log_entry ("Removing %s's keys location at %s...." % (user, user_index))
        index_data = json.load(f)
        index_data.pop(user)
        f.seek(0)
        json.dump(index_data, f)
        f.truncate()
        log_entry (ref, "Removed!")

def store_keys (user, keys, password="", context=default_context, if_no_directory = no_directory_default):
    directory = get_keys_directory(user, if_no_directory)
    
    if password:
        ref = log_entry ("Encrypting %s's keys...." % user)
        keys = transform(keys, password)
        log_entry (ref, "Encrypted!")
    else:
        log_entry ("WARNING: No password provided to encrypt %s's keys. This is unsafe, as keys will be stored in plain text." % user)
        
    filename = standard_filename(user, password, directory, context)
    with open(filename, 'w') as f:
        ref = log_entry("Storing %s's keys at %s...." % (user, filename))
        json.dump(keys, f)
        log_entry(ref, "Stored!")


def retrieve_keys (user, password="", context=default_context, return_location=False):
    directory = get_keys_directory(user)
    
    filename = standard_filename(user, password, directory, context)
    if os.path.isfile(filename):
        with open(filename, 'r') as f:
            ref = log_entry("Retrieving %s's keys from %s...." % (user, filename))
            keys = json.load(f)
            log_entry(ref, "Retrieved!")
    else:
        raise KeysFileNotFound(user, filename)
    
    if password:
        ref = log_entry ("Decrypting %s's keys...." % user)
        keys = transform(keys, password)
        log_entry (ref, "Decrypted!")
    
    if return_location:
        return (keys, filename)
    else:
        return keys


def standard_filename(user, password, directory, context):
    filename = context+(obfuscated if password else plaintext)+quote(user, safe='')+".json"
    return os.path.join(directory, filename)
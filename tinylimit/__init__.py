# encoding: utf-8
__author__ = 'jamesqin'

import os
import json
import time
import logging
import functools
import hashlib

def GenKey(method_name, args, kw):
    key_str = 'CallRateLimit@@' + method_name + "("
    for arg in args:
        if str(type(arg)) == "<type 'instance'>" or ' object at 0x' in str(arg):
            key_str = "{}&class={}".format(key_str, arg.__class__)
            for name,val in vars(arg).items():
                key_str = "{}&self.{}={}".format(key_str, name, val)
        else:
            key_str = "{}&{}={}".format(key_str, str(type(arg)), arg)
    for (k,v) in kw.items():
        key_str = "{}&{}={}".format(key_str, k, v)
    key_str += ")"
    key = hashlib.md5(key_str.encode('utf8')).hexdigest()
    return (key, key_str)


def AntiLimit(limit=1, every=10, cache_dir='cache/'):
    if cache_dir[-1] != '/':
        cache_dir = cache_dir + '/'
    is_exists = os.path.exists(cache_dir)
    if not is_exists:
        os.makedirs(cache_dir) 
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            (key,key_str) = GenKey(func.__name__, args, {})
            file_name = cache_dir + key

            try:
                with open(file_name, 'r') as f:
                    cache = json.load(f)
            except IOError as err:
                logging.info("open cache file failed, file={}, error msg={}".format(file_name, err))
                cache = {}
            except ValueError as err:
                logging.info("cache file is not json format, file={}, error msg={}".format(file_name, err))
                cache = {}

            now = time.time()
            if 'expired_at' not in cache or cache['expired_at'] < now:
                cache['created_at'] = now
                cache['expired_at'] = now + every
                cache['request_cnt'] = 1
                cache['value'] = func(*args, **kw)
                logging.info("No limit, finger={}, request_cnt={}".format(key_str,cache['request_cnt']))
            elif 'request_cnt' not in cache or int(cache['request_cnt'])<limit:
                cache['request_cnt'] = int(cache['request_cnt']) + 1
                cache['value'] = func(*args, **kw)
                logging.info("No limit, finger={}, request_cnt={}".format(key_str,cache['request_cnt']))
            else:
                cache['request_cnt'] = int(cache['request_cnt']) + 1
                logging.info("    limit, finger={}, request_cnt={}".format(key_str,cache['request_cnt']))
            cache['key_str'] = key_str
            cache['key'] = key
            try:
                with open(file_name, 'w') as f:
                    json.dump(cache, f, indent=4, default=str)
            except IOError as err:
                logging.info("update cache file failed, file={}, error msg={}".format(file_name, err))
            return cache['value']
        return wrapper
    return decorator


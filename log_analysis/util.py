import os
import datetime
import cPickle
import itertools

def round_by(num):
    '''
    round a number by num
    >>> round_by_5 = round_by(5)
    >>> round_by_5(0), round_by_5(3), round_by_5(5), round_by_5(10)
    (0, 0, 5, 10)
    '''
    if num <= 0:
        raise ValueError("num is not a positive number")
    def inner(a):
        return (a / num) * num
    return inner

def round_minutes_by(period):
    ''' round minutes
    '''
    round_by_n = round_by(period)
    def inner(date):
        return datetime.datetime(date.year, date.month, date.day, date.hour,
                                 round_by_n(date.minute))
    return inner

def upsert(dict1, dict2):
    '''
    If a key from dict2 is not present in dict1, insert it, else add the value
    '''
    for key in dict2.keys():
        if dict1.get(key):
            dict1[key] += dict2[key]
        else:
            dict1[key] = dict2[key]

def ensure_directory(directory):
    '''
    Ensuring the existance of the directory. If the directory is not exist,
    create it
    '''
    def _ensure_directory(func):
        def inner(*args, **argkw):
            if not os.path.exists(directory):
                os.makedirs(directory)
            return func(*args, **argkw)
        return inner
    return _ensure_directory

def load_and_delete(full_path):
    '''
    Load the pickle file and delete it
    '''
    result = cPickle.load(open(full_path))
    os.remove(full_path)
    return result

def listdir(path):
    '''
    List dir with path as prefix
    '''
    return map(lambda f: os.path.join(path, f), os.listdir(path))

def split_every(num, iterable):
    '''
    Splits a list into length-num pieces.  The last piece will be shorter if n
    does not evenly divide the length of the list.
    '''
    it = iter(iterable)
    while True:
        n_items = list(itertools.islice(it, num))
        if not n_items:
            break
        yield n_items

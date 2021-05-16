import datetime
import pandas as pd
import statistics

def dictionary_test():
    a = (1, 'a')
    b = (2, 'b')
    c = (1, 'c')
    array = [a, b, c]
    dictionary = {}
    for letter in array:
        dictionary_keys = dictionary.keys()
        print(dictionary_keys)
        if letter[0] not in dictionary_keys:
            dict_update = {letter[0]: letter[1]}
            dictionary.update(dict_update)
        else:
            addon = dictionary[letter[0]]+letter[1]
            dictionary[letter[0]] = addon


def datetime_test():
    a = datetime.datetime.now()
    b = datetime.datetime.combine(datetime.date(2021, 4, 12), datetime.time(12, 30, 42))
    c = datetime.datetime.combine(datetime.date(2021, 4, 28), datetime.time(17, 24, 47))
    d = a - b
    e = a - c
    f = c - b
    g = (d+e)/2

    return((d, e, g))


def new_dict():
    a = {}
    a['b'] = {'c': 'd'}
    return a


a = datetime.timedelta(days=3, hours=15, minutes=0, seconds=34)
b = datetime.timedelta(days=1, hours=20, minutes=10, seconds=00)
c = datetime.timedelta(days=2, hours=11, minutes=25, seconds=15)
d = datetime.timedelta(days=2, hours=9, minutes=33, seconds=43)
e = datetime.timedelta(days=2, hours=4, minutes=42, seconds=23)
f = datetime.timedelta(days=3, hours=18, minutes=12, seconds=43)
g = datetime.timedelta(days=2, hours=13, minutes=56, seconds=12)
h = datetime.timedelta(days=3, hours=4, minutes=16, seconds=25)
i = datetime.timedelta(days=4, hours=2, minutes=29, seconds=39)
w = datetime.timedelta(days=0, hours=3, minutes=19, seconds=35)
array = sorted([a, b, c, d, e, f, g, h, i, w])
unsorted = [a, b, c, d, e, f, g, h, i, w]
DF = pd.DataFrame({'Timedelta': pd.to_timedelta(array)})
print(DF['Timedelta'].median())
print(statistics.median(array))
print(statistics.median(unsorted))
j = datetime.timedelta(days=0, hours=0, minutes=0, seconds=36)
k = datetime.timedelta(days=0, hours=0, minutes=47, seconds=11)
DF2 = pd.DataFrame({'Times': pd.to_timedelta([j, k])})
DF3 = pd.DataFrame({'Time': pd.to_timedelta(['0 days 00:00:36',
                                             '0 days 00:47:11'])})
print(DF2['Times'].median())
print(DF3['Time'].median())
print(statistics.median([j, k]))
print(j)
print(k)

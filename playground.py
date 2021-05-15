import datetime

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


d = [1, 2, 3, 0]
print(len(d))
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
print(dictionary)
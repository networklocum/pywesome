import json as python_json 
from random import randint
from types import LambdaType
from copy import copy

'''
Basic functions for functional programming with lists,
map, reduce, search, contains, ...
'''


def map(collection, function):
    mapped_collection = []
    for item in collection:
        mapped_collection.append(function(item))
    return mapped_collection


def reduce(collection, function, carry=None):
    collection = copy(collection)
    if carry is None:
        carry = collection[0]
        collection.pop(0)
    for item in collection:
        carry = function(carry, item)
    return carry


def filter(collection, function):
    filtered_collection = []
    for item in collection:
        if function(item):
            filtered_collection.append(item)
    return filtered_collection


def reject(collection, function):
    filtered_collection = []
    for item in collection:
        if not function(item):
            filtered_collection.append(item)
    return filtered_collection


def contains(haystack, needle):
    if isinstance(needle, LambdaType):
        for item in haystack:
            if needle(item):
                return True
        return False
    return needle in haystack


def search(haystack, needle):
    for index, item in enumerate(haystack):
        if item == needle or (isinstance(needle, LambdaType) and needle(item)):
            return index
    return False


def random(collection, offset=1):
    indexes = []
    results = []
    for i in range(offset):
        index = random_number(0, len(collection) - 1, indexes)
        results.append(collection[index]) 
    return results[0] if len(results) == 1 else results


# Must be a dict collection
def only(collection, prop):
    return map(collection, lambda o: o[prop])


def chunk(collection, size):
    size = max(1, size)
    return [collection[item:item + size] for item in range(0, len(collection), size)]


def merge(*args):
    collection = args[0]
    for col in args[1:]:
        for item in col:
            collection.append(item)
    return collection


def collapse(collections):
    return reduce(collections, lambda g, c: merge(g, c))


def sort(collection, desc=False):
    return sorted(copy(collection), reverse=desc)


def sort_by(collection, prop, desc=False):
    return sorted(copy(collection), key=lambda d: d[prop], reverse=desc)

def where(collection, prop, value):
    return filter(collection, lambda el: el[prop] == value)

def where_in(collection, prop, values):
    return filter(collection, lambda el: el[prop] >= values[0] and el[prop] <= values[1])



'''
These methods can seem a bit overkilled or not pythonic
But they are useful for consistency when using the class wrapper
They are defined here for consistency in the library
'''


def first(collection):
    return collection[0]


def last(collection):
    return collection[-1]


def get(collection, key):
    return collection[key]

'''
Functions running operations on the list (avg, sum,...)
'''


def sum(collection, prop=None):
    if not prop:
        return reduce(collection, lambda c, n: c + n )
    return sum(only(collection, prop))


def avg(collection, prop=None):
    return sum(collection, prop) / len(collection)


def group_by(collection,
             key,
             key_is_unique=False,
             key_transformation_function=lambda a: a,
             value_transformation_function=lambda a: a,
             value_list_transformation_function=None,
             get_method=getattr):
        '''
        :param key: the key to group entities in the collection by
        :param key_is_unique: whether or not the key is unique. If False, the
        returning dictionary will contain lists of entities instead of entities
        :param key_transformation_function: a method used to transform the input
        keys to be used in the dictionary. Default is to just use the key.
        :param value_transformation_function: function to transform each value,
        default is not to transform
        :param value_list_transformation_function: function to transform each
        list in the dictionary values, default is to collect them
        :param get_method: the method used to retrieve the field from the item
        in the collection via a key
        :return: A dictionary containing the entities grouped by a key that
         is a field on the entities. If the field isn't found, the key, None, is
         used. The field must exist if unique_key=True
        '''

        if key_is_unique:
            return {key_transformation_function(get_method(e, key)):
                        value_transformation_function(e)
                    for e in collection}

        if value_list_transformation_function is None:
            # Use the collect method of the collection if it exists. Otherwise
            # leave the list as a list.
            value_list_transformation_function = getattr(
                collection, 'collect', lambda a: a
            )

        key_values = set([key_transformation_function(get_method(e, key, None)) 
                          for e in collection])
        grouped_dict = {k: [] for k in key_values}
        for entity in collection:
            new_key = key_transformation_function(get_method(entity, key, None))
            grouped_dict[new_key].append(
                value_transformation_function(entity)
            )
        for dict_key in grouped_dict:
            grouped_dict[dict_key] = value_list_transformation_function(
                grouped_dict[dict_key]
            )
        return grouped_dict

'''
Formatting functions
'''


def join(collection, char=','):
    return char.join(
        map(collection, lambda e: str(e))
    )


def json(collection):
    return python_json.dumps(collection)

'''
Helpers (not related to collections)
Could be moved elsewhere at some point
'''


def random_number(start, end, rejects=[]):
    index = randint(start, end)
    if index in rejects:
        return random_number(start, end, rejects)
    return index

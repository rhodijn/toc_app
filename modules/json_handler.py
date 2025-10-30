#!/usr/bin/env python3

#   ###################
#   ##                 ##
#   ##               ##
#     ######       ##
#       ##       ######
#     ##               ##
#   ##                 ##
#     ###################


import json


def get_value(file: str, k_1: str, k_2: str) -> str:
    """
    get a specific value from a json-file

    parameters:
    file: str = file name
    k_1: str = key 1
    k_2: str = key 2

    returns:
    str or None
    """
    try:
        with open(file) as f:
            data = json.load(f)
            return data[k_1][k_2]
    except:
        return None


def load_json(filename: str, p: str) -> dict:
    """
    load data from a json-file

    parameters:
    filename: str = library code
    p: str = code for the file location

    returns:
    dict = data from the json-file
    """
    path = get_value('data/config.json', 'path', p)

    if path:
        try:
            with open(path + filename, mode='r', encoding='utf-8') as f:
                data = json.load(f)
                return data
        except:
            return {}
    else:
        return {}


def write_json(data: dict, filename: str, p: str) -> bool:
    """
    write data to a json-file

    parameters:
    data: dict = data to be saved
    file name: str = name of the file to save data to
    p: str = code for the file location

    returns:
    success: bool = success saving data
    """
    path = get_value('data/config.json', 'path', p)

    if path:
        with open(path + filename, mode='w', encoding='utf-8') as f:
            f.seek(0)
            json.dump(data, f, indent=4)
        return True
    else:
        return False
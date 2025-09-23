#!/usr/bin/env python3


#   ###################
#   ##                 ##
#   ##               ##
#     ######       ##
#       ##       ######
#     ##               ##
#   ##                 ##
#     ###################


import os, requests
from dotenv import dotenv_values


secrets = dotenv_values('.env')


def api_request(method: str, value: str, frmt: str, par_1: str, par_2='') -> tuple:
    """
    perform an api request and return the answer

    parameters:
    method: str = api request method (GET, PUT, POST, ...)
    value: str = item id
    frmt: str = format (json, xml)
    param_1: str = api parameter 1
    param_2: str = api parameter 2

    returns:
    tuple = (req: str, response: requests.models.Response)
    """
    config = load_json('config.json', 'd')
    response = False

    if method == 'get':

        if frmt == 'j':
            req = f"{secrets['API_URL']}{par_1}{value}{par_2}&apikey={secrets['API_KEY']}&format={config['api']['j']}"
        elif frmt == 'x':
            req = f"{secrets['API_URL']}{par_1}{value}{par_2}&apikey={secrets['API_KEY']}&format={config['api']['x']}"
        response = requests.get(req)
    elif method == 'put':
        req = f"{secrets['API_URL']}{par_1}{value}{par_2}&apikey={secrets['API_KEY']}"
        filename = os.listdir('xml/')

        if filename:
            response = requests.put(req, headers=config['api']['header'], data=etree.tostring(etree.parse(f"xml/{filename[0]}")))
            # delete the enriched marc-xml file from the local drive
            # os.remove(f"xml/{filename[0]}")

    return req, response


def check_url(processing: dict) -> dict:
    """
    test the link to the pdf

    parameters:
    processing: dict = logging info of the currently processed record

    returns:
    processing: dict = logging info of the currently processed record
    """
    try:
        if processing['url']:
            response = requests.head(processing['url'])

            if response.status_code == 200:
                processing.update({'link_tested': True})
                processing['messages'].append(f"link tested (code: {response.status_code})")
            else:
                processing['messages'].append(f"link test failed (code: {response.status_code})")
        else:
            processing['messages'].append('no url to test')
    except requests.ConnectionError as e:
        processing['messages'].append(f"error: {e} occurred")

    return processing
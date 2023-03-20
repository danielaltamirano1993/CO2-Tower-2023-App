#run: ctrl + shift + B in Atom-IDE


import json
import requests

def get_carbon_intensity():
    print ("loop")
    requestUrl = 'https://api.co2signal.com/v1/latest?countryCode=DK-DK1'
    headers = {'auth-token': 'TOKEN'}
    response = requests.get(requestUrl, headers=headers)
    dataObject = response.json()
    if not isinstance(dataObject, dict) and "data" not in dataObject:
        return 0
    if "carbonIntensity" not in dataObject['data']:
        return 0
    try:
        float(dataObject['data']['carbonIntensity'])
    except ValueError:
        return 0
    return dataObject['data']['carbonIntensity']


co2_level = get_carbon_intensity()
print (co2_level)

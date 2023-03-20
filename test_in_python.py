#run: ctrl + shift + B in Atom-IDE


import json
import requests

def get_carbon_intensity():
    print ("loop")
    requestUrl = 'https://api.co2signal.com/v1/latest?countryCode=DK-DK1'
    headers = {'auth-token': 'TOKEN'}
    response = requests.get(requestUrl, headers=headers)
    dataObject = response.json()


co2_level = get_carbon_intensity()
print (co2_level)

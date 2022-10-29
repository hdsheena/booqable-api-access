
import requests
import dateutil.parser
import datetime
import csv
import yaml
from pathlib import Path


def get_settings():
    full_file_path = Path(__file__).parent.joinpath('settings.yaml')
    with open(full_file_path) as settings:
        settings_data = yaml.load(settings, Loader=yaml.Loader)
    return settings_data
settings_data = get_settings()
token = settings_data["token"]
urlbase = settings_data["urlbase"]

def get_items(itemType):
    url = "https://"+urlbase+".booqable.com/api/boomerang/"+itemType
    pagesize = "?page[size]=100"

    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9,en-GB;q=0.8",
        "content-type": "application/json",
       "authorization": "Bearer "+token
      }

    data = {
      "filters": [
      ]
    }


    # print("doing request next")
    # print(url+payload, headers)
    after = ""
    #url = "https://interior-trial.booqable.com/api/boomerang/product_groups/4ad65217-e5e0-4d17-bcde-083e516dba2b"
    response = requests.request("GET", url+pagesize, headers=headers)
    print(response.content)
    print(response.headers)
    data = response.json()["data"]
    return data

def delete_items(data):
    for i in data:
        #print(i['id'])
        deleteurl = url+"/"+i['id']
        #print(deleteurl)
        response1 = requests.request("DELETE", deleteurl, headers=headers)
        print(response1.content)
        
data = get_items("product_groups")
data = get_items("products")
for i in data:
    print(i)
#delete_items(data)


    


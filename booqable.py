
import requests
import dateutil.parser
import datetime
import csv
import yaml
from pathlib import Path


sampleResultProductGroup = {
            'created_at': '2022-11-03T20:29:36+00:00', 
            'updated_at': '2022-11-03T20:30:44+00:00', 
            'archived': False, 
            'archived_at': None, 
            'type': 'product_groups', 
            'name': 'test multi variation bulk', 
            'slug': 'test-multi-variation-bulk', 
            'sku': 'TEST_MULTI_VARIATION_BULK', 
            'lead_time': 0, 
            'lag_time': 0, 
            'product_type': 'rental', 
            'tracking_type': 'bulk', 
            'trackable': False, 
            'has_variations': True, 
            'extra_information': None, 
            'photo_url': 'https://cdn3.booqable.com/uploads/368b6a9911f438f5c97e26e330c43d10/photo/photo/201d5def-461e-4a67-8199-6429c39d7b86/large_photo.jpg', 
            'description': None, 
            'show_in_store': True, 
            'sorting_weight': 0, 
            'base_price_in_cents': 5000, 
            'price_type': 'simple', 
            'price_period': 'day', 
            'deposit_in_cents': 0, 
            'discountable': True, 
            'taxable': True, 
            'tag_list': [], 
            'properties': {}, 
            'photo_id': '201d5def-461e-4a67-8199-6429c39d7b86', 
            'tax_category_id': None, 
            'price_ruleset_id': None, 
            'price_structure_id': None, 
            'allow_shortage': False, 
            'shortage_limit': 0, 
            'variation_fields': ['length', 'diameter', 'colour'], 
            'flat_fee_price_in_cents': 5000, 
            'structure_price_in_cents': 0, 
            'stock_item_properties': []
        }

sampleResultProduct = {
            'type': 'products', 
            'name': 'test multi variation bulk - 2 feet, 2", blue', 
            'lead_time': 0, 
            'lag_time': 0, 
            'product_type': 'rental', 
            'tracking_type': 'bulk', 
            'trackable': False, 
            'extra_information': None, 
            'photo_url': 'https://cdn3.booqable.com/uploads/368b6a9911f438f5c97e26e330c43d10/photo/photo/201d5def-461e-4a67-8199-6429c39d7b86/large_photo.jpg', 
            'description': None, 
            'show_in_store': True, 
            'sorting_weight': 1, 
            'base_price_in_cents': 5000, 
            'price_type': 'simple', 
            'price_period': 'day', 
            'deposit_in_cents': 0, 
            'discountable': True, 
            'taxable': True, 
            'tag_list': [], 
            'properties': {}, 
            'tax_category_id': None, 
            'price_ruleset_id': None, 
            'price_structure_id': None, 
            'variation_values': ['2 feet', '2"', 'blue'], 
            'allow_shortage': False, 
            'shortage_limit': 0, 
            'product_group_id': '0bdedbf4-5a35-45d7-9086-2c9311323d4d'
        }
samplePostProduct = {'data': {
            'type': 'products', 
            'attributes': {
            'sku':'TEST_MULTI_VARIATION_BULK',
            'has_variations':False,
            'remote_photo_url': 'https://cdn3.booqable.com/uploads/368b6a9911f438f5c97e26e330c43d10/photo/photo/201d5def-461e-4a67-8199-6429c39d7b86/large_photo.jpg',
            'sorting_weight': 1, 
            'base_price_in_cents': 5000, 
            'deposit_in_cents': 0,
            'variation_values': ['2 feet', '2"', 'blue'], 
            'confim_shortage': False,
            'product_group_id': '0bdedbf4-5a35-45d7-9086-2c9311323d4d'
            }
        }
        }
minimalSamplePostProduct1 = {
            'data': {
                'type': 'products', 
                'attributes': {
                    'variation_values': ['2 feet', '1"', 'blue'], 
                    'product_group_id': '0bdedbf4-5a35-45d7-9086-2c9311323d4d'
                }
            }
        }
minimalSamplePostProduct = {
    'data': {
        'type': 'products', 
        'attributes': {
            'variation_values': ['4 feet'], 
            'product_group_id': '85f4ffe2-e1a9-4314-b808-c7d178c78e27'
        }
    }
}

def get_settings():
    full_file_path = Path(__file__).parent.joinpath('settings.yaml')
    with open(full_file_path) as settings:
        settings_data = yaml.load(settings, Loader=yaml.Loader)
    return settings_data
settings_data = get_settings()
token = settings_data["token"]
urlbase = settings_data["urlbase"]
headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9,en-GB;q=0.8",
        "content-type": "application/json",
       "authorization": "Bearer "+token
      }
def get_items(itemType):
    url = "https://"+urlbase+".booqable.com/api/boomerang/"+itemType
    pagesize = "?page[size]=100"

   

    data = {
      "filters": [
      ]
    }


    # print("doing request next")
    # print(url+payload, headers)
    after = ""
    #url = "https://interior-trial.booqable.com/api/boomerang/product_groups/4ad65217-e5e0-4d17-bcde-083e516dba2b"
    response = requests.request("GET", url+pagesize, headers=headers)
    #print(response.content)
    #print(response.headers)
    data = response.json()["data"]
    return data, url

def delete_items(itemType,data):
    for i in data:
        #print(i['id'])
        url = "https://"+urlbase+".booqable.com/api/boomerang/"+itemType
        deleteurl = url+"/"+i['id']
        #print(deleteurl)
        response1 = requests.request("DELETE", deleteurl, headers=headers)
        print(response1.content)

def get_products_from_all_groups():
    itemGetter = get_items("product_groups")
    data = itemGetter[0]
    url = itemGetter[1]
    #data = get_items("products")
    for i in data:
        #print(i)
        print("-----")
        print(i["attributes"]["type"],":",i["attributes"]["name"])
        #print(i["attributes"]["type"])
        #for key in i["attributes"].keys():
        #    print(key, i["attributes"][key])
        print("****")
        queryString = "?filter[product_group_id][eq]="+i['id']
        #print(queryString)
        productsInGroup = requests.request("GET", "https://"+urlbase+".booqable.com/api/boomerang/"+"products"+queryString, headers=headers)
        #print(productsInGroup.content)
        for i in productsInGroup.json()["data"]:
            print(i["attributes"]["type"],":",i["attributes"]["name"])



def deleteAllLocations():
    data = get_items("locations")
    for i in data:
        print(i)
    delete_items("locations",data)
        
def create_items(itemType,items):
    url = "https://"+urlbase+".booqable.com/api/boomerang/"+itemType
    for i in items:
        data = i
        print(data)
        response = requests.request("POST", url, headers=headers, data=data)
        print(response)
        print(response.content)
create_items("products",[minimalSamplePostProduct])




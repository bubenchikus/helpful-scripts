from pymongo import MongoClient
import requests
import os
from dotenv import load_dotenv
load_dotenv()


def get_pages_by_type(type, page_number):
    return requests.get("https://api.nal.usda.gov/fdc/v1/foods/list",
                        headers={"x-api-key": os.getenv('API_KEY')},
                        params={'pageSize': 200, 'dataType': type, 'pageNumber': page_number
                                }).json()


def trim_useless_fields(product):
    trimmed_product = {}
    for key in product.keys():
        if key == 'foodNutrients':
            trimmed_product[key] = {}
            for nutrient in product[key]:
                if nutrient['name'] in ['Carbohydrate, by difference', 'Protein', 'Total lipid (fat)', 'Energy', 'Energy (Atwater General Factors)', 'Energy (Atwater Specific Factors)',  'Fiber, total dietary']:
                    trimmed_product[key][nutrient['name']
                                         ] = nutrient['amount']
        elif key in ['description', 'dataType']:
            trimmed_product[key] = product[key]
    if 'Energy (Atwater General Factors)' in trimmed_product['foodNutrients'].keys() and 'Energy (Atwater Specific Factors)' in trimmed_product['foodNutrients'].keys():
        trimmed_product['foodNutrients'].pop(
            'Energy (Atwater General Factors)')
    return trimmed_product


def get_all_data_by_type(type, collection):
    page_number = 1
    while True:  # do-while emulation
        res = get_pages_by_type(type, page_number)
        if len(res) < 1 or page_number > 1:
            break
        for product in res:
            product = trim_useless_fields(product)
            if len(product['foodNutrients']) > 0:
                collection.insert_one(product)

        page_number += 1


if __name__ == '__main__':
    client = MongoClient('localhost', 27017)
    database = client.nutrition
    collection = database.nutrition

    get_all_data_by_type("Foundation", collection)
    # get_all_data_by_type("Branded", collection)
    # get_all_data_by_type("Survey (FNDDS)", collection)
    # get_all_data_by_type("SR Legacy", collection)

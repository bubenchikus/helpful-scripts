from pymongo import MongoClient
import requests
import os
import argparse
from dotenv import load_dotenv
load_dotenv()


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--types', '-t', nargs='+',
                        type=str, default=["Foundation"])

    return vars(parser.parse_args())


def get_pages_by_type(type, page_number):
    print(f"Requesting page #{page_number}...")
    result = requests.get("https://api.nal.usda.gov/fdc/v1/foods/list",
                          headers={"x-api-key": os.getenv('API_KEY')},
                          params={'pageSize': 200, 'dataType': type, 'pageNumber': page_number
                                  })
    if result.status_code == 200:
        return result.json()


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

    # 'Energy (Atwater Specific Factors)' is more preferred, remove 'Energy (Atwater General Factors)' if both exist
    if 'Energy (Atwater General Factors)' in trimmed_product['foodNutrients'].keys() and 'Energy (Atwater Specific Factors)' in trimmed_product['foodNutrients'].keys():
        trimmed_product['foodNutrients'].pop(
            'Energy (Atwater General Factors)')

    return trimmed_product


def get_all_data_by_type(type, collection):
    print(f"----Getting {type} data...----")
    current_page = 1
    while True:  # do-while emulation
        res = get_pages_by_type(type, current_page)

        if not res or len(res) < 1:
            break
        for product in res:
            product = trim_useless_fields(product)
            if len(product['foodNutrients']) > 0:
                collection.insert_one(product)

        current_page += 1
    print(f"Finished!\n")


if __name__ == '__main__':
    args = parse_args()

    client = MongoClient('localhost', 27017)
    database = client.nutrition
    collection = database.nutrition

    # type variants: "Foundation", "Branded", "Survey (FNDDS)", "SR Legacy"
    for type in args['types']:
        get_all_data_by_type(type, collection)

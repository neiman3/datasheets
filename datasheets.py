import os.path
import json
import requests
import time
from text_manipulation import clean_text, remove_ufeff


def unshorten_url(url):
    try:
        return requests.head(url, allow_redirects=True).url
    except requests.exceptions.MissingSchema:
        return url

def get_part_numbers_from_csv(filename):
    if os.path.exists(filename):
        f = open(filename, 'r')
        res = []
        for line in f:
            line = remove_ufeff(line)
            if len(line) > 0:
                if line[0] != '#':
                    res.append(line)
        f.close()
        return res
    else:
        return None

# def query(part_number):
#     query_text = """query {
#     characters {
#     results {
#     name
#     status
#     species
#     type
#     gender
#     }
#     }
#     }"""
#     url = 'https://rickandmortyapi.com/graphql/'
#     r = requests.post(url, json={'query': query_text})
#     time.sleep(1)
#     response = json.loads(r.text)
#     return response

def query(client, part):
    base_query = '''
    query test($mpn: String!) {
        supSearchMpn(
            q: $mpn
            limit: 1
        ) {
            results{
                part {
                    mpn
                    genericMpn
                    category {
                        name
                    }
                    manufacturer {
                        name
                    }
                    bestDatasheet {
                        url
                    }
                    shortDescription
                }
            }
        }
    }
    '''

    result = client.get_query(base_query, {'mpn': part})
    return result

def clean_result(dirty_result, part):
    result: dict
    if dirty_result['supSearchMpn']['results'] is None:
        result = {
            'mpn': part,
            'genericMpn': part,
            'category': None,
            'name': 'NONE',
            'manufacturer': None,
            'bestDatasheet': None,
            'shortDescription': "NO DESCRIPTION"
        }
    else:
        result = dirty_result['supSearchMpn']['results'][0]['part']
    if result['category'] is None:
        result['category'] = 'UNCATEGORIZED'
    else:
        result['category'] = result['category']['name']
    if result['manufacturer'] is None:
        result['manufacturer'] = 'NO MFG'
    else:
        result['manufacturer'] = result['manufacturer']['name']
    if result['bestDatasheet'] is None:
        result['url'] = 'NO DATASHEET'
    else:
        result['url'] = result['bestDatasheet']['url']
    result.pop('bestDatasheet')
    result['mpn'] = part
    return result

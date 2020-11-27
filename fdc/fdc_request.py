import requests
from fdc import secrets
import json

CACHE_FILENAME = 'fdc_cache.json'
CACHE = {}


def save_cache(cache_dict):
    ''' Saves the current state of the cache to disk

    Parameters
    ----------
    cache_dict: dict
        The dictionary to save

    Returns
    -------
    None
    '''
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(CACHE_FILENAME, "w")
    fw.write(dumped_json_cache)
    fw.close()


def open_cache():
    ''' Opens the cache file if it exists and loads the JSON into
    the CACHE_DICT dictionary. If the cache file doesn't exist,
    creates a new cache dictionary

    Parameters
    ----------
    None

    Returns
    -------
    The opened cache: dict
    '''
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict

BASE = 'https://api.nal.usda.gov/fdc/v1/foods/search'

''' query=cheddar%20cheese
    &dataType=Foundation,SR%20Legacy
    &pageSize=25
    &sortBy=description
    &sortOrder=asc
    &brandOwner=Kar%20Nut%20Products%20Company
'''

def search(search_term):
  ''' Searches the FDC database by term and get list of foods
  Parameters
  ----------
  search_term: string
      term to search in the FDC database

  Returns
  -------
  object
      FDC Response Object containing list of foods
  '''
  RESPNSE_CACHE = open_cache()

  if search_term in RESPNSE_CACHE:
    print('Using Cache for: ', search_term)
  else:
    print('Fetching for: ', search_term)
    RESPNSE_CACHE[search_term] = requests.get(f'{BASE}?query={search_term}&api_key={secrets.FDC_API}').json()
    save_cache(RESPNSE_CACHE)

  return RESPNSE_CACHE.get(search_term)

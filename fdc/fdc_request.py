import requests
from fdc import secrets

BASE = 'https://api.nal.usda.gov/fdc/v1/foods/search'

''' query=cheddar%20cheese
    &dataType=Foundation,SR%20Legacy
    &pageSize=25
    &sortBy=description
    &sortOrder=asc
    &brandOwner=Kar%20Nut%20Products%20Company
'''

def search():
  params = 'query=cheese'
  return requests.get(f'{BASE}?{params}&api_key={secrets.FDC_API}').json()

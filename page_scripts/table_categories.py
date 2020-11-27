from api import wiki_http as http
import models
from page_scripts import helpers
from page_scripts import food_page

def scrape(page_url, parent, column):
    ''' scrapes pages with the structure:
        1) h2 = name
        2) p = description
        3) table = list
    '''
    soup = http.request(page_url)

    return [models.WikiCategory(
        category_name(table),
        category_description(table),
        category_foods(table, column),
        parent,
    ) for table in soup.select('.mw-parser-output table.wikitable')]

def category_name(table):
    ''' scrapes the preceeding H2 text as the category name '''
    helpers.remove_superscripts(table)

    for sibling in table.previous_siblings:
        if sibling.name == 'h2':
            return helpers.scrub_string(sibling.text)


def category_foods(table, column = 1):
    ''' gets the food names and links to dedicated pages, ultimately scraping the description'''

    foods = []
    for anchor in [row.select_one(f'td:nth-child({column}) a') for row in table.select('tbody tr')]:
        if anchor and 'redlink=1' not in anchor["href"]:
            foods.append(food_page.create_food_from_anchor(anchor))

    return foods


def category_description(table):
    ''' scrapes the preceeding paragraph as a description of the category '''
    helpers.remove_superscripts(table)

    for sibling in table.previous_siblings:
        if sibling.name == 'p':
            return helpers.scrub_string(sibling.text)


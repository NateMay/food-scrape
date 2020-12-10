from page_scripts import helpers, food_page
from pages import PAGES_TO_SCRAPE
from wikipedia import wiki_http as http
import models
import pages


# logic to scrape a page with a table of foods
def scrape():
    categories = []
    for category in PAGES_TO_SCRAPE.get('table_categories'):
        categories += scrape_page(
            f'{pages.WIKI_BASE}{category[1]}', category[0], category[2])
    return categories
    # return [
    #     scrape_page(
    #         f'{pages.WIKI_BASE}{category[1]}', category[0], category[2])
    #     for category
    #     in PAGES_TO_SCRAPE.get('table_categories')
    # ]


def scrape_page(page_url, parent_category, column):
    ''' scrapes pages with the structure:
        1) h2 = name
        2) p = description
        3) table = list
    '''
    soup = http.request(page_url)

    # each table is a category
    tables = soup.select('.mw-parser-output table.wikitable')
    return [models.WikiCategory(
        category_name(table),
        category_description(table),
        category_foods(table, column),
        parent_category,
    ) for table in tables]


def category_name(table):
    # scrapes the preceeding H2 text as the category name
    helpers.remove_superscripts(table)

    for sibling in table.previous_siblings:
        if sibling.name == 'h2':
            return helpers.scrub_string(sibling.text)


def category_foods(table, column=1):
    # gets the food names and links to dedicated pages,
    # ultimately scraping the description

    foods = []
    for anchor in [row.select_one(f'td:nth-child({column}) a') for row in table.select('tbody tr')]:
        if anchor and 'redlink=1' not in anchor["href"]:
            foods.append(food_page.create_food_from_anchor(anchor))

    return foods


def category_description(table):
    # scrapes the preceeding paragraph as a description of the category
    helpers.remove_superscripts(table)

    for sibling in table.previous_siblings:
        if sibling.name == 'p':
            return helpers.scrub_string(sibling.text)

from page_scripts import helpers
from page_scripts import food_page
from api import wiki_http as http
import models

def scrape(page_url, category_name):
    ''' scrapes pages with (effectively) 1 large table
    '''

    soup = http.request(page_url)

    for superscript in soup.select('sup'):
        superscript.extract()

    foods = []

    for table in soup.select('.mw-parser-output table.wikitable'):
        for anchor in table.select('tbody tr td:first-child a'):
            if anchor and 'redlink=1' not in anchor["href"]:
                foods.append(food_page.create_food_from_anchor(anchor))

    return models.WikiCategory(category_name, helpers.scape_description(page_url, soup), foods)

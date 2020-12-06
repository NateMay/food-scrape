from page_scripts import helpers
from page_scripts import food_page
from api import wiki_http as http
import models

# logic for pages which have a single, giant table of foods

def scrape(page_url, category_name):
    # scrapes pages with (effectively) 1 large table

    soup = http.request(page_url)

    # remove footnote superscripts
    for superscript in soup.select('sup'):
        superscript.extract()

    foods = []
    # get the table
    for table in soup.select('.mw-parser-output table.wikitable'):
        # get the food links
        for anchor in table.select('tbody tr td:first-child a'):
            # ony the good ones
            if anchor and 'redlink=1' not in anchor["href"]:
                # create a food from the link
                foods.append(food_page.create_food_from_anchor(anchor))

    # store the foods within their category
    return models.WikiCategory(category_name, helpers.scape_description(page_url, soup), foods)

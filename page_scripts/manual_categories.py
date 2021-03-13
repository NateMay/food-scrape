from page_scripts import helpers, food_page
from pages import PAGES_TO_SCRAPE
import models


def scrape():
    return [create_category(name, data) for name, data in PAGES_TO_SCRAPE.get('manual_categories').items()]


def create_category(name, data):
    wiki_url = helpers.add_base_url(data.get('page_url'))
    foods = [ food_page.food_from_route(route) for route in data.get('foods')]
    return models.WikiCategory(name, helpers.scape_description(wiki_url), wiki_url, foods)

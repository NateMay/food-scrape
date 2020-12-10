from page_scripts import helpers, food_page
from pages import PAGES_TO_SCRAPE
import models


def scrape():
    return [create_category(name, data) for name, data in PAGES_TO_SCRAPE.get('manual_categories').items()]


def create_category(name, data):
    wiki_url = helpers.add_base_url(data.get('page_url'))
    foods = [ food_page.food_from_route(route) for route in data.get('foods')]
    return models.WikiCategory(name, helpers.scape_description(wiki_url), foods, wiki_url)

    # return [
    #   models.WikiCategory('Meat', helpers.scape_description(
    #       helpers.add_base_url('/wiki/Meat')), []),

    #   models.WikiCategory('Poultry', helpers.description_from_route(
    #       '/wiki/Poultry'), [food_page.food_from_route(route) for route in POULTRY_PAGES], 'Meat'),

    #   models.WikiCategory('Livestock', helpers.description_from_route(
    #       '/wiki/Livestock'), [food_page.food_from_route(route) for route in LIVESTOCK_PAGES], 'Meat'),

    #   models.WikiCategory('Game', helpers.description_from_route(
    #       '/wiki/Game_(hunting)'), [food_page.food_from_route(route) for route in GAME_PAGES], 'Meat'),

    #   models.WikiCategory('Fish', helpers.description_from_route(
    #       '/wiki/Fish_as_food'), [food_page.food_from_route(route) for route in FISH_PAGES], 'Meat'),

    #   models.WikiCategory('Seafood', helpers.description_from_route(
    #       '/wiki/Seafood'), [food_page.food_from_route(route) for route in SEAFOOD_PAGES], 'Meat'),
    # ]

from page_scripts import helpers
from api import wiki_http as http
import models


def create_food_from_anchor(anchor):
    return create_food_url(helpers.anchor_link(anchor))


def food_from_route(route):
    return create_food_url(helpers.add_base_url(route))


def create_food_url(page_url):
    soup = http.request(page_url)

    return models.WikiFood(
        helpers.scrub_string(soup.find('h1').text).replace(' as food', ''),
        helpers.scape_description(page_url, soup),
        helpers.scape_primary_image(soup),
    )

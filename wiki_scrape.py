#################################
# Name: Nate May
# Uniqname: natmay
# https://en.wikipedia.org/wiki/Lists_of_foods
#################################


import secrets
from api import db
from pages import MEATS, PAGES_TO_SCRAPE
import constants

# script for each page type
from page_scripts import ul_categories
from page_scripts import table_categories
from page_scripts import single_table_category

__version__ = '0.1.0'

CATEGORIES = []


def scrape_all_page_types():
    if True:
        for category in PAGES_TO_SCRAPE.get('multi_category_ulist_pages'):
            CATEGORIES.extend(ul_categories.scrape(
                f'{constants.WIKI_BASE}{category[1]}', category[0]))

    if True:
        for category in PAGES_TO_SCRAPE.get('multi_category_table_pages'):
            CATEGORIES.extend(table_categories.scrape(
                f'{constants.WIKI_BASE}{category[1]}', category[0], category[2]))

    if True:
        for category in PAGES_TO_SCRAPE.get('single_category_table_of_foods_pages'):
            CATEGORIES.append(single_table_category.scrape(
                f'{constants.WIKI_BASE}{category[1]}', category[0]))


def category_inserts(categories):
    commands = []
    for cat in categories:
        commands.append(cat.insert_cmd())

        if cat.foods:
            for food in cat.foods:
                commands.append(food.insert_cmd([cat.parent, cat.name]))

    return commands


if __name__ == "__main__":

    db.drop_tables()
    db.create_tables()
    # models.populate_dummies()
    scrape_all_page_types()
    db.run_commands(category_inserts(MEATS))
    db.run_commands(category_inserts(CATEGORIES))

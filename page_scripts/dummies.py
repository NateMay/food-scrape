from page_scripts import food_page, helpers
import models


def get_dummies():
    # helper function to create a test object tree
    return [
        models.WikiCategory(
            'Poultry',
            helpers.description_from_route('/wiki/Poultry'),
            helpers.add_base_url('/wiki/Poultry'),
            [food_page.create_food_url(
                helpers.add_base_url('/wiki/Egg_as_food'))],
            'Meat'
        )
    ]

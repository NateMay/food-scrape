import models
from page_scripts import food_page, helpers
from api import wiki_http as http

# This pages houses (by type) all Wikipedia Pages to be scraped 

PAGES_TO_SCRAPE = {  # reference: https://en.wikipedia.org/wiki/Lists_of_foods
    'multi_category_table_pages': [ # tuple[2] is the column index
        ('Fruit', '/wiki/List_of_culinary_fruits', 1),
        ('Vegitables', '/wiki/List_of_vegetables', 1),
        ('Pasta', '/wiki/List_of_pasta', 2),
    ],
    'multi_category_ulist_pages': [
        ('Nuts', '/wiki/List_of_culinary_nuts'),
        ('Breads', '/wiki/List_of_American_breads'),
        ('Condiments', '/wiki/List_of_condiments'),
        ('Spreads', '/wiki/List_of_spreads'),
        ('Common Dips', '/wiki/Dipping_sauce'),
        ('Sauces', '/wiki/List_of_sauces'),
        ('Mushrooms', '/wiki/Edible_mushroom'),
    ],
    'single_category_table_of_foods_pages': [
        ('Breads', '/wiki/List_of_breads'),
        ('Fried Dough', '/wiki/List_of_fried_dough_foods'),
        ('Dairy', '/wiki/List_of_dairy_products'),
        ('Cheese', '/wiki/List_of_cheeses'),
    ],
    # 'dishes': [
    #     ('Egg Dishes', '/wiki/List_of_egg_dishes'),
    #     ('Cheese Dishes', '/wiki/List_of_cheese_dishes'),
    #     ('Meat Dishes', '/wiki/List_of_meat_dishes'),
    #     ('Fish Dishes', '/wiki/List_of_fish_dishes'),
    #     ('Seafood Dishes', '/wiki/List_of_seafood_dishes'),
    #     ('Noodle Dishes', '/wiki/List_of_noodle_dishes'),
    #     ('Desserts', '/wiki/List_of_desserts'),
    #     ('Stews', '/wiki/List_of_stews'),
    #     ('Soups', '/wiki/List_of_soups'),
    #     ('Snack Foods', '/wiki/List_of_snack_foods'),
    #     ('Sandwiches', '/wiki/List_of_sandwiches'),
    #     ('Salads', '/wiki/List_of_salads'),
    #     ('Tarts & Flans', '/wiki/List_of_pies,_tarts_and_flans'),
    #     ('Noodles', '/wiki/List_of_noodles'),
    #     ('Fermented Foods', '/wiki/List_of_fermented_foods'),
    #     ('Food Pastes', '/wiki/List_of_food_pastes'),
    #     ('Porridges', '/wiki/List_of_porridges'),
    #     ('Dumplings', '/wiki/List_of_dumplings'),
    #     ("Hors D'oeuvre", '/wiki/List_of_hors_d%27oeuvre'),
    #     ('Rice Cakes', '/wiki/Rice_cake'),
    # ]
}

FISH_PAGES = [
    '/wiki/Anchovies_as_food',
    '/wiki/Catfish',
    '/wiki/Halibut',
    '/wiki/Mackerel_as_food',
    '/wiki/Pollock',
    '/wiki/Salmon_as_food',
    '/wiki/Sardines_as_food',
    '/wiki/Tilapia',
    '/wiki/Trout',
    '/wiki/Tuna',
    '/wiki/Walleye'
]

SEAFOOD_PAGES = [
    '/wiki/Squid_as_food',
    '/wiki/Clams',
    '/wiki/Lobster',
    '/wiki/Crayfish_as_food',
    '/wiki/Oyster',
    '/wiki/Mussel',
    '/wiki/Octopus_as_food',
    '/wiki/Scallop',
    '/wiki/Shrimp_and_prawn_as_food',
    '/wiki/Sea_urchin'
]

POULTRY_PAGES = [
    '/wiki/Egg_as_food',
    '/wiki/Chicken_as_food',
    '/wiki/Duck_as_food',
    '/wiki/Turkey_as_food',
]

LIVESTOCK_PAGES = [
    '/wiki/Beef',
    '/wiki/Lamb_and_mutton',
    '/wiki/Pork',
    '/wiki/Veal',
]

GAME_PAGES = ['/wiki/Venison']

MEATS = [
    models.WikiCategory('Meat', helpers.scape_description(
        helpers.add_base_url('/wiki/Meat')), []),

    models.WikiCategory('Poultry', helpers.description_from_route(
        '/wiki/Poultry'), [food_page.food_from_route(route) for route in POULTRY_PAGES], 'Meat'),

    models.WikiCategory('Livestock', helpers.description_from_route(
        '/wiki/Livestock'), [food_page.food_from_route(route) for route in LIVESTOCK_PAGES], 'Meat'),

    models.WikiCategory('Game', helpers.description_from_route(
        '/wiki/Game_(hunting)'), [food_page.food_from_route(route) for route in GAME_PAGES], 'Meat'),

    models.WikiCategory('Fish', helpers.description_from_route(
        '/wiki/Fish_as_food'), [food_page.food_from_route(route) for route in FISH_PAGES], 'Meat'),

    models.WikiCategory('Seafood', helpers.description_from_route(
        '/wiki/Seafood'), [food_page.food_from_route(route) for route in SEAFOOD_PAGES], 'Meat'),
]

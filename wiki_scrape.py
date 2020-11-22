#################################
# Name: Nate May
# Uniqname: natmay
# https://en.wikipedia.org/wiki/Lists_of_foods
#################################


from bs4 import BeautifulSoup
import requests
import json
import sqlite3
import secrets
import wiki_food as wfood
import wiki_category as wcat

CACHE_FILENAME = 'wiki_cache.json'
WIKI_BASE = 'https://en.wikipedia.org'

CATEGORIES = []

PAGES_TO_SCRAPE = { # reference: https://en.wikipedia.org/wiki/Lists_of_foods
    'multi_category_table_pages': [
        ('Fruit', '/wiki/List_of_culinary_fruits'),
        ('Vegitables', '/wiki/List_of_vegetables'),
    ],
    'multi_category_ulist_pages': [
        ('Nuts', '/wiki/List_of_culinary_nuts'),
        # ('Mushrooms', '/wiki/Edible_mushroom'),
        # ('Breads', '/wiki/List_of_American_breads'),
    ],
    'single_category_table_pages': [
        ('Breads', '/wiki/List_of_breads'),
        ('Dairy', '/wiki/List_of_dairy_products'),
    ],
    # TODO
    'single_food_pages': [
        ('Eggs', 'wiki/Egg_as_food'),

    ],
    'single_category_pages': [
        ('Rice', 'wiki/wiki/Rice'),
        ('Meat', 'wiki/wiki/Meat'),
    ]
}


# TODO
# don't scrape the nuts section, there's already a nuts page
BAKED_GOODS_PAGE = '/wiki/List_of_baked_goods'  # some overlap with breads page
CHEESES_PAGE = '/wiki/List_of_cheeses'
# cereals ??


CACHE = {}
def save_cache(cache_dict):
    ''' Saves the current state of the cache to disk

    Parameters
    ----------
    cache_dict: dict
        The dictionary to save

    Returns
    -------
    None
    '''
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(CACHE_FILENAME, "w")
    fw.write(dumped_json_cache)
    fw.close()


def open_cache():
    ''' Opens the cache file if it exists and loads the JSON into
    the CACHE_DICT dictionary. If the cache file doesn't exist, 
    creates a new cache dictionary

    Parameters
    ----------
    None

    Returns
    -------
    The opened cache: dict
    '''
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict


def request_or_uncache(url):
    '''Requests a url or gets the html from the cache

    Parameters
    ----------
    url: string
        address of the website to scrape

    Returns
    -------
    BeautifulSoup
        a BeautifulSoup object of the parsed html
    '''
    RESPNSE_CACHE = open_cache()

    if url in RESPNSE_CACHE:
        print('Using Cache')
    else:
        print('Fetching')
        RESPNSE_CACHE[url] = requests.get(url).text
        save_cache(RESPNSE_CACHE)

    return BeautifulSoup(RESPNSE_CACHE.get(url), 'html.parser')


def multi_tables_foods(table):
    ''' gets the food names and links to dedicated pages, ultimately scraping the description'''

    foods = []
    for anchor in [row.select_one('td:first-child a') for row in table.select('tbody tr')]:
        if anchor and 'redlink=1' not in anchor["href"]:
            foods.append(create_food_from_anchor(anchor))

    return foods


def create_food_from_anchor(anchor):
    page_url = f'{WIKI_BASE}{anchor["href"]}'
    soup = request_or_uncache(page_url)

    return wfood.WikiFood(
        anchor.text,
        scape_page_description(soup, page_url),
        scape_food_image(soup),
    )


def scape_food_image(soup):
    ''' scrapes the url of the first image '''
    if not soup.find(class_="mw-parser-output"):
        return ''
    img = soup.find(class_="mw-parser-output").find('img')
    return img['src'][2:] if img and img['src'] else None


def scape_page_description(soup, page_url):
    ''' scrapes all paragraph elements before the table of contents as the food description '''

    soup = request_or_uncache(page_url)

    description = ''

    toc = soup.find(id="toc")
    if not toc:
        name = soup.find('h1').text
        print(f'Could not assertain the descripton for {name}: {page_url}')
        return ''

    max_paragraphs = 5

    for element in soup.find(class_="mw-parser-output").children:
        if element == toc or max_paragraphs <= 0:
            break
        elif element.name == 'p':
            description += element.text
            max_paragraphs -= 1

    return description


def multi_tables_description(table):
    ''' scrapes the preceeding paragraph as a description of the category '''
    for sibling in table.previous_siblings:
        if sibling.name == 'p':
            return sibling.text


def multi_tables_name(table):
    ''' scrapes the preceeding H2 text as the category name '''

    for sibling in table.previous_siblings:
        if sibling.name == 'h2':
            return sibling.text.replace('[edit]', '')


def scrape_multi_tables_page(page_url, parent):
    ''' scrapes pages with the structure:
        1) h2 = name
        2) p = description
        3) table = list
    '''
    soup = request_or_uncache(page_url)
    for superscript in soup.select('sup'):
        superscript.extract()

    return [wcat.WikiCategory(
        multi_tables_name(table),
        multi_tables_description(table),
        multi_tables_foods(table),
        parent,
    ) for table in soup.find(class_="mw-parser-output").select('table')]


def scrape_ul_page(page_url, parent):
    ''' scrapes pages with the structure:
        1) h2 = name
        2) p = description
        3) ul = list
    '''
    soup = request_or_uncache(page_url)

    for superscript in soup.select('sup'):
        superscript.extract()

    results = []

    for anchor in soup.find(id="toc").select('ul > li > a'):

        idstr = anchor['href'][1:]
        if idstr in ['See_also', 'Notes', 'References']:
            continue

        h2 = soup.find(id=idstr).parent

        results.append(wcat.WikiCategory(
            h2.text.replace('[edit]', ''),
            h2.find_next_sibling("p").text,
            getUlFoods(h2),
            parent,
        ))

    return results


def getUlFoods(h2):
    foods = []
    for anchor in h2.find_next_sibling("ul").select('li > a:first-child'):

        page_url = f'{WIKI_BASE}{anchor["href"]}'
        soup = request_or_uncache(page_url)

        foods.append(wfood.WikiFood(
            soup.find('h1').text.replace('[edit]', ''),
            scape_page_description(soup, page_url),
            scape_food_image(soup),
        ))
    return foods


def scrape_single_table_page(page_url, category_name):
    ''' scrapes pages with (effectively) 1 large table
    '''

    soup = request_or_uncache(page_url)

    for superscript in soup.select('sup'):
        superscript.extract()

    foods = []

    for table in soup.find(class_="mw-parser-output").select('table'):
        if 'wikitable' not in table.get('class'):
            continue

        for anchor in table.select('tbody tr td:first-child a'):
            if anchor and 'redlink=1' not in anchor["href"]:
                food = create_food_from_anchor(anchor)
                print(food)
                foods.append(food)

    return wcat.WikiCategory(category_name, scape_page_description(soup, page_url), foods)


def db_connection():
    return sqlite3.connect('food_data.sqlite')


def create_category_table():
    drop_categories = 'DROP TABLE IF EXISTS "Categories";'
    create_categories = '''CREATE TABLE IF NOT EXISTS "Categories" (
      "Id"               INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
      "Name"             TEXT NOT NULL,
      "Description"      TEXT,
      "Parent"           TEXT
  );
  '''

    drop_foods = 'DROP TABLE IF EXISTS "Foods";'
    create_foods = '''CREATE TABLE IF NOT EXISTS "Foods" (
      "Id"               INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
      "Name"             TEXT NOT NULL,
      "Description"      TEXT,
      "Image_src"        TEXT
  );
  '''

    run_commands([
        drop_categories,
        create_categories,
        drop_foods,
        create_foods
    ])


def run_commands(commands):
    conn = db_connection()
    cur = conn.cursor()
    for command in commands:
        print(f'running command: {command}', "\n")
        cur.execute(command)
    conn.commit()
    conn.close()


if __name__ == "__main__":

    create_category_table()

    if True:
        for category in PAGES_TO_SCRAPE.get('multi_category_table_pages'):
            CATEGORIES.extend(scrape_multi_tables_page(
                f'{WIKI_BASE}{category[1]}', category[0]))

        for category in PAGES_TO_SCRAPE.get('multi_category_ulist_pages'):
            CATEGORIES.extend(scrape_ul_page(
                f'{WIKI_BASE}{category[1]}', category[0]))

        for category in PAGES_TO_SCRAPE.get('single_category_table_pages'):
            CATEGORIES.append(scrape_single_table_page(
                f'{WIKI_BASE}{category[1]}', category[0]))

    # CATEGORIES = [wcat.WikiCategory('Test', 'desc', [], 'Parent')]
    print('-------------------------')

    commands = []
    for cat in CATEGORIES:
        print('------ CATEGORY: ', cat, ' ------')
        commands.append(cat.insert_cmd())
        if not cat.foods:
            print(cat.name, 'has no foods')
            
        else:
            for food in cat.foods:
                commands.append(food.insert_cmd())

    run_commands(commands)

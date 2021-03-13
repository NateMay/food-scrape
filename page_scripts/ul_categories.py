from wikipedia import wiki_http as http
from page_scripts import helpers, food_page
from pages import PAGES_TO_SCRAPE
import pages
import models

# scapes pages that have several categories, but the foods are
# in a <ul>

def scrape():
    categories = []
    for category in PAGES_TO_SCRAPE.get('ul_categories'):
        page_url = f'{pages.WIKI_BASE}{category[1]}'
        parent_category = category[0]

        categories.append(models.WikiCategory(
            parent_category,
            helpers.scape_description(page_url), 
            page_url, 
            [],
            scrape_page(page_url)
        ))
    return categories


def scrape_page(page_url):
    ''' scrapes pages with the structure:
        1) h2 = name
        2) p = description
        3) ul = list
    '''
    soup = http.request(page_url)

    # remove footnote superscripts
    for superscript in soup.select('sup'):
        superscript.extract()

    results = []

    # scrape from the table of contents
    for anchor in soup.select('#toc ul > li > a'):

        #  ignore irrelevant sections
        idstr = anchor['href'][1:]
        if idstr in ['See_also', 'Notes', 'References']:
            break

        h2 = soup.find(id=idstr).parent
        # selector: 'p, div' did not work
        description = h2.find_next_sibling("p") or h2.find_next_sibling("div")

        results.append(models.WikiCategory(
            h2.text.replace('[edit]', ''),
            description.text.strip(),
            page_url,
            getUlFoods(h2)
        ))

    return results


def getUlFoods(h2):
    # recieves the h2 element and return an list of links to 
    # the foods in the list following it
    return [
        food_page.create_food_from_anchor(anchor)
        for anchor
        in h2.find_next_sibling("ul").select('li > a:first-child')
    ]

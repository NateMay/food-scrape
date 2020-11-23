from page_scripts import helpers
from api import wiki_http as http
import models
from page_scripts import food_page


def scrape(page_url, parent):
    ''' scrapes pages with the structure:
        1) h2 = name
        2) p = description
        3) ul = list
    '''
    soup = http.request(page_url)

    for superscript in soup.select('sup'):
        superscript.extract()

    results = []

    for anchor in soup.find(id="toc").select('ul > li > a'):

        idstr = anchor['href'][1:]
        if idstr in ['See_also', 'Notes', 'References']:
            continue

        h2 = soup.find(id=idstr).parent

        results.append(models.WikiCategory(
            h2.text.replace('[edit]', ''),
            h2.find_next_sibling("p").text,
            getUlFoods(h2),
            parent,
        ))

    return results


def getUlFoods(h2):
    return [
        food_page.create_food_from_anchor(anchor)
        for anchor
        in h2.find_next_sibling("ul").select('li > a:first-child')
    ]

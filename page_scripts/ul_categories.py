from page_scripts import helpers
from api import wiki_http as http
import models
from page_scripts import food_page

# 

def scrape(page_url, parent):
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
            getUlFoods(h2),
            parent,
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

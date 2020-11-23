from page_scripts import helpers
from api import wiki_http as http
import models

def create_food_from_anchor(anchor):
    page_url = helpers.anchor_link(anchor)
    soup = http.request(page_url)

    return models.WikiFood(
        helpers.scrub_string(anchor.text),
        scape_page_description(soup, page_url),
        scape_food_image(soup),
    )

def scape_page_description(soup, page_url):
    ''' scrapes all paragraph elements before the table of contents as the food description '''

    soup = http.request(page_url)

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

    return helpers.scrub_string(description)

def scape_food_image(soup):
    ''' scrapes the url of the first image '''
    if not soup.find(class_="mw-parser-output"):
        return ''
    img = soup.find(class_="mw-parser-output").find('img')
    return img['src'][2:] if img and img['src'] else None

import re
import constants
from api import wiki_http as http


def scrub_string(value):
    remove_edit_btn = value.strip().replace('[edit]', '')
    to_single_quotes = remove_edit_btn.replace('"', "'")
    remove_citations = re.sub('\[\d{0,2}\]', '', to_single_quotes)
    return remove_citations.strip()


def remove_superscripts(table):
    for superscript in table.select('sup'):
        superscript.extract()


def anchor_link(anchor):
    return anchor["href"] if 'http' in anchor["href"] else add_base_url(anchor["href"])


def add_base_url(route):
    return f'{constants.WIKI_BASE}{route}'


def description_from_route(route):
    return scape_description(add_base_url(route))


def scape_description(page_url, soup=None):
    ''' scrapes all paragraph elements before the table of contents as the food description '''
    if not soup:
        soup = http.request(page_url)

    as_food = soup.select_one("#As_food")

    return scrape_as_food_section(soup, as_food) if as_food else scrape_primary_page_description(soup)


def scrape_as_food_section(soup, as_food):
    return get_section_paragraphs(soup, as_food.parent.next_siblings)


def scrape_primary_page_description(soup):
    return get_section_paragraphs(soup, soup.find(
        class_="mw-parser-output").children)


def isHeader(el):
    return el.name == 'h2' or el.name == 'h3'


def get_section_paragraphs(soup, iterable):
    paras = []

    for element in iterable:
        if element.name == 'p':
            paras.append(element.text)
        elif element == soup.find(id="toc") or len(paras) >= 4 or isHeader(element):
            break

    return scrub_string('\n'.join(paras))


def scape_primary_image(soup):
    ''' scrapes the url of the first image '''
    if not soup.find(class_="mw-parser-output"):
        return ''
    img = soup.select_one('.mw-parser-output img.thumbimage')
    return img['src'][2:] if img and img['src'] else None

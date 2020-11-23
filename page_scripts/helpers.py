import re
import constants

def scrub_string(value):
    remove_edit_btn = value.strip().replace('[edit]', '')
    to_single_quotes = remove_edit_btn.replace('"', "'")
    remove_citations = re.sub('\[\d{0,2}\]', '', to_single_quotes)
    return remove_citations.strip()

def remove_superscripts(table):
    for superscript in table.select('sup'):
        superscript.extract()

def anchor_link(anchor):
    return anchor["href"] if 'http' in anchor["href"] else f'{constants.WIKI_BASE}{anchor["href"]}'

    

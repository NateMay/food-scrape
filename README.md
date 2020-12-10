# Food Metadata and Nutrition Aggregator

## Required Packages

- requests
- bs4 (BeautifulSoup)
- sqlite3
- flask

## Instructions for Use

### Scraping

- Open `scrape.py`
- Set all values in the `SHOULD` dictionary to `True`
- run `python scrape.py` from the project root directory

### Flask Application

- obtain a Food Data Central [API key](https://fdc.nal.usda.gov/api-key-signup.html)
- create `fdc/secrets.py` and add `FDC_API = 'XXXXXX'` replace your API Key
- run `python app.py` from the project root directory
- open `localhost:5000` in a web browser

## Inventory

| Variable | Description |
|----------|-------------|
| scrape.py | Entry point into the scraping flow |
| wiki_cache.py | cache for the Wikipedia scrape |
| pages.py | Organizes Wikipedia page urls to be scraped by type |
| models.py | Data models file |
| app.py | Entry point and routing logic for the Flask web application |
| /templates | HTML and templating files |
| /page_scripts | Wikipedia scraping logic |
| /api | SQL database interactions and Wikipedia request caching |
| /fdc | USDA Nutrition Database request logic and caching |

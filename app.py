
from flask import Flask, request, render_template
import db
from fdc import fdc_http

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('landing.html')

# handles a new search term
@app.route('/handle_term', methods=['POST'])
def handle_term():
    term = request.form["term"]

    return render_template(
        'select_wiki.html', 
        rows=db.query_db_by(f'%{term}%'),
        term=term,
    )

# handles a user selecting a food form the search results
@app.route('/select_food', methods=['POST'])
def select_food():
    wiki_food = eval(request.form["wiki_food"])
    wiki_name = wiki_food[1]
    results = fdc_http.search(wiki_name)

    return render_template(
        'select_fdc.html',
        wiki_food=wiki_food,
        id=wiki_food[0],
        name=wiki_name,
        description=wiki_food[2],
        src=wiki_food[4],
        cat1=db.get_category_name(wiki_food[5]),
        cat2=db.get_category_name(wiki_food[6]),
        foods=results.get('foods'),
        search=results.get('foodSearchCriteria').get('query')
    )

@app.route('/select_fdc', methods=['POST'])
def select_fdc():
    fdc_food = eval(request.form["fdc_food"])
    wiki_food = eval(request.form["wiki_food"])
    nutrients = fdc_food.get('foodNutrients')

    return render_template(
        'connected.html',
        fdc_food=fdc_food,
        wiki_food=wiki_food,
        name=wiki_food[1],
        description=wiki_food[2],
        src=wiki_food[4],
        cat1=db.get_category_name(wiki_food[5]),
        cat2=db.get_category_name(wiki_food[6]),
        nutrients=nutrients
    )

@app.route('/connect', methods=['POST'])
def connect():
    fdc_food = eval(request.form["fdc_food"])
    wiki_food = eval(request.form["wiki_food"])
    db.connect_fdc_wiki(fdc_food, wiki_food)
    name = wiki_food[1]
    results = fdc_http.search(name)

    return render_template(
        'select_fdc.html',
        wiki_food=wiki_food,
        id=wiki_food[0],
        name=name,
        description=wiki_food[2],
        src=wiki_food[4],
        cat1=db.get_category_name(wiki_food[5]),
        cat2=db.get_category_name(wiki_food[6]),
        foods=results.get('foods'),
        search=results.get('foodSearchCriteria').get('query')
    )

if __name__ == "__main__":

    print('starting Flask app', app.name)  
    app.run(debug=True)
    exit()

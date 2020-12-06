
from flask import Flask, request, render_template
from api import db

app = Flask(__name__)

@app.route('/')
def index():     
     return render_template('landing.html')

# handles a new search term
@app.route('/handle_term', methods=['POST'])
def handle_term():
    term = request.form["term"]
    return render_template(
      'search_table.html', 
      rows=db.query_db_by(f'%{term}%'),
      term=term
    )

# handles a user selecting a food form the search results
@app.route('/select_food', methods=['POST'])
def select_food():
    row = eval(request.form["row"])
    id = row[0]
    name = row[1]
    description = row[2]
    src = row[3]
    cat1 = row[4]
    cat2 = row[5]

    return render_template(
      'select_fdc.html', 
      id=id,
      name=name,
      description=description,
      src=src,
      cat1=cat1,
      cat2=cat2,
    )

if __name__ == "__main__":

    print('starting Flask app', app.name)  
    app.run(debug=True)
    exit()

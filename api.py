import flask
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# data set to use in the api
# data set also happens to be recipes I have made before and where the ratings are how they came out, tasted and based on user feedback
recipes = [
    {
        'id': 0,
        'name': 'Oatmeal raisin cookies',
        'rating': '5.0'
    },
    {
        'id': 1,
        'name': 'Brownies',
        'rating': '3.0'
    },
    {
        'id': 2,
        'name': 'M&M cookies',
        'rating': '3.5'
    },
    {
        'id': 3,
        'name': 'Plain sponge cake',
        'rating': '4.0'
    },
    {
        'id': 4,
        'name': 'Chocolcate chip cookies',
        'rating': '2.0'
    }
]

# maps url path '/' to the function home and performs a get request to return the contents in the <h1> tag
@app.route('/', methods = ['GET'])
def home():
    return "<h1>Hello World</h1>"

# maps url path below to the function to return json of the dataset
@app.route('/api/v1/resources/recipes/all', methods = ['GET'])
def api_all():
    return jsonify(recipes)

# returns json object of the specified id/s in a query of type ...recipes?id=xxx
@app.route('/api/v1/resources/recipes', methods = ['GET'])
def api_id():
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Error: No id specified"
    
    results = []

    for recipe in recipes:
        if recipe['id'] == id:
            results.append(recipe)
        
    return jsonify(results)

# FURTHER ROUTES TO BE ADDED

app.run()
import flask
import json
import sqlite3
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True

with open("recipes.json") as file:
    recipes = json.load(file)


def dict_factory(cursor, row):
    """
    Convert to dictionary

    Paramaters:
        cursor (Object): Cursor object in sqlite3 used to execute SQL statements
        row (Array): Row/record in the database table

    Returns:
        d: A dictionary format of the table row
    """
    
    d = {}
    for index, column in enumerate(cursor.description):
        d[column[0]] = row[index]
    return d


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Desert Recipes Attempted</h1>
    <p>An API of my attempted desert recipes and their outcomes.</p>'''


@app.route('/api/v1/resources/recipes/all', methods=['GET'])
def api_all():
    conn = sqlite3.connect('recipes.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_recipes = cur.execute('SELECT * FROM recipes;').fetchall()

    return jsonify(all_recipes)


@app.errorhandler(404)
def page_not_found(e):
    return '<h1>404</h1><br><p>The resource could not been found.</p>', 404


@app.route('/api/v1/resources/recipes', methods=['GET'])
def api_filter():
    query_parameters = request.args

    id = query_parameters.get('id')
    name = query_parameters.get('name')
    difficulty = query_parameters.get('difficulty')
    outcome = query_parameters.get('outcome')

    query = 'SELECT * FROM recipes WHERE'
    to_filter = []

    if id:
        query += ' ID=? AND'
        to_filter.append(id)
    if name:
        query += ' NAME=? AND'
        to_filter.append(name)
    if difficulty:
        query += ' DIFFICULTY=? AND'
        to_filter.append(difficulty)
    if outcome:
        query += ' OUTCOME=? AND'
        to_filter.append(outcome)
    if not (id or name or difficulty or outcome):
        return page_not_found(404)

    query = query[:-4] + ';'

    conn = sqlite3.connect('recipes.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, to_filter).fetchall()

    return jsonify(results)


app.run()

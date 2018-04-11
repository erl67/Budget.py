#erl67
REBUILD_DB = False
FDEBUG = True

import os, re, json
from sys import stderr
from flask import Flask, g, send_from_directory, flash, render_template, abort, request, redirect, url_for, session, Response, jsonify
from flask_restful import Resource, Api
from flask_debugtoolbar import DebugToolbarExtension
from datetime import datetime, date, timedelta
from dateutil import parser
from random import getrandbits

transactions = dict()
categories = dict()
budget = dict()

def create_app():
    app = Flask(__name__)
    DB_NAME = os.path.join(app.root_path, 'data/budget.txt')
    
    app.config.update(dict(
        SECRET_KEY='erl67_',
        TEMPLATES_AUTO_RELOAD=True,
        USE_THREADED = True,
    ))
        
    if REBUILD_DB == True and os.access(DB_NAME, os.W_OK):
        os.remove(DB_NAME)
        print('DB Dropped')
        
    if os.access(DB_NAME, os.W_OK):
        print('DB Exists')
    else:
        print('DB does not exist')
        
    print(app.__str__(), end="  ")
    return app

app = create_app()
api = Api(app)

class cats(Resource):    
    def get(self):
        return categories
    
    def put(self, category=None):
        category = request.json['category']
        eprint(str(category))
        categories[str(len(categories))] = category
        flash("category added : " + str(category))
        return {}, 204
    
    def delete(self, category=None):
        category = request.json['category']
        del categories[category]
        flash("category removed : " + str(category))
        return {}, 204
    
class trans(Resource):
    def get(self):
        return transactions
    
class budgetAll(Resource):
    def get(self):
        return budget
    
api.add_resource(cats, '/c')
api.add_resource(trans, '/t')
api.add_resource(budgetAll, '/b')
    
@app.route("/save")
def save_data():
    with open('data/categories.txt', 'w') as fh:
        json.dump(g.categories, fh, indent=1)
    with open('data/budget.txt', 'w') as fh:
        json.dump(g.budget, fh, indent=1)
    with open('data/transactions.txt', 'w') as fh:
        json.dump(g.transactions, fh, indent=1)
    flash("Data saved to file")
    return redirect(url_for("index"))

@app.route("/open")
def read_data():
    global categories, budget, transactions
    with open('data/categories.txt', 'r') as fh:
        categories = json.load(fh)
    with open('data/budget.txt', 'r') as fh:
        budget = json.load(fh)
    with open('data/transactions.txt', 'r') as fh:
        transactions = json.load(fh)
    flash("Data loaded from file")
    return redirect(url_for("index"))
    
@app.before_request
def before_request():
    g.budget = budget
    g.transactions = transactions
    g.categories = categories
    eprint("g.budget: " + str(g.budget))
    eprint("g.trans: " + str(g.transactions))
    eprint("g.cats: " + str(g.categories))
        
@app.before_first_request
def before_first_request():
    eprint("    🥇")
    
@app.route("/db/")
def rawstats():
    msg = ""
    msg += str(budget)
    msg += "\n\n"
    msg += str(categories)
    msg += "\n\n"
    msg += str(transactions)
    msg += "\n\n"
    return Response(render_template('test.html', testMessage=msg), status=203, mimetype='text/html')

@app.route('/')
def index():
    return Response(render_template('index.html'), status=200, mimetype='text/html')

# @app.route('/ajax.js')
# def ajax():
#     return Response(render_template('ajax.js'), status=200, mimetype='application/javascript')

@app.errorhandler(403)
@app.errorhandler(404)
def page_not_found(error):
    return Response(render_template('404.html', errno=error), status=404, mimetype='text/html')

@app.errorhandler(405)
def wrong_method(error):
    return Response("You shouldn't have done that", status=405, mimetype='text/html')

@app.route('/418/')
def err418(error=None):
    return Response(render_template('404.html', errno=error), status=418, mimetype='text/html')

@app.route('/favicon.ico') 
def favicon():
    if bool(getrandbits(1))==True:
        return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')
    else:
        return send_from_directory(os.path.join(app.root_path, 'static'), 'faviconF.ico', mimetype='image/vnd.microsoft.icon')

def eprint(*args, **kwargs):
    print(*args, file=stderr, **kwargs)
    
TAG_RE = re.compile(r'<[^>]+>')
def remove_tags(text):
    return TAG_RE.sub('', text)

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code stackoverflow.com/a/22238613/7491839 """
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))
    
if __name__ == "__main__":
    print('Starting......')
    if FDEBUG==True:
        app.config.update(dict(
            DEBUG=True,
            DEBUG_TB_INTERCEPT_REDIRECTS=False,
            TEMPLATES_AUTO_RELOAD=True,
        ))
        app.jinja_env.auto_reload = True
        toolbar = DebugToolbarExtension(app) 
        app.run(use_reloader=True, host='0.0.0.0')
    else:
        app.run()
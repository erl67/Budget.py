#erl67
FDEBUG = True

import os, re, json, pickle
from sys import stderr
from flask import Flask, g, send_from_directory, flash, render_template, abort, request, redirect, url_for, Response, jsonify
from flask_restful import Resource, Api
from flask_debugtoolbar import DebugToolbarExtension
from datetime import datetime, date, timedelta
from dateutil import parser
from random import getrandbits

transactions = dict()
categories = dict()

def create_app():
    app = Flask(__name__)
    
    app.config.update(dict(
        SECRET_KEY='erl67_',
        TEMPLATES_AUTO_RELOAD=True,
        USE_THREADED = True,
    ))
        
    print(app.__str__(), end="  ")
    return app

app = create_app()
api = Api(app)

class cats(Resource):    
    def get(self):
        return categories, 200
    
    def put(self, category=None):
        category = request.json['category']
        eprint(str(category))
        categories[str(len(categories))] = category
        flash("category added : " + str(category))
        return {}, 201
    
    def delete(self, category=None):
        category = request.json['category']
        del categories[category]
        flash("category removed : " + str(category))
        return {}, 204
    
class trans(Resource):
    def get(self):
        return transactions, 200
    
api.add_resource(cats, '/c')
api.add_resource(trans, '/t')
    
@app.route("/save")
def save_data():
    with open('data/categories.p', 'wb') as fh:
        pickle.dump(g.categories, fh)
    with open('data/transactions.p', 'wb') as fh:
        pickle.dump(g.transactions, fh)
    flash("Data saved to file")
    return redirect(url_for("index"))

@app.route("/open")
def read_data():
    global categories, transactions
    with open('data/categories.p', 'rb') as fh:
        categories = pickle.load(fh)
    with open('data/transactions.p', 'rb') as fh:
        transactions = pickle.load(fh)
    flash("Data loaded from file")
    return redirect(url_for("index"))
    
@app.before_request
def before_request():
    g.transactions = transactions
    g.categories = categories
    eprint("g.trans: " + str(g.transactions))
    eprint("g.cats: " + str(g.categories))
        
@app.before_first_request
def before_first_request():
    eprint("    🥇")

@app.route('/')
def index():
    return Response(render_template('index.html'), status=200, mimetype='text/html')

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
#         toolbar = DebugToolbarExtension(app) 
        app.run(use_reloader=True, host='0.0.0.0')
    else:
        app.run()
#erl67
FDEBUG = True

import os, re, json, pickle
from sys import stderr
from functools import wraps
from flask import Flask, g, send_from_directory, flash, render_template, abort, request, redirect, url_for, Response, session
from flask_restful import Resource, Api
from flask_debugtoolbar import DebugToolbarExtension
from random import getrandbits

transactions = dict()
categories = dict()
apiKeys = ['erl67api', 'test', 'random', 'key4']
auth = False

def create_app():
    app = Flask(__name__)
    
    app.config.update(dict(
        SECRET_KEY='erl67',
        TEMPLATES_AUTO_RELOAD=True,
        USE_THREADED = True,
    ))
        
    print(app.__str__(), end="  ")
    return app

app = create_app()
api = Api(app)

def require_apikey(view_function):  #coderwall.com/p/4qickw/require-an-api-key-for-a-route-in-flask-using-only-a-decorator
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        if (request.args.get('key') and request.args.get('key') in apiKeys) or (session.get('apiKey') in apiKeys):
            return view_function(*args, **kwargs)
        else:
            abort(401)
    return decorated_function

class cats(Resource):    
    @require_apikey
    def get(self, cat=None):
        if not cat:
            return categories, 200
        else:
            try:
                return categories[str(cat)], 200
            except:
                abort(404)

    @require_apikey
    def post(self):
        category = request.json['category']
        eprint(str(category))
        if category not in categories.values():
            categories[str(len(categories))] = category
            flash("category added : " + str(category))
        else:
            flash("category already exists")
        return {}, 201
    
    @require_apikey
    def delete(self):
        category = request.json['category']
        del categories[category]
        flash("category " + str(category) + " removed")
        return {}, 204
    
class trans(Resource):
    @require_apikey
    def get(self, transaction=None, val=None):
        if not transaction:
            return transactions, 200
        elif not val:
            try:
                result = transactions[str(transaction)]
                return result, 200
            except:
                abort(404)
        else:
            try:
                result = transactions[str(transaction)][str(val)]
                return result, 200
            except:
                abort(404)
    
    @require_apikey
    def put(self):
        transact = dict()
        transact['name'] = remove_tags(request.json['name'])
        transact['date'] = request.json['date']
        transact['total'] = request.json['total']
        transact['category'] = request.json['category']
        eprint(str(transact))
        transactions[str(len(transactions))] = transact
        flash("transaction added")
        return {}, 201
    
    @require_apikey
    def delete(self):
        transaction = request.json['transaction']
        eprint(str(transaction))
        if transaction in transactions:
            del transactions[transaction]
            flash("transaction removed")
        else:
            flash("nothing to remove")
        return {}, 204
    
api.add_resource(cats, '/c', '/api/cats', '/api/cats/<int:cat>')
api.add_resource(trans, '/t', '/api/transactions', '/api/transactions/<int:transaction>', '/api/transactions/<int:transaction>&value=<val>')
    
@app.before_request
def before_request():
    session['requests'] = int(session.get('requests') or 0) + 1
    g.session = session
    g.transactions = transactions
    g.categories = categories
    eprint("g.cats: " + str(g.categories), end="\t")
    eprint("g.trans: " + str(g.transactions), end="\n\n")
        
@app.before_first_request
def before_first_request():
    global auth
    session['starts'] = int(session.get('starts') or 0) + 1
    if session.get('apiKey') in apiKeys:
        auth = True
    eprint("\t🥇 \t\t" + str(auth))

@app.route("/save")
@require_apikey
def save_data():
    with open('data/categories.p', 'wb') as fh:
        pickle.dump(g.categories, fh)
    with open('data/transactions.p', 'wb') as fh:
        pickle.dump(g.transactions, fh)
    flash("Data saved to file")
    return redirect(url_for("index"))

@app.route("/open")
@require_apikey
def read_data():
    global categories, transactions
    with open('data/categories.p', 'rb') as fh:
        categories = pickle.load(fh)
    with open('data/transactions.p', 'rb') as fh:
        transactions = pickle.load(fh)
    flash("Data loaded from file")
    return redirect(url_for("index"))

@app.route("/setkey")
def setkey(k=int(getrandbits(2))):
    session['apiKey'] = apiKeys[k]
    return redirect(url_for("index"))

@app.route('/')
def index():
    return Response(render_template('index.html'), status=200, mimetype='text/html')

@app.route('/review')
def review():
    return Response(render_template('analysis.html'), status=200, mimetype='text/html')

@app.errorhandler(403)
@app.errorhandler(404)
def page_not_found(error):
    return Response(render_template('404.html', errno=error), status=404, mimetype='text/html')

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

# def json_serial(obj):
#     """JSON serializer for objects not serializable by default json code stackoverflow.com/a/22238613/7491839 """
#     if isinstance(obj, (datetime, date)):
#         return obj.isoformat()
#     raise TypeError ("Type %s not serializable" % type(obj))
    
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
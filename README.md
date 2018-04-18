# Name: Eric Laslo
Pitt ID: Erl67@pitt.edu

## Installation

1. Set Flask_APP=budget.py, flask run

2. Using Flask-restful and bootstrap 4.1

## Running the App

1. GOTO http://127.0.0.1:5000

2. API key (or token) must be loaded into session before using the api. A link to load a key will be displayed. It's not really necessary, but I wanted to add it, and didn't want to put it on every request. None of the API or saving and loading data will work without it.

3. Saved data to file for ease of testing. Left hand side has controls to let you load data from a file, along with save changes to data. The link to load data will only display if no categories exist. You will have to delete them all if you want to reload from file. Save will save all of the current data to a file, overwriting whatever is there. The saved data is stored as a pickle.

4. Api routes for get are:  
`Categories: '/c', '/api/cats', '/api/cats/<int:cat>'`  
`Transactions: '/t', '/api/transactions', '/api/transactions/<int:transaction>', '/api/transactions/<int:transaction>&value=<val>`

5. Console will show all the AJAX requests.

6. Buttons run AJAX to the rest API, except the last button because I didn't want it that way.

7. Color is generated by a hash of innerHTML. If AJAX is a success the recolor function is called, so the color will change (if html changes).

8. Analysis page runs a minimum version of the ajax, just to get JSON of the data. Delay of one second is applied to ensure ajax completes before analyzing. The functions could be moved to the ajax calls themselves, but I preferred to have them lowly coupled.

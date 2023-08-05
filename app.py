import url_database

from flask import Flask, request
from flask import Flask, render_template, redirect, url_for, session

# from slugify import slugify

import string
import random


app = Flask(__name__)


@app.route('/', methods = ["GET", "POST"])
def index():
    original_url = request.form.get('input')
    if request.method == "POST":
       short_code = generate_short_code()
       url_database.add_url(original_url, short_code)
       short_url = request.host_url + short_code
       return render_template('index.html', result=short_url)
    elif request.method == "GET":
        return render_template("index.html", result=None)
    


@app.route('/<short_code>')
def redirect_to_original(short_code):
    result = url_database.fetch_mapped_url(short_code)
    if result is not None:
        original_url = result[0]
        return redirect(original_url)
    else:
        return "Invalid URL"

@app.route('/old_links')
def show_old_links():
    data = url_database.show_stored_url()
    return render_template('old_links.html', data = data)


@app.route('/old_links', methods = ["POST"])
def delete_all_links():
    if request.method == "POST":
        url_database.delete_url()
    return redirect('/old_links')

def generate_short_code():
    # Generate a random 6-character short code using uppercase letters, lowercase letters, and digits
    characters = string.ascii_letters + string.digits
    short_code = ''.join(random.choices(characters, k=6))
    return short_code


@app.teardown_appcontext
def close_db(error):
    url_database.close_db()

if __name__ == '__main__':
    app.run(debug=True)

import url_database

from flask import Flask, request
from flask import Flask, render_template, redirect, url_for, session

from slugify import slugify


app = Flask(__name__)


@app.route('/', methods = ["GET", "POST"])
def index():
    the_url = request.form.get('input')
    if request.method == "POST":
        result = generate_url(the_url)
        return render_template("index.html", result=result)
    elif request.method == "GET":
        return render_template("index.html", result=None)
    

def generate_url(url):
    slug = slugify(url)
    url_database.add_url(url, slug)
    return slug


if __name__ == '__main__':
    app.run(debug=True)

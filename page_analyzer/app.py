import os
import psycopg2
from page_analyzer.db import URLsRepository
from  page_analyzer.validate import validate

from dotenv import load_dotenv
from flask import Flask, flash, get_flashed_messages, render_template, request, redirect, url_for
from urllib.parse import urlparse

load_dotenv("secret.env")

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

@app.route('/')
def index():

    return render_template('index.html')

@app.post('/urls')
def post_urls():

    repo = URLsRepository()
    data = request.form.get('url')
    data = 'https://' + urlparse(data).netloc
    errors = validate(data)
    if errors:
        flash(errors, 'danger')
        messages = get_flashed_messages(with_categories=True)
        return render_template("index.html", url=data, messages=messages), 422
    
    new_id = repo.save(data)
    flash("Страница успешно добавлена", "success")
    return redirect(url_for("get_url", id=new_id))

@app.route('/urls/<id>')
def get_url(id):

    messages = get_flashed_messages(with_categories=True)
    repo = URLsRepository()
    url = repo.check_url_by_id(id)[0]
    return render_template('urls/show.html', url=url, messages=messages,)

@app.get('/urls')
def get_urls():

    repo = URLsRepository()
    urls = [dict(row) for row in repo.get_all()]
    return render_template('urls/show_all.html', urls=urls,)
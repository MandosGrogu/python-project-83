import os
import requests

from page_analyzer.db import URLsRepository
from page_analyzer.preprocess import url_parse
from page_analyzer.preprocess import html_parse
from page_analyzer.validate import validate
from dotenv import load_dotenv
from flask import abort, Flask, flash, get_flashed_messages, render_template, request, redirect, url_for

load_dotenv("secret.env")

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

@app.route('/')
async def index():

    return render_template('index.html')

@app.post('/urls')
async def post_urls(save=URLsRepository().save):

    repo = URLsRepository()
    data = request.form.get('url')
    errors = validate(data)
    if errors:
        flash(errors, 'danger')
        messages = get_flashed_messages(with_categories=True)
        return render_template("index.html", url=data, messages=messages), 422
    data = url_parse(data)
    existed_data = await repo.check_url_by_name(data)
    if not existed_data:
        new_id = await save(data)
        flash("Страница успешно добавлена", "success")
    else:
        new_id = existed_data
        flash("Страница уже существует", 'info')
    return redirect(url_for("get_url", id=new_id['id']))

@app.route('/urls/<id>')
async def get_url(id):

    messages = get_flashed_messages(with_categories=True)
    repo = URLsRepository()
    existed_data = await repo.check_url_by_id(id)
    if not existed_data:
        abort(404)
    else:
        url = existed_data
    return render_template('urls/show.html', url=url, messages=messages,)

@app.get('/urls')
async def get_urls():

    repo = URLsRepository()
    urls = await repo.get_all()
    return render_template('urls/show_all.html', urls=urls,)

@app.post('/urls/<id>')
async def post_check(id):

    repo = URLsRepository()
    existed_data = await repo.check_url_by_id(id)
    if not existed_data:
        abort(404)
    else:
        url = existed_data
    try:
        r = requests.get(url['name'])
        r.raise_for_status()
        status_code = r.status_code
        result = html_parse(r.text)
        h1 = result['h1']
        title = result['title']
        descr = result['descr']
        await repo.save_check(url, status_code, h1, title, descr)
        flash('Страница успешно проверена', 'success')
        errors = ''
    except Exception as e:
        errors = f'{e}'
    if errors:
        flash('Произошла ошибка при проверке', 'danger')
    messages = get_flashed_messages(with_categories=True)
    check_urls = await repo.get_all_checks(id)
    return render_template('urls/show.html', url=url, check_urls=check_urls, messages=messages,)
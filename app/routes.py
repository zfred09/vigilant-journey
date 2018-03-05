from flask import render_template, flash, redirect, url_for
from app import app, db
from app.forms import LoginForm
from app.models import Recipes, Ingredients
from pyqrcode import pyqrcode
import io

@app.route('/')
@app.route('/index')
def index():
    recipe_id = 2
    title = Recipes.query.filter_by(id=recipe_id).first()
    ingredients = Ingredients.query.filter_by(recipe_id=recipe_id)

    return render_template('index.html', title=title, ingredients=ingredients)

# to-do - add error handling
@app.route('/recipes/<recipe_id>')
def recipes(recipe_id):
    recipe = Recipes.query.filter_by(id=recipe_id).first_or_404()
    ingredients = Ingredients.query.filter_by(recipe_id=recipe_id)

    return render_template('index.html', recipe=recipe, ingredients=ingredients)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
            flash('Login requested for user {}, remember_me={}'.format(
                form.username.data, form.remember_me.data))
            return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/qrcode')
def qrcode():
    # render qrcode
    url = pyqrcode.create('http://google.com')
    stream = io.BytesIO()
    url.svg(stream, scale=5)
    return stream.getvalue(), 200, {
        'Content-Type': 'image/svg+xml',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'}

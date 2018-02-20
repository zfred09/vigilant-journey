from flask import render_template, flash, redirect, url_for
from app import app, db
from app.forms import LoginForm
from app.models import Recipes, Ingredients

@app.route('/')
@app.route('/index')
def index():
    recipe_id = 2
    title = Recipes.query.filter_by(id=recipe_id).first()
    ingredients = Ingredients.query.filter_by(recipe_id=recipe_id)

    return render_template('index.html', title=title, recipe=recipe_id, ingredients=ingredients)

# to-do - add error handling
@app.route('/recipes/<recipe>')
def recipes(recipe):
    title = Recipes.query.filter_by(id=recipe).first_or_404()
    ingredients = Ingredients.query.filter_by(recipe_id=recipe)

    return render_template('index.html', title=title, recipe=recipe, ingredients=ingredients)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
            flash('Login requested for user {}, remember_me={}'.format(
                form.username.data, form.remember_me.data))
            return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

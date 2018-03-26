from flask import render_template, flash, redirect, url_for, request, session, escape
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


# todo - add error handling
@app.route('/recipes/<recipe_id>')
def recipes(recipe_id):
    recipe = Recipes.query.filter_by(id=recipe_id).first_or_404()
    ingredients = Ingredients.query.filter_by(recipe_id=recipe_id)

    return render_template('index.html', recipe=recipe, ingredients=ingredients)


# todo - add error handling
@app.route('/recipeCardList/<int:setLimit>')
def recipeCardList(setLimit):
    # todo create a sliding window of results
    recipe = Recipes.query.limit(setLimit).all()

    return render_template('recipeCard.html', recipe=recipe)

@app.route('/addToList/<recipe_id>')
def addToList(recipe_id):
    recipe = Recipes.query.filter_by(id=recipe_id).first_or_404()
    ingredients = Ingredients.query.filter_by(recipe_id=recipe_id)

    for i in ingredients:
        session['myList'].append(str(i.quantity) + " " + i.ingredient)

    flash(recipe.title + " added to list")

    return render_template('index.html', recipe=recipe, ingredients=ingredients)

@app.route('/newList')
def newList():
    session['myList'].clear()
    flash('New list started')

    # Todo - eventually add some ability to create names or different lists here
    return render_template('viewList.html', myList=session['myList'])

@app.route('/viewList')
def viewList():
    # todo - escape this output?
    return render_template('viewList.html', myList=session['myList'])

@app.route('/clearList')
def clearList():
    session['myList'].clear()
    flash('List cleared')
    return render_template('viewList.html', myList=session['myList'])


@app.route('/qrcode/<targetRecipeId>')
def qrcode(targetRecipeId):
    # render qrcode
    targetURL = request.url_root + "recipes/" + targetRecipeId
    url = pyqrcode.create(targetURL)
    stream = io.BytesIO()
    url.svg(stream, scale=5)
    return stream.getvalue(), 200, {
        'Content-Type': 'image/svg+xml',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'}

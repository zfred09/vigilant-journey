from datetime import datetime
from app import db

class Recipes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), index=True)
    prep_time = db.Column(db.Integer)
    cook_time_min = db.Column(db.Integer)

    # backref sets the virtual field name for Ingredients' recipe_id field
    ingredients = db.relationship('Ingredients', backref='ingredients', lazy='dynamic')

    def get_ingredients(recipe_id):
        print(recipe_id)
        return Ingredients.query.filter_by(ingredients=recipe_id)

    # Tells Python how to print objects of this class - for debugging
    #def __repr__(self):
     #   return '<Recipes {}>'.format(self.title)

class Ingredients(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ingredient = db.Column(db.String(70))
    quantity = db.Column(db.String(15))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))

    # Tells Python how to print objects of this class - for debugging
    def __repr__(self):
        return '<Ingredients {} - {} - {}>'.format(self.ingredient, self.quantity, self.recipe_id)
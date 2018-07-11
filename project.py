from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Items

app = Flask(__name__)

engine = create_engine('sqlite:///item_catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
def home():
    category = session.query(Category).first()
    items = session.query(Items).filter_by(category_id=Category.id)
    return render_template('catalog.html', category=category, items=items)



@app.route('/category/<int:category_id>/')
def ShowCategory():
    category = session.query(Category).first()
    items = session.query(Items).filter_by(category_id=Category.id)
    return render_template('catalog.html', category=category, items=items)



@app.route('/category/<int:category_id>/new/', methods=['GET', 'POST'])
def newItem(category_id):
    if request.method == 'POST':
        newItem = Items(
            name=request.form['name'], category_id=category_id)
        session.add(newItem)
        session.commit()
        return redirect(url_for('home', category_id=category_id))
    else:
        return render_template('newitem.html', category_id=category_id)




@app.route('/category/<int:category_id>/<int:cat_id>/edit/', methods=['GET', 'POST'])
def editItem(category_id, cat_id):
    editedItem = session.query(Items).filter_by(id=cat_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('home', category_id=category_id))
    else:
        render_template('editItem', category_id=category_id, item=editedItem)

@app.route('/category/<int:category_id>/delete/')
def deleteItem(category_id):
    return "to delete items"





if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

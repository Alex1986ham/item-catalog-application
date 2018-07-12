from flask import Flask, render_template, request, redirect, url_for, flash
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


@app.route('/')
@app.route('/category/<int:category_id>/items')
def ShowCategory(category_id):
    category = session.query(Category).first()
    items = session.query(Items).filter_by(category_id=Category.id)
    return render_template('catalog.html', category=category, items=items, category_id=category_id)




@app.route('/category/<int:category_id>/new/', methods=['GET', 'POST'])
def newItem(category_id):
    if request.method == 'POST':
        newItem = Items(
            name=request.form['name'], category_id=category_id)
        session.add(newItem)
        session.commit()
        session.close()
        flash("new item created!")
        return redirect(url_for('ShowCategory', category_id=category_id))
    else:
        return render_template('newitem.html', category_id=category_id)




@app.route('/category/<int:category_id>/<int:items_id>/edit/', methods=['GET', 'POST'])
def editItem(category_id, items_id):
    editedItem = session.query(Items).filter_by(id=items_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        session.add(editedItem)
        session.commit()
        session.close()
        flash("Item has benn edited")
        return redirect(url_for('ShowCategory', category_id=category_id))
    else:
        return render_template('edititem.html', category_id=category_id, items_id=items_id, item=editedItem)



@app.route('/category/<int:category_id>/<int:items_id>/delete/', methods=['GET', 'POST'])
def deleteItem(category_id, items_id):
    itemtoDelete = session.query(Items).filter_by(id=items_id).one()
    if request.method == 'POST':
        session.delete(itemtoDelete)
        session.commit()
        session.close()
        flash("Item has been deleted")
        return redirect(url_for('ShowCategory', category_id=category_id))
    else:
        return render_template('deleteitem.html', item=itemtoDelete)




if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

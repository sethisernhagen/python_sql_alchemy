from flask import Flask, flash, jsonify, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('postgres:///restaurantmenu')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menu_item_JSON(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id = menu_id).one()
    return jsonify(item.serialize)

@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('menu.html', restaurant=restaurant, items=items)

@app.route('/restaurants/<int:restaurant_id>/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(name = request.form['name'], restaurant_id = restaurant_id)
        session.add(newItem)
        session.commit()
        flash("new menu item created!")
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:
        return render_template('new_menu_item.html', restaurant_id = restaurant_id)

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit', methods=['GET', 'Post'])
def editMenuItem(restaurant_id, menu_id):
    if request.method == 'POST':
        newName = request.form['name']
        item = session.query(MenuItem).filter_by(id=menu_id).one()
        item.name = newName
        flash("menu item edited!")
        session.commit()
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:
        restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
        item = session.query(MenuItem).filter_by(id=menu_id).one()
        return render_template('edit_menu_item.html', restaurant=restaurant, menu_item=item)

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    menu_item = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(menu_item)
        flash("menu item deleted!")
        session.commit()
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:
        return render_template('delete_menu_item.html', item=menu_item)

    return "page to delete a menu item. Task 3 complete!"

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
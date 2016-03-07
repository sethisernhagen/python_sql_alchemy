from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('postgres:///restaurantmenu')

Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

# restaurants = session.query(Restaurant).all()
session.query(MenuItem).delete()
session.query(Restaurant).delete()
session.commit()

myFirstRestaurant = Restaurant(name = "Pizza Palace")

session.add(myFirstRestaurant)
session.commit()

cheesePizza = MenuItem(name = "Cheese Pizza",
  description = "Made with cheese",
  course = "Entree",
  price = "$8.99",
  restaurant = myFirstRestaurant)

session.add(cheesePizza)
session.commit()
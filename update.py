from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('postgres:///restaurantmenu')

Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

veggieBurgers = session.query(MenuItem).filter_by(name = 'Veggie Burger')

for veggieBurger in veggieBurgers:
  print(veggieBurger.id)
  print(veggieBurger.price)
  print(veggieBurger.restaurant.name)
  print("\n")


# get urban veggie burger
urbanVeggieBurger = session.query(MenuItem).filter_by(id = 12).one()
urbanVeggieBurger.price = '$2.99'
session.commit()

for veggieBurger in veggieBurgers:
  print(veggieBurger.id)
  print(veggieBurger.price)
  print(veggieBurger.restaurant.name)
  print("\n")
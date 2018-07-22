from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Items, User

# Create database and create a shortcut for easier to update database
engine = create_engine('sqlite:///item_catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

category1 = Category(user_id=1, name="Indoor Furniture")
session.add(category1)
session.commit()

items1 = Items(user_id=1, name="Livingroom Sofa", description="Perfect Sofa for your livingroom",
                price="399", category_id=2)

user1 = User(name="Alexander Dudko", email="alexander.dudko@eufh.de", picture='https://scontent-ams3-1.xx.fbcdn.net/v/t1.0-9/390888_280097078716240_2049534995_n.jpg?_nc_cat=0&oh=d149bbd571d0000f9551bdc17b180407&oe=5BDD1FCF')
session.add(user1)
session.commit()

session.add(items1)
session.commit()

print ("added category and items!")

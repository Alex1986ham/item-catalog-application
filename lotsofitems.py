from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Items

# Create database and create a shortcut for easier to update database
engine = create_engine('sqlite:///item_catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

category1 = Category(name="Indoor Furniture")
session.add(category1)
session.commit()

items1 = Items(name="Livingroom Sofa", description="Perfect Sofa for your livingroom",
                price="399", category_id=2)
session.add(items1)
session.commit()

print ("added category and items!")

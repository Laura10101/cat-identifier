from flask_sqlalchemy import SQLAlchemy

#Declare the db in database.py to avoid circular references
#Taken from:
#https://stackoverflow.com/questions/22929839/circular-import-of-db-reference-using-flask-sqlalchemy-and-blueprints
db = SQLAlchemy()
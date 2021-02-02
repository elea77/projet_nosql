from flask import Flask
from flask_pymongo import pymongo
from app import app


CONNECTION_STRING = "mongodb+srv://NoSql:bobo@cluster0.mya65.mongodb.net/NoSql?retryWrites=true&w=majority"

client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('nosql_db')

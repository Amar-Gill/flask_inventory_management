import peeweedbevolve
from flask import Flask, render_template, request
from models import db, Store
app = Flask(__name__)

@app.before_request
def before_request():
   db.connect()

@app.after_request
def after_request(response):
   db.close()
   return response

@app.cli.command()
def migrate():
   db.evolve(ignore_tables={'base_model'})

@app.route("/")
def index():
   return render_template('index.html')

@app.route("/store", methods=["GET"])
def store_get():
   return render_template("store.html")

@app.route("/store", methods=["POST"])
def store_post():
   print(request.form)
   store = request.form['store']
   Store.create(name = store)
   return render_template("store.html", store=store)

if __name__ == '__main__':
   app.run()
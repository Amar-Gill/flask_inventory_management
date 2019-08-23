import peeweedbevolve
from flask import Flask, render_template, request, redirect, flash
from models import db, Store, Warehouse
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

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
def home():
   return render_template('index.html')

@app.route("/store", methods=["GET"])
def new_store():
   return render_template("store.html")

@app.route("/warehouse", methods=["GET"])
def new_warehouse():
   stores = Store.select()
   return render_template("warehouse.html", stores=stores)

@app.route("/store", methods=["POST"])
def create_store():
   print(request.form)
   store = Store(name = request.form['store'])
   if store.save():
      flash( store.name + ' was successfully saved!')
      return redirect('/store')
   else:
      return render_template("store.html", name=request.form['store'])

@app.route("/warehouse", methods=["POST"])
def create_warehouse():
   print(request.form)
   store = Store.get_by_id(request.form['store_id'])
   warehouse = Warehouse(location = request.form['location'], store=store)
   if warehouse.save():
      flash('Warehouse ' + str(warehouse.id) + ' was successfully saved!')
      return redirect('/warehouse')
   else:
      return render_template("warehouse.html", location=request.form['location'])

if __name__ == '__main__':
   app.run()
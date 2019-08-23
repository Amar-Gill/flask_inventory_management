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

@app.route("/new_store", methods=["GET"])
def new_store():
   return render_template("new_store.html")

@app.route("/new_warehouse", methods=["GET"])
def new_warehouse():
   stores = Store.select()
   return render_template("new_warehouse.html", stores=stores)

@app.route("/stores", methods=["GET"])
def index_stores():
   stores = Store.select()
   return render_template("index_stores.html", stores=stores)

@app.route("/store/<store_id>", methods=["GET"])
def edit_store(store_id):
   store = Store.get_or_none(Store.id == store_id)
   if store:
      return render_template('show_store.html', store = store)
   else:
      return redirect('/stores')

@app.route("/store/<store_id>", methods=["POST"])
def update_store(store_id):
   name = request.form['name']
   newname = Store.update(name = name).where(Store.id == store_id)
   newname.execute()
   flash('Store name updated!')
   return redirect(f'/store/{store_id}')

@app.route("/new_store", methods=["POST"])
def create_store():
   print(request.form)
   store = Store(name = request.form['store'])
   if store.save():
      flash( store.name + ' was successfully saved!')
      return redirect('/new_store')
   else:
      return render_template("new_store.html", name=request.form['store'])

@app.route("/new_warehouse", methods=["POST"])
def create_warehouse():
   print(request.form)
   store = Store.get_by_id(request.form['store_id'])
   warehouse = Warehouse(location = request.form['location'], store=store)
   if warehouse.save():
      flash('Warehouse ' + str(warehouse.id) + ' was successfully saved!')
      return redirect('/new_warehouse')
   else:
      return render_template("new_warehouse.html", location=request.form['location'], store=store)

if __name__ == '__main__':
   app.run()
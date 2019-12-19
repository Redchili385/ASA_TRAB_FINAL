from flask import Flask, request, render_template, redirect, session, flash, url_for, abort, jsonify, json
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, text, select, ForeignKey, exc
from flask_bootstrap import Bootstrap
from flask_cors import CORS, cross_origin
from dbutils import *
from json import dumps
import psycopg2

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


class User:
    def __init__(self, name, password, email):
        self.name = name
        self.password = password
        self.email = email

class Product:
    def __init__(self, Id, name, price, text, urlImage):
        self.id = Id
        self.name = name
        self.price = price
        self.text = text
        self.urlImage = urlImage

products = []
users = []

def exportProductstoBD():
    products = []
    products.append(Product(0,"IphoneX","5999.99","IphoneX text","iphoneX.jpg"))
    products.append(Product(1,"Galaxy S10+","3999.99","Galaxy S10+ text","Galaxy_S10+.jpg"))
    products.append(Product(2,"Huawei P30 Pro","3500.00","Huawei P30 Pro Text","Huawei_P30.jpg"))
    products.append(Product(3,"Moto G8 Plus","1999.99","Moto G8 text","MotoG8.jpg"))
    products.append(Product(4,"Xiaomi Mi9", "2299.99", "Xiaomi Mi9", "XiaomiMi9.jpg"))
    products.append(Product(5,"Alcatel Pixi 4","186.90","Alcatel Pixi 4 text","AlcatelPixi4.jpg"))
    dbUtils = DbUtils()
    dbUtils.createTableProducts()  #Table products
    for product in products:
        dbUtils.addNewProduct(product.name, product.price, product.text, product.urlImage)

def importProductsFromBD():
    products = []
    dbUtils = DbUtils()
    productsBD = dbUtils.selectProducts()
    #while(product):
    if(productsBD):
        for product in productsBD:
            products.append(Product(product[0],product[1],product[2],product[3],product[4]))
            print(product)
    print(products)
    return products

if(not importProductsFromBD()):
    exportProductstoBD()
    

@app.route('/index.html')
def index():
    return render_template("index.html")

@app.route("/about.html")
def about():
    return render_template("about.html")

@app.route("/cadastro.html")
def cadastro():
    return render_template("cadastro.html")

@app.route("/login.html")
def login():
    return render_template("login.html")

@app.route("/logar", methods=['POST'])
def logar():
    print(request.form)
    print(request.form['password'])
    print(request.form['email'])
    password = request.form['password']
    email = request.form['email']
    dbUtils = DbUtils()
    res = dbUtils.selectUsers(email,password)
    if(res):
        print(res)
        userReturn = None
        for user in res:
            userReturn = user
            print(user)
        if(userReturn == None):
            return json.dumps({'message':'Usuário ou senha incorretos','username':''})
    else:
        return json.dumps({'message':'Erro ao logar','username':''})
    return json.dumps({'message':'Bem vindo','username':userReturn[1]})

@app.route("/cadastrar", methods=['POST'])
def cadastrar():
    #global users
    print(request.form)
    #user_data = request.get_json(force=True)
    #print(user_data)
    print(request.form['name'])
    print(request.form['password'])
    print(request.form['email'])
    newUser = User(request.form['name'],request.form['password'],request.form['email'])
    users.append(newUser)
    dbUtils = DbUtils()
    dbUtils.createTableUsers()
    #for user in users:
    dbUtils.addNewUser(newUser.name, newUser.password, newUser.email)
    return json.dumps({'cadastrado':'1'})

@app.route("/loadAllProducts", methods=['GET'])
@cross_origin()
def loadAllProducts():
    products = importProductsFromBD()
    myDictObj = []
    for product in products:
        myDictObj.append({"name":product.name,"price":product.price,"text":product.text,"urlImage":product.urlImage})
    serialized = json.dumps(myDictObj)
    print(serialized)
    return (serialized)

@app.route("/loadProduct", methods=['GET'])
@cross_origin()
def loadProduct():
    products = importProductsFromBD()
    product_id = request.args['product_id']
    product = products[int(product_id)]
    myDictObj = [{"name":product.name,"price":product.price,"text":product.text,"urlImage":product.urlImage}]
    serialized = json.dumps(myDictObj)
    print(serialized)
    return (serialized)
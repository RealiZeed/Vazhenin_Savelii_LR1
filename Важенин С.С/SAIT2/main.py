
from random import randrange
import telebot
import php

bot = telebot.TeleBot('5884879874:AAH7racX2Z8lUnGbWI1cuDZyWU8fKG2Ajpk')

from flask import Flask, request, render_template, send_from_directory, make_response, current_app, jsonify, redirect, \
url_for
from werkzeug.security import generate_password_hash, check_password_hash
import json

import pymysql
app = Flask(__name__)

host='127.0.0.1'
user='root'
passwrd='root'
database='oknada'

zayavka = ''

@app.route('/cookie/')
def cookie(user_id):
    if not request.cookies.get('id'):
        res = make_response("Setting a cookie")
        res.set_cookie('id', user_id, max_age=None)
    else:
        res = make_response("Value of cookie foo is {}".format(request.cookies.get('id')))
    return res

@app.route("/")
def index_page():
    if request.cookies.get('id') != None:
        conn = pymysql.connect(host = host, user = user, password = passwrd, database = database, port = 3306)
        cursor = conn.cursor()

        cursor.execute("SELECT Name FROM users WHERE ID = '" + str(request.cookies.get('id')) + "'")
        name = cursor.fetchone()[0]
        data = {'username': name}

        return render_template("index.html", data=data)
    else:
        data = {'username': "None"}

        return render_template("index.html", data = data)

@app.route("/examples")
def examples_page():
    conn = pymysql.connect(host = host, user = user, password = passwrd, database = database, port = 3306)
    cursor = conn.cursor()

    cursor.execute("SELECT Name FROM users WHERE ID = '" + str(request.cookies.get('id')) + "'")
    name = cursor.fetchone()[0]
    data = None
    if name != None:
        data = {'username': name}
    else:
        data = {'username': 'None'}
    return render_template("newindex.html", data=data)

@app.route("/services")
def services_page():
    conn = pymysql.connect(host = host, user = user, password = passwrd, database = database, port = 3306)
    cursor = conn.cursor()

    cursor.execute("SELECT Name FROM users WHERE ID = '" + str(request.cookies.get('id')) + "'")
    name = cursor.fetchone()[0]
    data = None
    if name != None:
        data = {'username': name}
    else:
        data = {'username': 'None'}
    return render_template("newindex2.html", data=data)

@app.route("/register", methods=['GET', 'POST'])
def register():
    conn = pymysql.connect(host = host, user = user, password = passwrd, database = database, port=3306)
    cursor = conn.cursor()

    login = request.form.get('login')
    password = request.form.get('password')

    password_hash = generate_password_hash(password)

    success = False

    if userExists(login):
        print("Этот пользователь уже существует")
    else:
        cursor.execute(
            "INSERT INTO users (ID, Name, Login, Password) VALUES (" + str(
                randrange(9999)) + ", '" + login + "', '" + login + "', '" + password_hash + "')")
        conn.commit()
        success = True
    conn.close()
    return str(success)

@app.route("/send_zayavka", methods=['GET', 'POST'])
def send_zayavka():
    print ('xyi')
    name = request.form.get('zname')
    print (name)
    num = request.form.get('znum')
    home = request.form.get('zhome')
    mail = request.form.get('zmail')

    zayavka = 'Новая заяка:'
    zayavka += f'\nФИО: {name}'
    zayavka += f'\nНомер: {num}'
    zayavka += f'\nДомашний адрес: {home}'
    zayavka += f'\nЭлектронная почта: {mail}'
    bot.send_message(987797704, text = zayavka)


def doCookies(user_id):
    res = make_response(url_for("index_page"))
    print(str(res) + " -- " + str(user_id))
    res.set_cookie('id', str(user_id), max_age=None)
    return res


@app.route("/login", methods=['GET', 'POST'])
def login():
    conn = pymysql.connect(host = host, user = user, password = passwrd, database = database, port=3306)
    cursor = conn.cursor()

    login = request.form.get('login')
    password = request.form.get('password')

    if userExists(login):
        if passCorrect(login, password):
            cursor.execute("SELECT ID FROM users WHERE Login = '" + str(login) + "'")
            user_id = cursor.fetchone()[0]

            res = make_response(url_for("index_page"))
            res.set_cookie('id', str(user_id), max_age=None)

            print(request.cookies.get('id'))
            print("Пользователь id" + str(user_id) + " авторизовался")
            conn.close()
            return res
        else:
            print("Неверный пароль")
    else:
        print("Пользователь не существует")

    conn.close()
    return "False"




def passCorrect(user_login, password):
    conn = pymysql.connect(host = host, user = user, password = passwrd, database = database, port=3306)
    cursor = conn.cursor()

    correct = False

    cursor.execute("SELECT Password FROM users WHERE Login = '" + user_login + "'")
    password_hash = cursor.fetchone()[0]

    if check_password_hash(password_hash, password):
        correct = True

    conn.close()
    return correct


def userExists(user_login):
    conn = pymysql.connect(host = host, user = user, password = passwrd, database = database, port=3306)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE Login = '" + str(user_login) + "'")
    exist = cursor.fetchone()
    if exist is None:
        conn.close()
        return False
    else:
        conn.close()
        return True

@app.route("/signin")
def display_reg():
    return render_template("register.html")


@app.route("/auth")
def display_login():
    return render_template("login.html")


app.run()
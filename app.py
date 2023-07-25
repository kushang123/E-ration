from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import login_required
from flask_mysqldb import MySQL
import MySQLdb.cursors
import app
import numpy as np
import pandas as pd

app = Flask(__name__)
app.secret_key = 'AAbb'
app.debug = True

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'Ration'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    msg = ''
    if request.method == 'POST' and 'uname' in request.form and 'password' in request.form:
        uname = request.form['uname']
        pas = request.form['password']
        option = request.form['utype']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM login WHERE Username = %s AND Pass = %s', (uname, pas))
        account = cursor.fetchone()
        a = ["shop1", "shop2", "shop3", "shop4"]

        if account:
            if option == '1':
                if uname not in a:
                    session['cardholder'] = True
                    session['uname'] = account['Username']
                    session['password'] = account['Pass']
                    return redirect(url_for("cardholder", uid=session["password"]))
            elif option == '2':
                if uname in a:
                    session['shopkeeper'] = True
                    session['uname'] = account['Username']
                    session['password'] = account['Pass']
                    return redirect(url_for("shopkeeper"))
            elif option == '3':
                if uname == 'admin':
                    session['admin'] = True
                    session['uname'] = account['Username']
                    session['password'] = account['Pass']
                    return render_template('admin.html')
            else:
                return render_template('login.html', msg=msg)

        else:
            msg = 'Incorrect username/password!'
    return render_template('login.html', msg=msg)


@app.route('/cardholder/<uid>')
def cardholder(uid):
    if 'cardholder' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT Full_Name FROM cardholder WHERE Card_Number=%s', (uid,))
        name = cursor.fetchone()
        cursor.close()
        name = name["Full_Name"]
        return render_template("cardholder.html", name=name)
    return redirect(url_for('login'))

@app.route('/shopkeeper', methods=["GET", "POST"])
def shopkeeper():
    if 'shopkeeper' in session:
        shop = session["uname"]
        l_no = session["password"]
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT Full_Name FROM cardholder WHERE Card_Number=%s', (l_no,))
        name = cursor.fetchone()
        cursor.close()
        name = name["Full_Name"]
        if request.method == 'POST':
            if shop == "shop1":
                option = request.form['stock']
                update_qty = request.form['qty']
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('select Qty from shop1 where Items=%s', (option,))
                old_qty = cursor.fetchone()
                old_qty = old_qty["Qty"]
                cursor.execute('UPDATE shop1 SET Qty= %s+%s WHERE Items= %s', (old_qty, update_qty, option))
                mysql.connection.commit()
                cursor.close()
            elif shop == "shop2":
                option = request.form['stock']
                update_qty = request.form['qty']
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('select Qty from shop2 where Items=%s', (option,))
                old_qty = cursor.fetchone()
                old_qty = old_qty["Qty"]
                cursor.execute('UPDATE shop2 SET Qty= %s+%s WHERE Items= %s', (old_qty, update_qty, option))
                mysql.connection.commit()
                cursor.close()
            elif shop == "shop3":
                option = request.form['stock']
                update_qty = request.form['qty']
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('select Qty from shop3 where Items=%s', (option,))
                old_qty = cursor.fetchone()
                old_qty = old_qty["Qty"]
                cursor.execute('UPDATE shop3 SET Qty= %s+%s WHERE Items= %s', (old_qty, update_qty, option))
                mysql.connection.commit()
                cursor.close()
            elif shop == "shop4":
                option = request.form['stock']
                update_qty = request.form['qty']
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('select Qty from shop4 where Items=%s', (option,))
                old_qty = cursor.fetchone()
                old_qty = old_qty["Qty"]
                cursor.execute('UPDATE shop4 SET Qty= %s+%s WHERE Items= %s', (old_qty, update_qty, option))
                mysql.connection.commit()
                cursor.close()

        return render_template("shopkeeper.html", name=name, uid=l_no)

    return redirect(url_for('login'))

@app.route('/order/shop1', methods=["POST", "GET"])
def shop1():
    if 'cardholder' in session:

        contact = session["uname"]
        card_number = session["password"]
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * from shop1')
        d = cursor.fetchall()
        cursor.execute('SELECT Full_Name FROM cardholder WHERE Card_Number=%s', (card_number,))
        name = cursor.fetchone()
        cursor.close()
        name = name["Full_Name"]
        if request.method == "POST":
            option = request.form['option']
            quantity = request.form['qty']


            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('Update shop1 set Qty=qty-%s WHERE Items=%s', (quantity, option))
            mysql.connection.commit()
            cursor.close()
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * from shop1')
            d = cursor.fetchall()
            cursor.execute('SELECT Full_Name FROM cardholder WHERE Card_Number=%s', (card_number,))
            name = cursor.fetchone()
            cursor.close()

            shop = 'shop1'
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO orderhist (username,Item,qty,shop) VALUES (%s,%s,%s,%s)',
                           (card_number, option, quantity, shop))
            mysql.connection.commit()
            cursor.close()

            name = name["Full_Name"]
        return render_template("shop1.html", d=d, name=name)


@app.route('/order/shop2', methods=["POST", "GET"])
def shop2():
    if 'cardholder' in session:
        contact = session["uname"]
        card_number = session["password"]
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * from shop2')
        d = cursor.fetchall()
        cursor.execute('SELECT Full_Name FROM cardholder WHERE Card_Number=%s', (card_number,))
        name = cursor.fetchone()
        cursor.close()
        name = name["Full_Name"]
        if request.method == "POST":
            option = request.form['option']
            quantity = request.form['qty']


            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('Update shop2 set Qty=qty-%s WHERE Items=%s', (quantity, option))
            mysql.connection.commit()
            cursor.close()
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * from shop2')
            d = cursor.fetchall()
            cursor.execute('SELECT Full_Name FROM cardholder WHERE Card_Number=%s', (card_number,))
            name = cursor.fetchone()
            cursor.close()

            shop = 'shop2'
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO orderhist (username,Item,qty,shop) VALUES (%s,%s,%s,%s)',
                           (card_number, option, quantity, shop))
            mysql.connection.commit()
            cursor.close()

            name = name["Full_Name"]

        return render_template("shop2.html", d=d, name=name)


@app.route('/order/shop3', methods=["POST", "GET"])
def shop3():
    if 'cardholder' in session:
        contact = session["uname"]
        card_number = session["password"]
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * from shop3')
        d = cursor.fetchall()
        cursor.execute('SELECT Full_Name FROM cardholder WHERE Card_Number=%s', (card_number,))
        name = cursor.fetchone()
        cursor.close()
        name = name["Full_Name"]
        if request.method == "POST":
            option = request.form['option']
            quantity = request.form['qty']


            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('Update shop3 set Qty=qty-%s WHERE Items=%s', (quantity, option))
            mysql.connection.commit()
            cursor.close()
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * from shop3')
            d = cursor.fetchall()
            cursor.execute('SELECT Full_Name FROM cardholder WHERE Card_Number=%s', (card_number,))
            name = cursor.fetchone()
            cursor.close()

            shop = 'shop3'
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO orderhist (username,Item,qty,shop) VALUES (%s,%s,%s,%s)',
                           (card_number, option, quantity, shop))
            mysql.connection.commit()
            cursor.close()

            name = name["Full_Name"]
        return render_template("shop3.html", d=d, name=name)


@app.route('/order/shop4', methods=["POST", "GET"])
def shop4():
    if 'cardholder' in session:
        contact = session["uname"]
        card_number = session["password"]
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * from shop4')
        d = cursor.fetchall()
        cursor.execute('SELECT Full_Name FROM cardholder WHERE Card_Number=%s', (card_number,))
        name = cursor.fetchone()
        cursor.close()
        name = name["Full_Name"]
        if request.method == "POST":
            option = request.form['option']
            quantity = request.form['qty']


            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('Update shop4 set Qty=qty-%s WHERE Items=%s', (quantity, option))
            mysql.connection.commit()
            cursor.close()
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * from shop4')
            d = cursor.fetchall()
            cursor.execute('SELECT Full_Name FROM cardholder WHERE Card_Number=%s', (card_number,))
            name = cursor.fetchone()
            cursor.close()

            shop = 'shop4'
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO orderhist (username,Item,qty,shop) VALUES (%s,%s,%s,%s)',
                           (card_number, option, quantity, shop))
            mysql.connection.commit()
            cursor.close()

            name = name["Full_Name"]
        return render_template("shop4.html", d=d, name=name)


@app.route('/orderhistory')
def history():
    if 'cardholder' in session:
        contact = session["uname"]
        card_number = session["password"]
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT Item,qty,shop from orderhist where username= %s ', (card_number,))
        d = cursor.fetchall()
        cursor.close()
        return render_template('orderhistory.html', d=d)


@app.route('/orderhistory/back', methods=["POST", "GET"])
def historyback():
    if 'cardholder' in session:
        if request.method == "POST":
            return redirect(url_for("cardholder", uid=session["password"]))

@app.route('/pendingorders')
def pendinorders():
    if 'shopkeeper' in session:
        return render_template("pendingorders.html")

@app.route('/pendingorders/back', methods=["POST", "GET"])
def pendingback():
    if 'shopkeeper' in session:
        if request.method == "POST":
            return redirect(url_for("shopkeeper", uid=session["password"]))

@app.route('/logout')
def logout():
    session.pop('cardholder', None)
    session.pop('uname', None)
    session.pop('password', None)
    return redirect(url_for('index'))


@app.route('/logout/shop')
def logout_shop():
    session.pop('shopkeeper', None)
    session.pop('uname', None)
    session.pop('password', None)
    return redirect(url_for('index'))

@app.route('/ask')
def ask():
    return render_template('ASK.html')


if __name__ == '__main__':
    app.run(debug=True)
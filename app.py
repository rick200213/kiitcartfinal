from typing import List, Any

from flask import Flask, render_template, request, redirect, session, jsonify
import re
import pymysql

app = Flask(__name__)
app.secret_key = 'your secret key'


@app.route('/')
def index():
    con = pymysql.connect(host='localhost', user='root', passwd='Account1start', database='ecommerce1')
    print('connection sucessful')
    con1 = pymysql.connect(host='localhost', user='root', passwd='Account1start', database='ecommerce1')
    cur = con.cursor()
    cur1 = con1.cursor()
    str = "select * from  product"
    str1 = "select * from featuredproduct"
    cur.execute(str)
    cur1.execute(str1)
    row_headers = [x[0] for x in cur.description]  # this will extract row headers
    frow_headers = [y[0] for y in cur1.description]  # this will extract row headers
    rv = cur.fetchall()
    rv1 = cur1.fetchall()
    print(row_headers)
    print(frow_headers)
    print(rv)
    print(rv1)
    json_data = []
    json_data1 = []
    for i in rv:
        json_data.append(dict(zip(row_headers, i)))
    print(json_data)

    for result in rv1:
        json_data1.append(dict(zip(frow_headers, result)))
    print(json_data1)
    return render_template('index.html', data=json_data, data1=json_data1)


@app.route('/register', methods=['POST', 'GET'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        # Connect to MySQL database
        con = pymysql.connect(host='localhost', user='root', passwd='Account1start', database='ecommerce1')
        print('connection sucessful')
        cur = con.cursor()
        cur.execute('select * FROM accounts where username = % s', (username,))
        account = cur.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cur.execute('INSERT INTO accounts VALUES (NULL,% s, % s, % s)',
                        (username, email, password))
            con.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('signup.html', msg=msg)


@app.route('/checkuserexist', methods=['POST', 'GET'])
def checkuserexist():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        # Connect to MySQL database
        con = pymysql.connect(host='localhost', user='root', passwd='Account1start', database='ecommerce1')
        print('connection sucessful')
        cur = con.cursor()
        cur.execute('select * FROM accounts where username = % s', (username,))
        account = cur.fetchone()
        if account:
            msg = 'Username not available'
        else:
            msg = 'Username Avialable'

    return jsonify(msg)


@app.route('/login', methods=['POST', 'GET'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        # Connect to MySQL database
        con = pymysql.connect(host='localhost', user='root', passwd='Account1start',
                              database='ecommerce1', cursorclass=pymysql.cursors.DictCursor)
        print('connection sucessfull')
        cur = con.cursor()
        cur.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        account = cur.fetchone()
        print(account)
        if account:

            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            msg = 'Logged in successfully !'
            return redirect('/')
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg=msg)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect('/')


@app.route('/add_product_cart', methods=['POST', 'GET'])
def add_product_cart():
    con = pymysql.connect(host='localhost', user='root', passwd='Account1start',
                          database='ecommerce1', cursorclass=pymysql.cursors.DictCursor)
    print('connection successfull')
    cur = con.cursor()
    print("hii cart")
    try:
        _code = request.form['code']
        _quantity = int(request.form['quantity'])
        print(_code)
        # validate the received values
        if _code and request.method == 'POST':
            cur.execute("SELECT * FROM product WHERE id=%s", _code)
            row = cur.fetchone()
            print(row['id'])
            itemarray = {str(row['id']): {'title': row['title'], 'id': row['id'], 'quantity': _quantity,
                                          'price': row['price'], 'image': row['img'],
                                          'total_price': _quantity * row['price']}}
            print(itemarray)
            all_total_price = 0
            all_total_quantity = 0
            session.modified = True
            if 'cart_item' in session:

                session['cart_item'] = array_merge(session['cart_item'], itemarray)
                print(session['cart_item'])

                for key, value in session['cart_item'].items():
                    print(session)
                    individual_quantity = int(session['cart_item'][key]['quantity'])
                    individual_price = float(session['cart_item'][key]['total_price'])
                    all_total_quantity = all_total_quantity + individual_quantity
                    all_total_price = all_total_price + individual_price
            else:
                session['cart_item'] = itemarray
                all_total_quantity = all_total_quantity + _quantity
                all_total_price = all_total_price + row['price']

            session['all_total_quantity'] = all_total_quantity
            session['all_total_price'] = all_total_price

            return jsonify(session['all_total_quantity'])
        else:
            return jsonify('Error while adding item to cart')
    except Exception as e:
        print("exception")
        print(e)
    finally:
        cur.close()
        con.close()
    return redirect('/')


@app.route('/add1', methods=['POST', 'GET'])
def add_product_cart1():
    con = pymysql.connect(host='localhost', user='root', passwd='Account1start',
                          database='ecommerce1', cursorclass=pymysql.cursors.DictCursor)
    print('connection successfull')
    cur = con.cursor()
    print("hii cart")
    try:
        _code = request.form['code']
        _quantity = int(request.form['quantity'])
        print(_code)
        # validate the received values
        if _code and request.method == 'POST':
            cur.execute("SELECT * FROM product WHERE id=%s", _code)
            row = cur.fetchone()
            print(row['id'])
            itemarray = {str(row['id']): {'title': row['title'], 'id': row['id'], 'quantity': _quantity,
                                          'price': row['price'], 'image': row['img'],
                                          'total_price': _quantity * row['price']}}
            print(itemarray)
            all_total_price = 0
            all_total_quantity = 0
            session.modified = True
            if 'cart_item' in session:

                session['cart_item'] = array_merge(session['cart_item'], itemarray)
                print(session['cart_item'])

                for key, value in session['cart_item'].items():
                    print(session)
                    individual_quantity = int(session['cart_item'][key]['quantity'])
                    individual_price = float(session['cart_item'][key]['total_price'])
                    all_total_quantity = all_total_quantity + individual_quantity
                    all_total_price = all_total_price + individual_price
            else:
                session['cart_item'] = itemarray
                all_total_quantity = all_total_quantity + _quantity
                all_total_price = all_total_price + row['price']

            session['all_total_quantity'] = all_total_quantity
            session['all_total_price'] = all_total_price

            return redirect('/')
        else:
            return 'Error while adding item to cart'
    except Exception as e:
        print("exception")
        print(e)
    finally:
        cur.close()
        con.close()
    return redirect('/')


@app.route('/add2', methods=['POST', 'GET'])
def add_product_cart2():
    con = pymysql.connect(host='localhost', user='root', passwd='Account1start',
                          database='ecommerce1', cursorclass=pymysql.cursors.DictCursor)
    print('connection successfull')
    cur = con.cursor()
    print("hii cart")
    try:
        _code = request.form['code']
        _quantity = int(request.form['quantity'])
        print(_code)
        # validate the received values
        if _code and request.method == 'POST':
            cur.execute("SELECT * FROM featuredproduct WHERE id=%s", _code)
            row = cur.fetchone()
            print(row['id'])
            itemarray = {str(row['id']): {'title': row['title'], 'id': row['id'], 'quantity': _quantity,
                                          'price': row['price'], 'image': row['img'],
                                          'total_price': _quantity * row['price']}}
            print(itemarray)
            all_total_price = 0
            all_total_quantity = 0
            session.modified = True
            if 'cart_item' in session:

                session['cart_item'] = array_merge(session['cart_item'], itemarray)
                print(session['cart_item'])

                for key, value in session['cart_item'].items():
                    print(session)
                    individual_quantity = int(session['cart_item'][key]['quantity'])
                    individual_price = float(session['cart_item'][key]['total_price'])
                    all_total_quantity = all_total_quantity + individual_quantity
                    all_total_price = all_total_price + individual_price
            else:
                session['cart_item'] = itemarray
                all_total_quantity = all_total_quantity + _quantity
                all_total_price = all_total_price + row['price']

            session['all_total_quantity'] = all_total_quantity
            session['all_total_price'] = all_total_price

            return redirect('/')
        else:
            return 'Error while adding item to cart'
    except Exception as e:
        print("exception")
        print(e)
    finally:
        cur.close()
        con.close()
    return redirect('/')


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    code = request.form['code']
    try:
        all_total_price = 0
        all_total_quantity = 0
        session.modified = True

        for item in session['cart_item'].items():  # for key,value in session['cart_item'].item()
            if item[0] == code:
                session['cart_item'].pop(item[0], None)
                break;
        if 'cart_item' in session:
            for key, value in session['cart_item'].items():
                individual_quantity = int(session['cart_item'][key]['quantity'])
                individual_price = float(session['cart_item'][key]['total_price'])
                all_total_quantity = all_total_quantity + individual_quantity
                all_total_price = all_total_price + individual_price

        if all_total_quantity == 0:
            session.pop('cart_item', None)
        else:
            session['all_total_quantity'] = all_total_quantity
            session['all_total_price'] = all_total_price

        return jsonify(session['all_total_quantity'])
    except Exception as e:
        print(e)


@app.route('/add_product_quantity', methods=['GET', 'POST'])
def add_product_quantity():
    code = request.form['code']
    try:
        all_total_price = 0
        all_total_quantity = 0
        session.modified = True

        for item in session['cart_item'].items():
            if item[0] == code:
                item[1]['quantity'] = item[1]['quantity'] + 1
                break;
        if 'cart_item' in session:
            for key, value in session['cart_item'].items():
                individual_quantity = int(session['cart_item'][key]['quantity'])
                individual_price = float(session['cart_item'][key]['total_price'])
                all_total_quantity = all_total_quantity + individual_quantity
                all_total_price = all_total_price + individual_price * individual_quantity

        session['all_total_quantity'] = all_total_quantity
        print(session['all_total_quantity'])
        session['all_total_price'] = all_total_price

        return jsonify(session['all_total_quantity'])
    except Exception as e:
        print(e)


@app.route('/delete_product_quantity', methods=['GET', 'POST'])
def delete_product_quantity():
    code = request.form['code']
    try:
        all_total_price = 0
        all_total_quantity = 0
        session.modified = True

        for item in session['cart_item'].items():
            if item[0] == code:
                if item[1]['quantity'] > 1:
                    print("item deleted")
                    item[1]['quantity'] = item[1]['quantity'] - 1
                    break;
        if 'cart_item' in session:
            for key, value in session['cart_item'].items():
                individual_quantity = int(session['cart_item'][key]['quantity'])
                individual_price = float(session['cart_item'][key]['total_price'])
                all_total_quantity = all_total_quantity + individual_quantity
                all_total_price = all_total_price + individual_price * individual_quantity

        session['all_total_quantity'] = all_total_quantity
        print(session['all_total_quantity'])
        session['all_total_price'] = all_total_price
        print(session['all_total_price'])

        return jsonify(session['all_total_quantity'])
    except Exception as e:
        print(e)


def array_merge(first_array, second_array):
    first_array.update(second_array)
    return first_array

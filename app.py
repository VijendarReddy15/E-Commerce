from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = 'secret123'

def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    db = get_db()
    products = db.execute('SELECT * FROM products').fetchall()
    return render_template('index.html', products=products)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE email = ? AND password = ?',
                          (request.form['email'], request.form['password'])).fetchone()
        if user:
            session['user_id'] = user['id']
            return redirect('/')
        return 'Invalid credentials'
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        db = get_db()
        db.execute('INSERT INTO users (email, password) VALUES (?, ?)',
                   (request.form['email'], request.form['password']))
        db.commit()
        return redirect('/login')
    return render_template('register.html')

@app.route('/product/<int:product_id>')
def product(product_id):
    db = get_db()
    product = db.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
    return render_template('product.html', product=product)

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    db = get_db()
    if request.method == 'POST':
        db.execute('INSERT INTO products (name, price, description) VALUES (?, ?, ?)',
                   (request.form['name'], request.form['price'], request.form['description']))
        db.commit()
    products = db.execute('SELECT * FROM products').fetchall()
    return render_template('admin.html', products=products)

if __name__ == '__main__':
    app.run(debug=True)

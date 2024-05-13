from flask import Blueprint, render_template, request, Flask, session, redirect, url_for, session
from flask_mysqldb import MySQL
from bcrypt import hashpw, gensalt, checkpw
from datetime import datetime

app = Flask(__name__)

mysql = MySQL(app)

main = Blueprint('main', __name__, static_url_path='/static')

@main.route("/")
def home():
    return render_template("pages/home/index.html", title="home")

@main.route("/contact")
def contact():
    return render_template("pages/home/contact.html", title="contact")

@main.route("/menu")
def menu():
    return render_template("pages/home/menu.html", title="menu")

@main.route("/dashboard")
def dashboard():
    return render_template("pages/dashboard/index.html", title="dashboard")

@main.route("/sales")
def sales():
    sales_data = None
    try:
        with mysql.connection.cursor() as cur:
            cur.execute("SELECT * FROM penjualan")
            sales_data = cur.fetchall()
    except Exception as e:
        print("Error fetching data:", e)

    print("Sales data:", sales_data)

    return render_template("pages/dashboard/sales.html", title="Penjualan", sales_data=sales_data)


@main.route("/tambah", methods=["GET", "POST"])
def tambah():
    if request.method == "POST":
        nama_barang = request.form.get("nama_barang")
        harga_barang = request.form.get("harga_barang")
        jumlah_barang = request.form.get("jumlah_barang")
        total_harga = request.form.get("total_harga")

        with mysql.connection.cursor() as cur:
            cur.execute("INSERT INTO penjualan (nama_barang, harga_barang, jumlah_barang, total_harga) VALUES (%s, %s, %s, %s)", (nama_barang, harga_barang, jumlah_barang, total_harga))
            mysql.connection.commit()

        return redirect(url_for('main.sales'))

    return render_template("pages/dashboard/tambah.html", title="Tambah")


@main.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

auth = Blueprint('auth', __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password_candidate = request.form.get("password").encode('utf-8')

        with mysql.connection.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cur.fetchone()

            if user:
                hashed_password = user[3] 
                if checkpw(password_candidate, hashed_password.encode('utf-8')):
                    session['logged_in'] = True
                    session['username'] = username
                    return redirect(url_for('main.dashboard'))
                else:
                    error = "Invalid login"
                    return render_template("pages/auth/login.html", title="Login", error=error)
            else:
                error = "Username not found"
                return render_template("pages/auth/login.html", title="Login", error=error)

    return render_template("pages/auth/login.html", title="Login")

@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")


        salt = gensalt()
        hashed_password = hashpw(password.encode('utf-8'), salt).decode('utf-8') 

        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        with mysql.connection.cursor() as cur:
            cur.execute("INSERT INTO users (email, username, password, created_at, updated_at) VALUES (%s, %s, %s, %s, %s)", (email, username, hashed_password, current_time, current_time))
            mysql.connection.commit()

        return redirect(url_for('auth.login'))

    return render_template("pages/auth/register.html", title="Register")

app.register_blueprint(main)
app.register_blueprint(auth)

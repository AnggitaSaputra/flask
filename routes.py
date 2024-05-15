from flask import Blueprint, render_template, request, Flask, session, redirect, url_for, session
from flask_mysqldb import MySQL
from bcrypt import hashpw, gensalt, checkpw
from datetime import datetime

app = Flask(__name__)

mysql = MySQL(app)

# Define main blueprint
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
        # Use MySQL connection context manager
        with mysql.connection.cursor() as cur:
            cur.execute("SELECT * FROM penjualan")
            sales_data = cur.fetchall()
    except Exception as e:
        print("Error fetching data:", e)
        # Handle the error appropriately, e.g., render an error page

    # Print sales_data to check if it contains the expected data
    print("Sales data:", sales_data)

    return render_template("pages/dashboard/sales.html", title="Penjualan", sales_data=sales_data)


@main.route("/tambah", methods=["GET", "POST"])
def tambah():
    if request.method == "POST":
        # Ambil data dari formulir
        nama_barang = request.form.get("nama_barang")
        harga_barang = request.form.get("harga_barang")
        jumlah_barang = request.form.get("jumlah_barang")
        total_harga = request.form.get("total_harga")

        # Simpan data ke database MySQL
        with mysql.connection.cursor() as cur:
            cur.execute("INSERT INTO penjualan (nama_barang, harga_barang, jumlah_barang, total_harga) VALUES (%s, %s, %s, %s)", (nama_barang, harga_barang, jumlah_barang, total_harga))
            mysql.connection.commit()

        # Redirect kembali ke halaman tambah untuk mengajukan entri baru
        return redirect(url_for('main.sales'))

    # Jika metode adalah GET, tampilkan formulir tambah
    return render_template("pages/dashboard/tambah.html", title="Tambah")


@main.route("/logout")
def logout():
    # Clear session data
    session.clear()
    return redirect(url_for('auth.login'))

# Define auth blueprint
auth = Blueprint('auth', __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Retrieve form data
        username = request.form.get("username")
        password_candidate = request.form.get("password").encode('utf-8')  # Encode password as bytes

        # Fetch user from database
        with mysql.connection.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cur.fetchone()

            if user:
                # Verify password
                hashed_password = user[3]  # Ensure stored hash is encoded
                if checkpw(password_candidate, hashed_password.encode('utf-8')):
                    # Password matched, create session
                    session['logged_in'] = True
                    session['username'] = username
                    return redirect(url_for('main.dashboard'))
                else:
                    # Password incorrect
                    error = "Invalid login"
                    return render_template("pages/auth/login.html", title="Login", error=error)
            else:
                # User not found
                error = "Username not found"
                return render_template("pages/auth/login.html", title="Login", error=error)

    return render_template("pages/auth/login.html", title="Login")

@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Retrieve form data
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")

        # Generate salt and hash the password with bcrypt
        salt = gensalt()  # No additional arguments needed for salt generation
        hashed_password = hashpw(password.encode('utf-8'), salt).decode('utf-8')  # Decode before storing

        # Get the current date and time
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Perform insertion into database
        with mysql.connection.cursor() as cur:
            cur.execute("INSERT INTO users (email, username, password, created_at, updated_at) VALUES (%s, %s, %s, %s, %s)", (email, username, hashed_password, current_time, current_time))
            mysql.connection.commit()

        return redirect(url_for('auth.login'))

    return render_template("pages/auth/register.html", title="Register")

# Register blueprints
app.register_blueprint(main)
app.register_blueprint(auth)

from flask import Blueprint, render_template, request, Flask, session, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from bcrypt import hashpw, gensalt, checkpw
from datetime import datetime

app = Flask(__name__)

mysql = MySQL(app)

main = Blueprint('main', __name__, static_url_path='/static')

@main.route("/")
def home():
    return render_template("pages/index.html", title="home")

@main.route("/contact")
def contact():
    return render_template("pages/contact.html", title="contact")

@main.route("/menu")
def menu():
    with mysql.connection.cursor() as cur:
        cur.execute('SELECT * FROM menu')
        menu_items = cur.fetchall()
    return render_template("pages/menu/index.html", title="menu", menu_items=menu_items)

@main.route("/menu/tambah", methods=["GET", "POST"])
def tambah_menu():
    if request.method == "POST":
        nama = request.form['nama']
        stok = request.form['stok']
        harga_beli = request.form['harga_beli']
        harga_jual = request.form['harga_jual']

        with mysql.connection.cursor() as cur:
            cur.execute('''
                INSERT INTO menu (nama, stok, harga_beli, harga_jual)
                VALUES (%s, %s, %s, %s)
            ''', (nama, stok, harga_beli, harga_jual))
            mysql.connection.commit()

        return redirect(url_for('main.menu'))

    return render_template("pages/menu/tambah.html", title="Tambah Menu")

@main.route("/menu/delete/<int:id>", methods=["POST"])
def delete_menu(id):
    try:
        with mysql.connection.cursor() as cur:
            cur.execute("DELETE FROM menu WHERE id = %s", (id,))
            mysql.connection.commit()
        flash("Menu item deleted successfully", "success")
    except Exception as e:
        mysql.connection.rollback()
        flash(f"An error occurred: {str(e)}", "danger")
    return redirect(url_for('main.menu'))

@main.route("/jurnalumum")
def jurnalumum():
    with mysql.connection.cursor() as cur:
        cur.execute('SELECT * FROM jurnal_umum')
        jurnal_items = cur.fetchall()

    return render_template("pages/jurnalumum/index.html", title="jurnalumum", data=jurnal_items)

@main.route("/jurnalumum/tambah", methods=["GET", "POST"])
def tambah_jurnal():
    if request.method == "POST":
        tanggal = request.form['tanggal']
        keterangan = request.form['keterangan']
        debit = request.form['debit']
        credit = request.form['credit']

        try:
            with mysql.connection.cursor() as cur:
                # Insert into jurnal_umum table
                sql_insert = "INSERT INTO jurnal_umum (tanggal, keterangan, debit, credit) VALUES (%s, %s, %s, %s)"
                cur.execute(sql_insert, (tanggal, keterangan, debit, credit))

            mysql.connection.commit()
            flash('Data has been added and credit updated successfully!', 'success')
        except Exception as e:
            mysql.connection.rollback()
            flash(f'An error occurred: {str(e)}', 'danger')

        return redirect(url_for('main.jurnalumum'))

    return render_template("pages/jurnalumum/tambah.html", title="jurnalumum")

@main.route("/jurnalumum/delete/<int:id>", methods=["POST"])
def delete_jurnal(id):
    try:
        with mysql.connection.cursor() as cur:
            cur.execute("DELETE FROM jurnal_umum WHERE id = %s", (id,))
            mysql.connection.commit()
        flash("Journal entry deleted successfully", "success")
    except Exception as e:
        mysql.connection.rollback()
        flash(f"An error occurred: {str(e)}", "danger")
    return redirect(url_for('main.jurnalumum'))

@main.route("/sales")
def sales():
    sales_data = None
    try:
        with mysql.connection.cursor() as cur:
            query = """
                SELECT penjualan.*, menu.*
                FROM penjualan
                JOIN menu ON penjualan.id_menu = menu.id
            """
            cur.execute(query)
            sales_data = cur.fetchall()
    except Exception as e:
        print("Error fetching data:", e)

    print("Sales data:", sales_data)
    return render_template("pages/penjualan/index.html", title="Penjualan", sales_data=sales_data)

@main.route("/sales/delete/<int:id>", methods=["POST"])
def delete_sale(id):
    try:
        with mysql.connection.cursor() as cur:
            cur.execute("DELETE FROM penjualan WHERE id = %s", (id,))
            mysql.connection.commit()
        flash("Sale deleted successfully", "success")
    except Exception as e:
        mysql.connection.rollback()
        flash(f"An error occurred: {str(e)}", "danger")
    return redirect(url_for('main.sales'))

@main.route("/sales/tambah", methods=["GET", "POST"])
def tambah_penjualan():
    waktu_saat_ini = datetime.now()

    with mysql.connection.cursor() as cur:
        cur.execute("SELECT * FROM menu")
        menu_items = cur.fetchall()

    if request.method == "POST":
        id_menu = request.form.get("id_menu")
        quantity = int(request.form.get("quantity"))  # Ensure quantity is an integer

        with mysql.connection.cursor() as cur:
            cur.execute("SELECT * FROM menu WHERE id = %s", (id_menu,))
            menu_item = cur.fetchone()

            if menu_item:
                price = menu_item[4]
                total = price * quantity
                tanggal_penjualan = waktu_saat_ini

                cur.execute("INSERT INTO penjualan (id_menu, quantity, total, tanggal_penjualan) VALUES (%s, %s, %s, %s)", 
                            (id_menu, quantity, total, tanggal_penjualan))
                mysql.connection.commit()

                return redirect(url_for('main.sales'))
            else:
                return redirect(url_for('main.tambah'))

    return render_template("pages/penjualan/tambah.html", title="Tambah", menu_items=menu_items)

@main.route("/logout")
def logout():
    session.pop('logged_in', None)
    session.clear()
    return redirect(url_for('auth.login'))

auth = Blueprint('auth', __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    session['logged_in'] = True
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
                    return redirect(url_for('main.home'))
                else:
                    error = "Invalid login"
                    return render_template("pages/auth/login.html", title="Login", error=error)
            else:
                error = "Username not found"
                return render_template("pages/auth/login.html", title="Login", error=error)

    return render_template("pages/auth/login.html", title="Login")

app.register_blueprint(main)
app.register_blueprint(auth)

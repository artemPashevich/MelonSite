from flask import Flask, render_template, url_for, request, flash, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
import create_db


app = Flask(__name__)


@app.route("/", methods=['POST', 'GET'])
def home():
     if request.method == 'GET':
        products = create_db.get_all_product()
        id_customer = create_db.get_id_user(session['name'])
     return render_template("home.html", products=products, id_customer=id_customer)


@app.route("/cart/<int:id>", methods=['POST', 'GET'])
def addCartToProduct(id):
        id_customer = create_db.get_id_user(session['name'])
        create_db.add_cart(id_customer['customer_id'], str(id))
        # return redirect(url_for("addCart"), cart_products=cart_products)
        return render_template("cartSeccsess.html")


@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form["email"]
        password = request.form["password"]
        user = create_db.get_user_by_email(email)

        if len(user) > 0:
            if check_password_hash(user['password'], password):
                session['name'] = user['name']
                session['email'] = user['email']
                return render_template("home.html")
        else:
            return "Error password or user not match"
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return render_template("home.html")


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        name = request.form["name"]
        phone = request.form["phone"]
        email = request.form["email"]
        password = request.form["password"]
        hash_password = generate_password_hash(password)
        create_db.add_user(name, email, phone, hash_password)
        session['name'] = name
        session['email'] = email
        return redirect(url_for("home"))


@app.route("/addProduct", methods=["POST", "GET"])
def addProduct():
    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]
        description = request.form["description"]
        id = create_db.get_id_user(session['name'])
        create_db.add_product(id['customer_id'], name, price, description)
        return redirect(url_for("home"))
    return render_template("addProduct.html")


@app.route("/cart", methods=["POST", "GET"])
def cart():
    id_customer = create_db.get_id_user(session['name'])
    cart_products = create_db.get_product_from_cart(id_customer['customer_id'])
    return render_template("cart.html", cart_products=cart_products)


@app.route("/delete/<int:id>", methods=["POST", "GET"])
def deleteCart(id):
    create_db.delete_product_from_cart(id)
    return render_template("deleteProduct.html")


@app.route("/profile", methods=["POST", "GET"])
def profile():
    phone = create_db.get_info_user(session['name'])
    return render_template("profile.html", phone=phone)


if __name__ == "__main__":
    app.secret_key = "ttt"
    app.run(debug=True)


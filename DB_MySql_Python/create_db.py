import mysql.connector


class Database():
    def __init__(self):
        self.conn = mysql.connector.connect(
            user="root",
            password="root",
            host="localhost",
            port='8889',
            database='Melon'
        )
        self.curs = self.conn.cursor(dictionary=True)

    def __enter__(self):
        return self.curs

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()


def add_user(name, email, phone, password):
    with Database() as curs:
        _SQL = f"""INSERT INTO customer (name, phone, email, password)
                          VALUES ('{name}', '{phone}', '{email}', '{password}');"""
        curs.execute(_SQL)


def get_user_by_email(email):
    with Database() as curs:
        _SQL = f"""SELECT * FROM customer WHERE email = '{email}' LIMIT 1;"""
        curs.execute(_SQL)
        return curs.fetchone()


def add_product(id_user, name, price, description):
    with Database() as curs:
        _SQL = f"""INSERT INTO product (name, description, price, customer_id)
                          VALUES ('{name}', '{description}', '{price}', '{id_user}');"""
        curs.execute(_SQL)


def get_id_user(name_user):
    with Database() as curs:
        _SQL = f"""SELECT customer_id FROM customer WHERE name = '{name_user}' LIMIT 1;"""
        curs.execute(_SQL)
        return curs.fetchone()


def get_all_product():
    with Database() as curs:
        _SQL = f"""SELECT * FROM product;"""
        curs.execute(_SQL)
        products = curs.fetchall()
        return products


def add_cart(customer_id, product_id):
    with Database() as curs:
        _SQL = f"""INSERT INTO cart (customer_id, id_product)
                          VALUES ('{customer_id}', '{product_id}');"""
        curs.execute(_SQL)


def get_product_from_cart(customer_id):
    with Database() as curs:
        _SQL = f"""SELECT name, description, price, cart.id_product
                   FROM product
                   INNER JOIN cart
                   ON cart.id_product = product.id_product 
                   WHERE cart.customer_id = '{customer_id}';"""
        curs.execute(_SQL)
        return curs.fetchall()


def delete_product_from_cart(id_product):
    with Database() as curs:
        _SQL = f"""DELETE FROM cart WHERE id_product='{id_product}';"""
        curs.execute(_SQL)


def get_info_user(name_user):
    with Database() as curs:
        _SQL = f"""SELECT phone
                    FROM customer
                    WHERE name = '{name_user}' LIMIT 1;"""
        curs.execute(_SQL)
        return curs.fetchone()


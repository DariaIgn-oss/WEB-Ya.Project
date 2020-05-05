import sqlalchemy
from data import products
from data import db_session

db_session.global_init("db/blogs0.sqlite")


def price_products(products_list):
    session = db_session.create_session()
    result = 0
    count = 0
    if products_list[0] == '1':
        result = 1
        summa = 0
        for product in products_list[1:]:
            product = product.split(':')
            bd = products.Products
            for prod in session.query(bd).filter(bd.title.like(product[0])):
                summa += prod.prices * int(product[1])
                count += 1
            if count != 0:
                result = summa / count
    elif products_list[0] == '2':
        for product in products_list[1:]:
            if product.isdigit():
                result += int(product)
                count += 1
    return result

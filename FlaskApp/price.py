import sqlalchemy
from data import products
from data import db_session


def price_products(products_list):
    db_session.global_init('blogs0.sqlite')
    session = db_session.create_session()
    result = 0
    if products_list[0] == '1':
        for product in products_list:
            summa = 1
            count = 0
            product = product.split(':')
            bd = products.Products
            for prices in session.query(bd).filter(bd.title.like(product[0])):
                summa += prices * int(product[1])
                count += 1
            if count != 0:
                result += summa // count
            else:
                return '0'
    if products_list[0] == 2:
        for product in products_list:
            if product.isdigit():
                result += int(product)
    return result

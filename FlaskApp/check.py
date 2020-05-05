from route import price_per_path
from price import price_products

const = {'tel': True, 'path': True, 'order': True, 'payment': True, 'price': 0}


def check_number(number):
    number = number.replace(' ', '')
    if number:
        if number.isdigit():
            if number[0] == '8':
                if len(number) == 11:
                    return True
    return False


def check_order(args):
    if not check_number(args[0]):
        const['tel'] = False
    if args[-1].lower() != 'картой':
        if args[-1].lower() != 'наличными':
            const['payment'] = False

    message = args[-2].split('\n')
    for i in range(len(message)):
        message[i] = message[i].replace('\r', '')
    if message and len(message) > 1 and message[0] == '1' or message[0] == '2':
        const['price'] = price_products(message)
    else:
        const['order'] = False

    price_path = price_per_path(args[-4], args[-3])
    if not price_path:
        const['path'] = False
    else:
        const['price'] += price_path


def check_True(lst):
    global const
    for key in lst.keys():
        if (lst[key] is not True and key != 'price') and lst['price'] != 0:
            const = {'tel': True, 'path': True, 'order': True, 'payment': True, 'price': 0}
            return False
    return True

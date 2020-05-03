from route import price_per_path

const = {'tel': True, 'path': True, 'order': True, 'payment': True}


def check_number(number):
    number = number.replace(' ', '')
    if number:
        if number.isdigit():
            if number[0] == '8':
                if len(number) == 11:
                    return True
    return False


def check_order(*args):
    if not check_number(args[0]):
        const['tel'] = False
    if args[-1].lower() != 'картой':
        if args[-1].lower() != 'наличными':
            const['payment'] = False

    message = args[-2].split('\n')
    for i in range(len(message)):
        message[i] = message[i].replace('\r', '')
    if not message:
        if len(message) < 2:
            if message[0] != '1' or message[0] != '2':
                const['order'] = False

    if not price_per_path(args[-4], args[-3]):
        const['path'] = False

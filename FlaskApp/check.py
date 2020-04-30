from route.py import price_per_path

class FormatError(Exception):
    pass


class FormatSurNameError(FormatError):
    pass


class FormatNumberError(FormatError):
    pass


class FormatAddressError(FormatError):
    pass


def check_number(number):
    number = number.replace(' ', '')
    if not number.isdigit() or number[0] != 8 or len(number) != 11:
        return False
    else:
        return True

def check(*args):
    try:
        if not args[0] and not args[1]:
            raise FormatSurNameError('Вы не указали ни имени, ни фамилии! Мы не знаем, как к вам обращаться!')
        elif not check_number(args[2]):
            raise FormatNumberError('Номер недействителен!')



from binance.um_futures import UMFutures
from math import floor
from random import randint


# {
#    "volume": 10000.0,  # Объем в долларах
#    "number": 5,  # На сколько ордеров нужно разбить этот объем
#    "amountDif": 50.0,  # Разброс в долларах, в пределах которого случайным образом выбирается объем в верхнюю и нижнюю сторону
#    "side": "SELL",  # Сторона торговли (SELL или BUY)
#    "priceMin": 200.0,  # Нижний диапазон цены, в пределах которого нужно случайным образом выбрать цену
#    "priceMax": 300.0  # Верхний диапазон цены, в пределах которого нужно случайным образом выбрать цену
# }

symbol = 'BTCUSDT'
api_key = ''
secret_key = ''
client = UMFutures(key=api_key, secret=secret_key) # пример на фьючерсах


# Это блок округления в нижнюю сторону
# На биржах есть лимит на количетсво знаков после запятой плюс питон иногда при делении оставляят хвосты
def round_down(x, n=0):
    if n == 0:
        x = x + 0.0000000001  # без этого добавления округление в нижнюю сторону сьедало 1 от последнего числа
        a = floor(x)
    else:
        x = x + 0.0000000001
        a = x
        for i in range(n):
            a = a * 10
        a = floor(a)
        for i in range(n):
            a = a / 10
    a = round(a, n)
    return a


def make_orders(df):
    volume = df['volume']
    number = df['number']
    amountDif = df['amountDif']
    side = df['side']
    priceMin = df['priceMin']
    priceMax = df['priceMax']

    volume_per_trade = round(float(volume)/int(floor(float(number))))
    amountDif = floor(float(amountDif))

    n = df['n'] # У некоторых монет разное допустимое количество знаков после запятой, было бы не плохо его тоже получить


    for i in range(5):
        tmp_rand_vol = randint(0, int(float(amountDif * 2)))
        tmp_volume = volume_per_trade - amountDif + tmp_rand_vol
        tmp_rand_price = randint(int(floor(priceMin), int(floor(priceMax))))

        # Вычисляем объем в нужной нам монете и округляем до допустмого количества знаков после запятой
        qty = round_down(tmp_volume/tmp_rand_price,n)

        if side == "BUY":
            try:
                client.new_order(symbol=symbol, side='BUY', type='LIMIT', timeInForce='GTC',
                                 quantity=qty, price=tmp_rand_price)
            except:
                print('Ордер не был размещен')
        elif side == "SELL":
            try:
                client.new_order(symbol=symbol, side='SELL', type='LIMIT', timeInForce='GTC',
                                 quantity=qty, price=tmp_rand_price)
            except:
                print('Ордер не был размещен')


# В данном случае ошибки могут быть в некорректонсти исходных данных или если цена размещенных ордеров
# не адекватная(Цена лимтоного ордера BUY не может быть выше текущей цены)
# Так же ордер не будет размещен при отстутсвии доступных на это средств

# заранее извиняюсь за отсутвие тестов.
# питон целенаправленно не учил и не особо интересовался как их делать.
# но при желании конечно могу и это исправить.
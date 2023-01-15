import requests
import json
from config import currencies


class APIException(Exception):
    pass

class Converter:
    @staticmethod
    def get_price(base, quote, amount):
        try:
            base_ticker = currencies[base.lower()]
        except KeyError:
            raise APIException(f"Валюта '{base}' не найдена!")

        try:
            quote_ticker = currencies[quote.lower()]
        except KeyError:
            raise APIException(f"Валюта '{quote}' не найдена!")

        if base.lower() == quote.lower():
            raise APIException(f'Введите 2 разных валюты!')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество "{amount}"!')

        r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}")
        conversion = round(json.loads(r.content)[quote_ticker] * amount, 2)
        message_ = f'За {amount} {base_ticker} вы получите {conversion} {quote_ticker}'
        return message_

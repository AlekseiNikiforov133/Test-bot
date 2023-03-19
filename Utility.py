import requests
import json
from Config import keys


class ConvertException(Exception):
    pass


class CurrencyConvert:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertException(f"Невозможно обработать одинаковые валюты {base}")

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertException(f'Не удалось обработать количество {amount}')

        req = requests.get(f'https://api.exchangeratesapi.io/latest?symbols={base_ticker}&base={quote_ticker}')
        total_base = json.loads(req.content)["rates"][keys[base]]*amount

        return total_base
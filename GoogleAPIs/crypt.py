from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json


class Crpyo:
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'limit': 1,
        'convert': 'BRL',
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': 'be0f6e20-47f6-44f2-8652-ded0c4b74ea9',
    }

    async def get_cryptocurrency(self):
        try:
            session = Session()
            session.headers.update(self.headers)
            response = session.get(self.url, params=self.parameters)
            data = json.loads(response.text)
            data = data['data'][0]
            name = data['name']
            price = f"{data['quote']['BRL']['price']:0,.2f}"
            pair = self.parameters['convert']
            symbol = data['symbol']
            value_btc = f'R$ {price} {pair}/{symbol}'
            output = dict({name: value_btc})
            return output
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)


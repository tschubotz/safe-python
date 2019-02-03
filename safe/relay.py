import requests
from .utils import TransactionSpeed

class Relay(object):
    def __init__(self, url):
        self.base = url
        self.gas_price = None
    
    def _build_endpoint(self, url):
        return '{}/api/v1/{}/'.format(self.base, url)

    def gas_station(self, transaction_speed=TransactionSpeed.Standard):
        endpoint = self._build_endpoint('gas-station')
        response = requests.get(endpoint)

        return int(response.json()[transaction_speed])

    def get_gas_price(self):
        if not self.gas_price:
            self.gas_price = self.gas_station()
        return self.gas_price

    def estimate_transaction(self, transaction):
        endpoint = self._build_endpoint('safes/{}/transactions/estimate'.format(transaction.safe_address))

        response = requests.post(endpoint, json={
            'safe': transaction.safe_address,
            'to': transaction.to,
            'value': transaction.value,
            'data': transaction.data.hex(),
            'operation': transaction.operation,
            'gasToken': transaction.gas_token
        })
        
        return response.json()

    def create_transaction(self, transaction):
        endpoint = self._build_endpoint('safes/{}/transactions/'.format(transaction.safe_address))

        response = requests.post(endpoint, json={
            'safe': transaction.safe_address,
            'to': transaction.to,
            'value': transaction.value,
            'data': transaction.data.hex(),
            'operation': transaction.operation,
            'gasToken': transaction.gas_token,
            'safeTxGas': transaction.safe_tx_gas,
            'dataGas': transaction.data_gas,
            'gasPrice': transaction.gas_price,
            'refundReceiver': transaction.refund_receiver,
            'nonce': transaction.nonce,
            'signatures': transaction.signatures
        })

        return response.json()

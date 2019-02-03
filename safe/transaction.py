from .utils import ADDRESS0, Operation

class Transaction(object):
    def __init__(
        self, 
        safe_address, 
        to = '',
        value = 0,
        data = bytes(0),
        operation = Operation.Call,
        gas_token = ADDRESS0,
        safe_tx_gas = 0,
        data_gas = 0,
        gas_price = 0,
        refund_receiver = ADDRESS0,
        nonce = 0,
        signatures = []):
        self.safe_address = safe_address
        self.to = to
        self.value = value
        self.data = data
        self.operation = operation
        self.gas_token = gas_token
        self.safe_tx_gas = safe_tx_gas
        self.data_gas = data_gas
        self.gas_price = gas_price
        self.refund_receiver = refund_receiver
        self.nonce = nonce
        self.signatures = signatures
        self.transaction_semantics_text = ''

    def estimate(self, relay):
        estimate = relay.estimate_transaction(self)        
        self.safe_tx_gas = estimate['safeTxGas']
        self.data_gas = estimate['dataGas']
        # self.nonce = int(estimate['lastUsedNonce']) + 1 if estimate ['lastUsedNonce'] else 0 # Seems the relay service always returns None
        
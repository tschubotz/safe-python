from .utils import ADDRESS0, Operation
from ethereum.utils import ecrecover_to_pub

class Transaction(object):
    def __init__(
        self, 
        safe, 
        to = '',
        value = 0,
        data = '0x',
        operation = Operation.Call,
        gas_token = ADDRESS0,
        safe_tx_gas = 0,
        data_gas = 0,
        gas_price = 0,
        refund_receiver = ADDRESS0,
        nonce = 0,
        signatures = []):
        self.safe = safe
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
        self.hash = ''

    def estimate(self, relay):
        estimate = relay.estimate_transaction(self)

        self.safe_tx_gas = estimate['safeTxGas']
        self.data_gas = estimate['dataGas']
        
    def calculate_hash(self):
        self.hash = self.safe.get_transaction_hash(self)

    def add_signatures(self, signatures):
        # sort signatures by lower case lexicographical order
        mapping = {}
        for signature in signatures:
            address = ecrecover_to_pub(self.hash, signature['v'], signature['r'], signature['s'])
            mapping[address.lower()] = signature

        sorted_signatures = []
        
        for address in sorted(mapping):
            sorted_signatures.append(mapping[address])
        
        self.signatures = sorted_signatures

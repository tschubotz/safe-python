import web3
from gnosis.safe.contracts import get_safe_contract
from web3.middleware import geth_poa_middleware
from .relay import Relay
from .transaction import Transaction
from .utils import sign, get_balance
from ethereum import utils
import codecs



class Safe(object):
    def __init__(self, address, rpc_endpoint_url, safe_relay_url):
        """Initializes a Safe.
        """
        self.address = address
        self.w3 = web3.Web3(web3.HTTPProvider(rpc_endpoint_url))
        # https://web3py.readthedocs.io/en/stable/middleware.html#geth-style-proof-of-authority
        self.w3.middleware_stack.inject(geth_poa_middleware, layer=0)
        self.contract = get_safe_contract(w3=self.w3, address=self.address)
        self.safe_relay = Relay(safe_relay_url)

    def get_balance(self, unit='wei'):
        """Returns the Safe balance in the given unit.
        """
        return get_balance(self.w3, self.address, unit)

    def get_nonce(self):
        """Return the current nonce of the Safe.
        """
        return self.contract.functions.nonce().call()

    def get_owners(self):
        """Returns a list of owner addresses.
        """
        return self.contract.functions.getOwners().call()

    def get_threshold(self):
        """Returns the threshold as int.
        """
        return self.contract.functions.getThreshold().call()

    def get_transaction_hash(self, transaction):
        """Return hash to be signed by owners.
        """
        return self.contract.functions.getTransactionHash(
            transaction.to,
            transaction.value,
            transaction.data, 
            transaction.operation, 
            transaction.safe_tx_gas, 
            transaction.data_gas, 
            transaction.gas_price,
            transaction.gas_token,
            transaction.refund_receiver,
            transaction.nonce
        ).call()
        
    # def exec_transaction(
    #     self,
    #     to,
    #     value,
    #     data,
    #     operation,
    #     safeTxGas,
    #     dataGas,
    #     gasPrice,
    #     gasToken,
    #     refundReceiver,
    #     signatures
    # ):
        
    #     #     gasPrice=self.w3.eth.gasPrice,


    #     tx = self.contract.functions.execTransaction(
    #         to,
    #         value,
    #         data,
    #         operation,
    #         safeTxGas,
    #         dataGas,
    #         gasPrice,
    #         gasToken,
    #         refundReceiver,
    #         signatures
    #         ).buildTransaction({
    #             'nonce': self.w3.eth.getTransactionCount('0x39cBD3814757Be997040E51921e8D54618278A08'),
    #             'gas': safeTxGas + dataGas,
    #             'gasPrice': gasPrice,
    #             'chainId': 1977 
    #         })
    #     private_key = ''

    #     # self.w3.eth.estimateGas({'from':self.contract.address, 'to':self.contract.address, 'data': self.contract.functions.requiredTxGas(to, value, data, operation)._encode_transaction_data()})
    #     signed_tx = self.w3.eth.account.signTransaction(tx, private_key)
        
    #     tx_hash = self.w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    #     import pdb; pdb.set_trace()
    #     print(tx_hash)

    def build_transaction(self, function, *params):
        transaction = function(*params)
        transaction.gas_price = self.safe_relay.get_gas_price()
        transaction.estimate(self.safe_relay)
        transaction.nonce = self.get_nonce()
        return transaction, self.get_transaction_hash(transaction)

    def execute_transaction(self, transaction, signatures):
        transaction.signatures = signatures

        return self.safe_relay.create_transaction(transaction)

    def transfer_ether(self, to, ether_value):
        transaction = Transaction(
            self.address,
            to = to,
            value = self.w3.toWei(ether_value, 'ether'))
        
        transaction.transaction_semantics_text = 'Transfer {} ETH from your Safe to {}'.format(transaction.value, transaction.to)

        return transaction

import web3
from gnosis.safe.contracts import get_safe_contract
from web3.middleware import geth_poa_middleware


class Operation(object):
    Call = 0
    DelegateCall = 1
    Create = 2

ADDRESS0 = '0x0000000000000000000000000000000000000000'

class Safe(object):
    def __init__(self, address, rpc_endpoint_url):
        """Initializes a Safe.
        """
        self.address = address
        self.w3 = web3.Web3(web3.HTTPProvider(rpc_endpoint_url))
        # https://web3py.readthedocs.io/en/stable/middleware.html#geth-style-proof-of-authority
        self.w3.middleware_stack.inject(geth_poa_middleware, layer=0)
        self.contract = get_safe_contract(w3=self.w3, address=self.address)

    def get_balance(self, unit='wei'):
        """Returns the Safe balance in the given unit.
        """
        return get_balance(self.w3, self.address, unit)

    def get_owners(self):
        """Returns a list of owner addresses.
        """
        return self.contract.functions.getOwners().call()

    def get_threshold(self):
        """Returns the threshold as int.
        """
        return self.contract.functions.getThreshold().call()

    def exec_transaction(
        self,
        to,
        value,
        data,
        operation,
        safeTxGas,
        dataGas,
        gasPrice,
        gasToken,
        refundReceiver,
        signatures
    ):
        
        #     gasPrice=self.w3.eth.gasPrice,
        

        tx = self.contract.functions.execTransaction(
            to,
            value,
            data,
            operation,
            safeTxGas,
            dataGas,
            gasPrice,
            gasToken,
            refundReceiver,
            signatures
            ).buildTransaction()
        tx['nonce'] = self.w3.eth.getTransactionCount('0x0e329fa8d6Fcd1ba0Cda495431F1f7CA24F442C2')
        private_key = ''
        signed_tx = self.w3.eth.account.signTransaction(tx, '')
        tx_hash = self.w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(tx_hash)

    def transfer_ether(self, to, ether_value, signatures):
        return self.exec_transaction(
                    to=to,
                    value=self.w3.toWei(ether_value, 'ether'),
                    data=bytes(0),
                    operation=Operation.Call,
                    safeTxGas=100000,
                    dataGas=100000,
                    gasPrice=10,
                    gasToken=ADDRESS0,
                    refundReceiver=ADDRESS0,
                    signatures=bytes(0)
                    )


def code_exists(w3, address):
    """Checks if code exists at the given address. Returns boolean.
    """
    return (len(w3.eth.getCode(address)) != 0)


def get_balance(w3, address, unit='wei'):
    """Return the balance of the address in the given unit.
    """
    wei_balance = w3.eth.getBalance(address)
    return w3.fromWei(wei_balance, unit)
import web3
from gnosis.eth.contracts import get_safe_contract
from web3.middleware import geth_poa_middleware
from .relay import Relay
from .transaction import Transaction
from .utils import get_balance
from ethereum import utils
import codecs


class Safe(object):
    def __init__(self, network, address, rpc_endpoint_url, safe_relay_url):
        """Initializes a Safe.
        """
        self.network = network
        self.address = address
        self.w3 = web3.Web3(web3.HTTPProvider(rpc_endpoint_url))
        # https://web3py.readthedocs.io/en/stable/middleware.html#geth-style-proof-of-authority
        self.w3.middleware_stack.inject(geth_poa_middleware, layer=0)
        self.contract = get_safe_contract(w3=self.w3, address=self.address)
        self.safe_relay = Relay(safe_relay_url)

    def get_owners_sentinel(self):
        """Return the owner sentinel constat.
        """
        return self.contract.functions.SENTINEL_OWNERS().call()

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

    def build_transaction(self, function, *params):
        transaction = function(*params)
        transaction.gas_price = self.safe_relay.get_gas_price()
        transaction.estimate(self.safe_relay)
        transaction.nonce = self.get_nonce()
        transaction.calculate_hash()
        return transaction

    def execute_transaction(self, transaction, signatures):
        transaction.add_signatures(signatures)

        return self.safe_relay.create_transaction(transaction)

    def transfer_ether_tx(self, to, ether_value):
        transaction = Transaction(
            self,
            to = to,
            value = self.w3.toWei(ether_value, 'ether'))
        
        transaction.transaction_semantics_text = 'Transfer {} ETH from your Safe to {}'.format(self.w3.fromWei(transaction.value, 'ether'), transaction.to)

        return transaction

    def owner_add_tx(self, owner_address, threshold):
        data = self.contract.encodeABI(fn_name='addOwnerWithThreshold', args=[owner_address,1])

        transaction = Transaction(
            self,
            to = self.address,
            data = data)

        transaction.transaction_semantics_text = 'Add owner with address {} and set threshold to {}'.format(owner_address, threshold)
        
        return transaction
        
    def owner_remove_tx(self, owner_address, threshold):
        prev_owner = self._get_prev_owner(owner_address)

        data = self.contract.encodeABI(fn_name='removeOwner', args=[prev_owner, owner_address, 1])

        transaction = Transaction(
            self,
            to = self.address,
            data = data)

        transaction.transaction_semantics_text = 'Remove owner with address {} and set threshold to {}'.format(owner_address, threshold)
        
        return transaction
        

    def owner_swap_tx(self, old_owner_address, new_owner_address):
        prev_owner = self._get_prev_owner(old_owner_address)

        data = self.contract.encodeABI(fn_name='swapOwner', args=[prev_owner, old_owner_address, new_owner_address])

        transaction = Transaction(
            self,
            to = self.address,
            data = data)

        transaction.transaction_semantics_text = 'Replace owners: Remove owner with address {} and add owner with address {}'.format(old_owner_address, new_owner_address)
        
        return transaction

    def owner_change_threshold_tx(self, threshold):
        data = self.contract.encodeABI(fn_name='changeThreshold', args=[threshold])

        transaction = Transaction(
            self,
            to = self.address,
            data = data)

        transaction.transaction_semantics_text = 'Change threshold to {}'.format(threshold)
        
        return transaction
        
    def _get_prev_owner(self, owner_address):
        """Some OwnerManager methods require to provide the address of the previous owner address store in the owner mapping.

        See:
        https://github.com/gnosis/safe-contracts/blob/development/contracts/base/OwnerManager.sol#L74
        https://github.com/gnosis/safe-contracts/blob/development/contracts/base/OwnerManager.sol#L97

        """
        owners = self.get_owners()
        # If owner to be remove is on index 0, then SENTINEL_OWNERS
        try:
            owner_index = owners.index(owner_address)
        except ValueError:
            raise Exception('{} is not an owner of Safe at {}'.format(owner_address, self.address))

        return self.get_owners_sentinel() if owner_index == 0 else owners[owner_address - 1]

import codecs
from ethereum import utils


ADDRESS0 = '0x0000000000000000000000000000000000000000'


class TransactionSpeed(object):
    Lowest = 'lowest'
    SafeLow = 'safeLow'
    Standard = 'standard'
    Fast = 'fast'
    Fastest = 'fastest'


class Operation(object):
    Call = 0
    DelegateCall = 1
    Create = 2
    

def code_exists(w3, address):
    """Checks if code exists at the given address. Returns boolean.
    """
    return not(w3.eth.getCode(address) == 0 or w3.eth.getCode(address).hex() == '0x00')


def get_balance(w3, address, unit='wei'):
    """Return the balance of the address in the given unit.
    """
    wei_balance = w3.eth.getBalance(address)
    return w3.fromWei(wei_balance, unit)
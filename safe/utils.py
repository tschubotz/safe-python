import codecs
from ethereum import utils
from bip44.crypto import HDPrivateKey, HDKey

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
    return not(
        w3.eth.getCode(address) == 0 
        or w3.eth.getCode(address).hex() in ('0x00', '0x', '0x0')
        )


def get_balance(w3, address, unit='wei'):
    """Return the balance of the address in the given unit.
    """
    wei_balance = w3.eth.getBalance(address)
    return w3.fromWei(wei_balance, unit)


def get_account_info_from_mnemonic(mnemonic, index=0):
    """asdf
    """
    master_key = HDPrivateKey.master_key_from_mnemonic(mnemonic)
    root_keys = HDKey.from_path(master_key,"m/44'/60'/0'")
    acct_priv_key = root_keys[-1]
    
    keys = HDKey.from_path(acct_priv_key,'{change}/{index}'.format(change=0, index=index))
    private_key = keys[-1]
    public_key = private_key.public_key
    
    return private_key._key.to_hex(), public_key.address()
import pytest
from safe.utils import TransactionSpeed, Operation, code_exists, get_balance, get_account_info_from_mnemonic
from hexbytes.main import HexBytes
from web3 import Web3

def test_enums():
    assert TransactionSpeed.Lowest == 'lowest'
    assert TransactionSpeed.SafeLow == 'safeLow'
    assert TransactionSpeed.Standard == 'standard'
    assert TransactionSpeed.Fast == 'fast'
    assert TransactionSpeed.Fastest == 'fastest'

    assert Operation.Call == 0
    assert Operation.DelegateCall == 1
    assert Operation.Create == 2

def test_code_exists(mocker):
    w3_mock = mocker.MagicMock()
    w3_mock.eth.getCode.return_value = 0

    address = '0x123'
    assert not code_exists(w3_mock, address)

    w3_mock.eth.getCode.return_value = HexBytes('')
    assert not code_exists(w3_mock, address)

    w3_mock.eth.getCode.return_value = HexBytes('0x')
    assert not code_exists(w3_mock, address)

    w3_mock.eth.getCode.return_value = HexBytes('0x0')
    assert not code_exists(w3_mock, address)

    w3_mock.eth.getCode.return_value = HexBytes('0x00')
    assert not code_exists(w3_mock, address)

    w3_mock.eth.getCode.return_value = HexBytes(address)
    assert code_exists(w3_mock, address)

def test_balance(mocker):
    w3 = Web3()
    address = '0x123'
    w3.eth.getBalance = mocker.MagicMock()
    w3.eth.getBalance.return_value = 12345678901234
    get_balance(w3, address)

    get_balance(w3, address) == 12345678901234
    get_balance(w3, address, 'ether') == 0.000012345678901234

def test_get_account_info_from_mnemonic():
    test_address = '0x39cBD3814757Be997040E51921e8D54618278A08'
    test_key = '9bb77243653b370165aa6d7c6e7826ba0b35b2ce76858ceba57d5decad557405'
    test_mnemonic = 'abuse garden okay stuff mistake exotic vanish unlock certain erase female umbrella'

    private_key, address = get_account_info_from_mnemonic(test_mnemonic)

    assert private_key == test_key
    assert test_address == address
    assert Web3.isChecksumAddress(address)
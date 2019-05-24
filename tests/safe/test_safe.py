import pytest
from safe import Safe
from commands import ENVS
from web3 import Web3
from safe.transaction import Transaction
from safe.utils import Operation

# safe
# lawn canoe sure wrestle inform patrol tomato bitter collect dilemma kidney denial
# 0xb1A135230A88BB4Ef938110C2E8ceD27F97e946B
# Available Accounts
# ==================
# (0) 0x39cbd3814757be997040e51921e8d54618278a08 (~100 ETH)
# (1) 0xfc7efb6bfc363ec16d560a27a006832f32f65c20 (~100 ETH)
# (2) 0xe375204da98055d1c96fc12172252fbaf105e052 (~100 ETH)
# (3) 0xb02dcdcaac338fb5ee12ca0a59457fa05d50c3e7 (~100 ETH)
# (4) 0x08ef4fa325b930a4c50b0e13e9bbd73f5611d3fb (~100 ETH)
# (5) 0xcbd7f9606c14c6f2d78a0c8ee3dbb3951a1635fa (~100 ETH)
# (6) 0xddbdb60f31e5d5c0e1223c565f5344f66f8ae7f9 (~100 ETH)
# (7) 0xa24bc4872264295f016c0765c1720853543c65d6 (~100 ETH)
# (8) 0x6dcd79066a3b629b9aaffb57d1d6654a3a8f49d5 (~100 ETH)
# (9) 0xd8efe0bb9805b5862c0827b06b699cdf692dff9b (~100 ETH)

# Private Keys
# ==================
# (0) 0x9bb77243653b370165aa6d7c6e7826ba0b35b2ce76858ceba57d5decad557405
# (1) 0xeda15f8d16b9f6bf4c9b0e5618914aa379359e27ac6b8fe6027fc1c5f54c3a2d
# (2) 0xa4e20f2809258ddcd5d31d85b505926663bfb31220c6c153eb98f926d113aef8
# (3) 0xe70b090ce5428c598bf8f625aeaee256a029b6a361475f05cfabc46d9b256379
# (4) 0x29fe99787c8d7a838a99e71fb8c7cee60aa8a880f91c5e93dcadf63f7fe20c2f
# (5) 0x4ce2edc66b436e5fd8f58627b2703242830989a747bc744fe5de87dcdf83e1b0
# (6) 0x0026fc8af98c4832b0c8a0830c3da8008b1b45d0f93379291e61a408e1f9149e
# (7) 0xb5810b353648846f958a458423729a0e235d9eec73026c9e0e20b2826b00dcea
# (8) 0xe65e5c2801f9ed06400d14edbb6d30f3fa52c871561c0fc0c24848498364e466
# (9) 0xa67bd80bd7ed048e01656ba31972a3359bf14c347de29f8dd881d770caab602e

# @pytest.fixture
# def transaction():
#     safe
#     t = Transaction()
#     return smtplib.SMTP("smtp.gmail.com", 587, timeout=5)
# @pytest.fixture
# def safe(mocker):
#     network = ENVS['rinkeby']
#     address = '0xb1A135230A88BB4Ef938110C2E8ceD27F97e946B'    
#     return Safe(network, address, '', '')


def test_get_owners_sentinel(mocker):
    safe = Safe(None, '', '', '')
    safe.contract.functions.SENTINEL_OWNERS = mocker.MagicMock()
    sentinel_owners_mock = mocker.MagicMock()
    sentinel_owners_mock.call.return_value = 123
    safe.contract.functions.SENTINEL_OWNERS.return_value = sentinel_owners_mock
    
    assert safe.get_owners_sentinel() == 123
    sentinel_owners_mock.call.assert_called()

def test_get_nonce(mocker):
    safe = Safe(None, '', '', '')
    safe.contract.functions.nonce = mocker.MagicMock()
    nonce_mock = mocker.MagicMock()
    nonce_mock.call.return_value = 123
    safe.contract.functions.nonce.return_value = nonce_mock
    
    assert safe.get_nonce() == 123
    nonce_mock.call.assert_called()

def test_get_owners(mocker):
    safe = Safe(None, '', '', '')
    safe.contract.functions.getOwners = mocker.MagicMock()
    get_owners_mock = mocker.MagicMock()
    get_owners_mock.call.return_value = 123
    safe.contract.functions.getOwners.return_value = get_owners_mock
    
    assert safe.get_owners() == 123
    get_owners_mock.call.assert_called()

def test_get_threshold(mocker):
    safe = Safe(None, '', '', '')
    safe.contract.functions.getThreshold = mocker.MagicMock()
    get_threshold_mock = mocker.MagicMock()
    get_threshold_mock.call.return_value = 123
    safe.contract.functions.getThreshold.return_value = get_threshold_mock
    
    assert safe.get_threshold() == 123
    get_threshold_mock.call.assert_called()

def test_get_balance(mocker):
    safe = Safe(None, '', '', '')
    safe.w3.eth.getBalance = mocker.MagicMock()
    safe.w3.eth.getBalance.return_value = 12345678901234

    assert safe.get_balance() == 12345678901234
    assert float(safe.get_balance('ether')) == 0.000012345678901234
    
def test_get_transaction_hash(mocker):
    safe = Safe(None, '', '', '')
    transaction = Transaction(
        safe, 
        '0xto_address', 
        value=0.123,
        data='0xdata', 
        operation=Operation.Call, 
        gas_token='0xgas_token',
        safe_tx_gas=123,
        data_gas=456,
        gas_price=789,
        refund_receiver='0xrefund_receiver',
        nonce=90
    )
    safe.contract.functions.getTransactionHash = mocker.MagicMock()
    get_transation_hash_mock = mocker.MagicMock()
    get_transation_hash_mock.call.return_value = 123
    safe.contract.functions.getTransactionHash.return_value = get_transation_hash_mock
    
    assert safe.get_transaction_hash(transaction) == 123
    get_transation_hash_mock.call.assert_called()
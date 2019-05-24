import pytest

from safe.transaction import Transaction

def test_estimate(mocker):
    transaction = Transaction(None)
    relay_mock = mocker.MagicMock()
    
    relay_mock.estimate_transaction.return_value = {'safeTxGas': 123, 'dataGas': 456}
    transaction.estimate(relay_mock)

    relay_mock.estimate_transaction.assert_called_with(transaction)
    assert transaction.safe_tx_gas == 123
    assert transaction.data_gas == 456

def test_calculate_hash(mocker):
    safe_mock = mocker.MagicMock()
    safe_mock.get_transaction_hash.return_value = b'\x8c\xfb\xfa\xc7\x8a\xd8\x0eC%\x99\x93b\x1e\xac\xa6k\x07\xff\x12\xea\x13Q2\x1c3\x1f\x05\x03wG\x12\x12'  #'8cfbfac78ad80e43259993621eaca66b07ff12ea1351321c331f050377471212'

    transaction = Transaction(safe_mock)
    transaction.calculate_hash()

    safe_mock.get_transaction_hash.assert_called_with(transaction)
    assert transaction.hash == b'\x8c\xfb\xfa\xc7\x8a\xd8\x0eC%\x99\x93b\x1e\xac\xa6k\x07\xff\x12\xea\x13Q2\x1c3\x1f\x05\x03wG\x12\x12'

def test_add_signatures():
    signatures = [
        {"v": 27, "r": 27555170324652676827630814712574958259239250774737836427766322829994538071693, "s": 53160465039259171157691482495637694636981072482605304137272964982625197154915},
        {"v": 28, "r": 54347870011433158865244599706051799377684047032440985438815293282093787507317, "s": 34908952815364364151308491742535206948994209196358987314910920659683592076947}
    ]

    transaction = Transaction(None)
    transaction.hash = b'\x8c\xfb\xfa\xc7\x8a\xd8\x0eC%\x99\x93b\x1e\xac\xa6k\x07\xff\x12\xea\x13Q2\x1c3\x1f\x05\x03wG\x12\x12'
    transaction.add_signatures(signatures)

    sorted_signatures = [
        {"v": 28, "r": 54347870011433158865244599706051799377684047032440985438815293282093787507317, "s": 34908952815364364151308491742535206948994209196358987314910920659683592076947},
        {"v": 27, "r": 27555170324652676827630814712574958259239250774737836427766322829994538071693, "s": 53160465039259171157691482495637694636981072482605304137272964982625197154915}
    ]
    assert transaction.signatures == sorted_signatures


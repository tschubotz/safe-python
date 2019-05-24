from commands import cli as safe_cli

test_address = '0x39cBD3814757Be997040E51921e8D54618278A08'
test_key = '0x9bb77243653b370165aa6d7c6e7826ba0b35b2ce76858ceba57d5decad557405'
test_mnemonic = 'abuse garden okay stuff mistake exotic vanish unlock certain erase female umbrella'


def test_network(runner):
    
    result = runner.invoke(safe_cli, ['-n'])
    assert result.exit_code == 2
    assert result.output == 'Error: -n option requires an argument\n'

    result = runner.invoke(safe_cli, ['--network'])
    assert result.exit_code == 2
    assert result.output == 'Error: --network option requires an argument\n'
import click
import web3
import json
from safe.utils import ADDRESS0, Operation, get_balance, code_exists
from safe import Safe
from ethereum import utils
import codecs

RPC_ENDPOINT_URL = 'https://rinkeby.infura.io/asdf'
# RPC_ENDPOINT_URL = 'http://localhost:8545'
SAFE_RELAY_URL = 'https://safe-relay.rinkeby.gnosis.pm'


class ChecksumAddressParamType(click.ParamType):
    name = 'checksum_address'

    def convert(self, value, param, ctx):
        if web3.Web3.isChecksumAddress(value):
            return value
        else:
            self.fail(
                '{} is not a valid checksum address'.format(value),
                param,
                ctx)

CHECKSUM_ADDRESS = ChecksumAddressParamType()
pass_safe = click.make_pass_decorator(Safe)


@click.group()
@click.argument('address', type=CHECKSUM_ADDRESS)
@click.version_option('0.0.2')
@click.pass_context
def cli(ctx, address):
    """Command line interface for the Gnosis Safe.
    """
    ctx.obj = Safe(address, RPC_ENDPOINT_URL, SAFE_RELAY_URL)


@cli.command()
@pass_safe
def info(safe):
    """Shows info about a Safe.
    This will show info such as balance, threshold and owners of a Safe.
    """
    # Get general things.
    click.echo('Safe at address: {}'.format(safe.address))
    click.echo('https://rinkeby.etherscan.io/address/{}\n'.format(
        safe.address))
    click.echo('ETH balance: {}\n'.format(safe.get_balance('ether')))

    # Owners
    owners = safe.get_owners()
    threshold = safe.get_threshold()
    click.echo('threshold/owners: {}/{}\n'.format(threshold, len(owners)))
    for i, owner in enumerate(owners):
        is_contract = code_exists(safe.w3, owner)
        owner_eth_balance = get_balance(safe.w3, owner, 'ether')
        click.echo('Owner {}: {} (code at address: {}, balance: {})'.format(
            i,
            owner,
            is_contract,
            owner_eth_balance))


@cli.command()
@pass_safe
def get_nonce(safe):
    """Show current nonce of the Safe.
    This will show the current nonce of the Safe.
    """
    for owner in safe.get_owners():
        click.echo(owner)


@cli.command()
@pass_safe
def get_owners(safe):
    """Lists all owners of a Safe.
    This will show the addresses of all owners.
    """
    for owner in safe.get_owners():
        click.echo(owner)


@cli.command()
@pass_safe
def get_threshold(safe):
    """Shows threshold of a Safe.
    This will the currently set threshold of the Safe.
    """
    click.echo(safe.get_threshold())


@cli.command()
@click.argument('to_address', type=CHECKSUM_ADDRESS)
@click.argument('ether_value', type=float)
@pass_safe
def transfer_ether(safe, to_address, ether_value):
    """asdf
    """
    # build tx and get tx hash
    transaction, transaction_hash = safe.build_transaction(safe.transfer_ether, to_address, ether_value)

    click.echo(transaction.transaction_semantics_text)

    click.echo('Gas price: {}\nsafeTxGas: {}\ndataGas: {}\nnonce: {}\n\n'.format(transaction.gas_price, transaction.safe_tx_gas, transaction.data_gas, transaction.nonce))

    # check how many signatures are required
    threshold = safe.get_threshold()
    
    click.echo('Threshold: {}\n Please sign: {}\n\n'.format(threshold, transaction_hash.hex()))
    signatures = []
    for i in range(threshold):
        signature = click.prompt('Signature {}/{}'.format(i+1, threshold)) # TODO validate format
        signatures.append(json.loads(signature))

    click.confirm('Good to go. Submit tx?')

    click.echo('https://rinkeby.etherscan.io/tx/{}'.format(safe.execute_transaction(transaction, signatures)['transactionHash']))


@cli.command()
@click.confirmation_option(help='Are you sure you want to delete the Safe?')
@pass_safe
def delete(safe):
    """Deletes a Safe.
    This will throw away the current Safe.
    """
    click.echo('You cannot delete a Safe. It will forever be on the blockchain! ¯\_(ツ)_/¯')

@cli.command()
@pass_safe
def sign(safe):
    """asdf
    """
    transaction_hash = click.prompt('Please enter transaction hash')
    transaction_hash = codecs.decode(transaction_hash, 'hex_codec')

    choice = click.prompt('What would you like to use for signing?\n(1) Private key\n(2) Account mnemonic\n(3) Safe mnemonic (Yields 2 signatures)\n', type=int)
    
    if choice == 1:
        private_key = click.prompt('Please enter private key (Input hidden)', hide_input=True)
    else:
        # TODO
        exit()

    v, r, s = utils.ecsign(transaction_hash, codecs.decode(private_key, 'hex_codec'))
    signature = {'v': v, 'r': r, 's': s}
    click.echo('Signature:\n\n{}'.format(json.dumps(signature)))
    

if __name__ == '__main__':
    # show_details()
    pass

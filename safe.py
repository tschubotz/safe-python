import click
import web3
from gnosis.safe.contracts import get_safe_contract

RPC_ENDPOINT_URL = 'https://rinkeby.infura.io/v3/c0ce0a963aa14e3898bd8525d3bdf682'


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


class Safe():
    def __init__(self, address):
        self.address = address


pass_safe = click.make_pass_decorator(Safe)


@click.group()
@click.argument('address', type=CHECKSUM_ADDRESS)
@click.version_option('0.0.1')
@click.pass_context
def cli(ctx, address):
    """Command line interface for the Gnosis Safe.
    """
    ctx.obj = Safe(address)


@cli.command()
@pass_safe
def info(safe):
    """Shows info about a Safe.
    This will show info such as balance, threshold and owners of a Safe.
    """
    w3 = web3.Web3(web3.HTTPProvider(RPC_ENDPOINT_URL))

    # Get general things.
    click.echo('Safe at address: {}'.format(safe.address))
    click.echo('https://rinkeby.etherscan.io/address/{}\n'.format(
        safe.address))
    eth_balance = w3.eth.getBalance(safe.address)
    click.echo('ETH balance: {}\n'.format(w3.fromWei(eth_balance, 'ether')))

    # Owners
    safe_contract = get_safe_contract(w3=w3, address=safe.address)
    owners = safe_contract.functions.getOwners().call()
    threshold = safe_contract.functions.getThreshold().call()
    click.echo('threshold/owners: {}/{}\n'.format(threshold, len(owners)))
    for i, owner in enumerate(owners):
        code_exists = (len(w3.eth.getCode(owner)) != 0)
        owner_eth_balance = w3.eth.getBalance(owner)
        click.echo('Owner {}: {} (code at address: {}, balance: {})'.format(
            i,
            owner,
            code_exists,
            owner_eth_balance))


@cli.command()
@click.confirmation_option(help='Are you sure you want to delete the Safe?')
@pass_safe
def delete(safe):
    """Deletes a Safe.
    This will throw away the current Safe.
    """
    click.echo('You cannot delete a Safe. It will forever be on the blockchain! ¯\_(ツ)_/¯')


if __name__ == '__main__':
    # show_details()
    pass

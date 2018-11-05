import click
import web3
from safe import Safe, get_balance, code_exists

RPC_ENDPOINT_URL = 'https://rinkeby.infura.io/asdfasdf'


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
    ctx.obj = Safe(address, RPC_ENDPOINT_URL)


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
    safe.transfer_ether(to_address, ether_value, [])


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

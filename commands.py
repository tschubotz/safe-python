import click
import web3
import json
from safe.utils import ADDRESS0, Operation, get_balance, code_exists, get_account_info_from_mnemonic
from safe import Safe
from ethereum.utils import ecsign
import codecs
from bip44.crypto import HDPrivateKey, HDKey
from eth_account.account import Account

INFURA_KEY = ''

ENVS = {
    'mainnet': {
        'name': 'Ethereum mainnet',
        'rpc_endpoint_url': 'https://mainnet.infura.io/{}'.format(INFURA_KEY),
        'safe_relay_url': 'https://safe-relay.gnosis.pm', 
        'etherscan_url': 'https://etherscan.io'
    },
    'rinkeby': {
        'name': 'Rinkeby testnet',
        'rpc_endpoint_url': 'https://rinkeby.infura.io/{}'.format(INFURA_KEY),
        'safe_relay_url': 'https://safe-relay.rinkeby.gnosis.pm', 
        'etherscan_url': 'https://rinkeby.etherscan.io'
    }    
}


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
@click.option('-n', '--network', type=click.Choice(['mainnet', 'rinkeby']))
@click.version_option('0.0.3')
@click.pass_context
def cli(ctx, address, network):
    """Command line interface for the Gnosis Safe.
    """
    if not network:
        network = 'mainnet'  

    env = ENVS[network]

    click.echo('\nYou are using: {}\n\n'.format(env['name']))

    ctx.obj = Safe(network, address, env['rpc_endpoint_url'], env['safe_relay_url'])


@cli.command()
@pass_safe
def info(safe):
    """Shows info about a Safe.
    This will show info such as balance, threshold and owners of a Safe.
    """
    # Get general things.
    click.echo('Safe at address: {}'.format(safe.address))
    click.echo('{}/address/{}\n'.format(
        ENVS[safe.network]['etherscan_url'], safe.address))
    click.echo('ETH balance: {}\n'.format(safe.get_balance('ether')))
    
    # Is there even code at the address?
    if not code_exists(safe.w3, safe.address):
        click.echo('No code found at provided address. Are you sure that you are on the right network?')
        exit()

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
    """Transfer ether to an account.
    This will transfer the given amount of ether from the Safe to another account.
    """
    safe_tx(safe, safe.transfer_ether_tx, to_address, ether_value)


@cli.command()
@click.argument('owner_address', type=CHECKSUM_ADDRESS)
@click.argument('threshold', type=int)
@pass_safe
def owner_add(safe, owner_address, threshold):
    """Add owner to a Safe.
    This will add an owner to the Safe.
    """
    safe_tx(safe, safe.owner_add_tx, owner_address, threshold)
    

@cli.command()
@click.argument('owner_address', type=CHECKSUM_ADDRESS)
@click.argument('threshold', type=int)
@pass_safe
def owner_remove(safe, owner_address, threshold):
    """Remove owner from a Safe.
    This will remove an owner from the Safe.
    """
    safe_tx(safe, safe.owner_remove_tx, owner_address, threshold)


@cli.command()
@click.argument('old_owner_address', type=CHECKSUM_ADDRESS)
@click.argument('new_owner_address', type=CHECKSUM_ADDRESS)
@pass_safe
def owner_swap(safe, old_owner_address, new_owner_address):
    """Swap owners of a Safe.
    This will replace an existing owner of the Safe with a new one.
    """
    safe_tx(safe, safe.owner_swap_tx, old_owner_address, new_owner_address)


@cli.command()
@click.argument('threshold', type=int)
@pass_safe
def owner_change_threshold(safe, threshold):
    """Change confirmation threshold of a Safe.
    This will change the number of confirmations required to make a transaction with the Safe.
    """
    safe_tx(safe, safe.owner_change_threshold_tx, threshold)
 

def safe_tx(safe, function, *params):
    # build tx and get tx hash
    transaction = safe.build_transaction(function, *params)

    click.echo(transaction.transaction_semantics_text)

    click.echo('\nGas price: {}\nsafeTxGas: {}\ndataGas: {}\nnonce: {}\n\n'.format(transaction.gas_price, transaction.safe_tx_gas, transaction.data_gas, transaction.nonce))

    # check how many signatures are required
    threshold = safe.get_threshold()
    
    click.echo('Threshold: {}\n Please sign: {}\n\n'.format(threshold, transaction.hash.hex()))
    signatures = []
    for i in range(threshold):
        signature = click.prompt('Signature {}/{}'.format(i+1, threshold)) # TODO validate format
        signatures.append(json.loads(signature))

    click.confirm('Good to go. Submit tx?')
    
    click.echo('{}/tx/{}'.format(ENVS[safe.network]['etherscan_url'], safe.execute_transaction(transaction, signatures)['transactionHash']))


@cli.command()
@click.confirmation_option(help='Are you sure you want to delete the Safe?')
@pass_safe
def delete(safe):
    """Deletes a Safe.
    This will throw away the current Safe.
    """
    click.echo('You cannot delete a Safe. It will forever be on the blockchain! ¯\_(ツ)_/¯')

@cli.command()
@click.option('--multi', is_flag=True, help='Ask for multiple signatures until threshold. Comes in handy when signing multiple owners on one machine.')
@pass_safe
def sign(safe, multi):
    """Sign transation of a Safe.
    This will sign a given transaction hash and return the signature.
    """
    transaction_hash = click.prompt('Please enter transaction hash')
    transaction_hash = codecs.decode(transaction_hash, 'hex_codec')

    choice = click.prompt('What would you like to use for signing?\n(1) Private key\n(2) Account mnemonic\n(3) Safe mnemonic (Yields 2 signatures)\n', type=int)
    
    loops = 1 if not multi else safe.get_threshold()

    account_info = []

    while loops > 0:
        if choice == 1:
            private_key = click.prompt('Please enter private key (Input hidden)', hide_input=True)
            
            address = Account.privateKeyToAccount(private_key).address
            account_info.append((private_key, address))
        elif choice == 2:
            mnemonic = click.prompt('Please enter account mnemonic (Input hidden)', hide_input=True)
            account_info.append(get_account_info_from_mnemonic(mnemonic))
        else:
            mnemonic = click.prompt('Please enter Safe mnemonic (Input hidden)', hide_input=True)
            account_info.append(get_account_info_from_mnemonic(mnemonic, index=0))
            account_info.append(get_account_info_from_mnemonic(mnemonic, index=1))

        for i, info in enumerate(account_info):
            loops -= 1
            private_key = info[0]
            address = info[1]
            v, r, s = ecsign(transaction_hash, codecs.decode(private_key, 'hex_codec'))
            signature = {'v': v, 'r': r, 's': s}
            click.echo('Signature {} ({}):\n\n{}'.format(i, address, json.dumps(signature)))
    

if __name__ == '__main__':
    # show_details()
    pass

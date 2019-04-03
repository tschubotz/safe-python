# safe-python
```
$ pip install --editable .
```

```
$ safe --help
Usage: safe [OPTIONS] ADDRESS COMMAND [ARGS]...

  Command line interface for the Gnosis Safe.

Options:
  -n, --network [mainnet|rinkeby]
  --version                       Show the version and exit.
  --help                          Show this message and exit.

Commands:
  delete                  Deletes a Safe.
  get_nonce               Show current nonce of the Safe.
  get_owners              Lists all owners of a Safe.
  get_threshold           Shows threshold of a Safe.
  info                    Shows info about a Safe.
  owner_add               Add owner to a Safe.
  owner_change_threshold  Change confirmation threshold of a Safe.
  owner_remove            Remove owner from a Safe.
  owner_swap              Swap owners of a Safe.
  sign                    Sign transation of a Safe.
  transfer_ether          Transfer ether to an account```

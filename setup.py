from setuptools import setup, find_packages

setup(
    name='safe',
    version='0.0.3',
    packages=find_packages(),
    install_requires=[
        'click',
        'gnosis-py',
        'web3',
        'requests',
        'rlp',
        'eth_utils',
        'two1',
        'pycrypto',
        'pycryptodome',
    ],
    entry_points='''
        [console_scripts]
        safe=commands:cli
    ''',
)
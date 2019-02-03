from setuptools import setup, find_packages

setup(
    name='safe',
    version='0.0.2',
    packages=find_packages(),
    install_requires=[
        'click',
        'gnosis-py',
        'web3',
        'requests'
    ],
    entry_points='''
        [console_scripts]
        safe=commands:cli
    ''',
)
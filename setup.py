from setuptools import setup

setup(
    name='safe',
    version='0.0.1',
    py_modules=['safe'],
    install_requires=[
        'click',
        'gnosis-py',
        'web3'
    ],
    entry_points='''
        [console_scripts]
        safe=safe:cli
    ''',
)
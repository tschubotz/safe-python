from setuptools import setup, find_packages

setup(
    name='safe',
    version='0.0.3',
    packages=find_packages(),
    install_requires=[
        'requests==2.21.0',
        'click==6.6',
        'gnosis-py==0.12.3',
        'web3==4.8.2',
        'bip44@git+https://git@github.com/tschubotz/ethereum-bip44-python@master',
    ],
    tests_require=[
        'pytest',
        'pytest-mock',
    ],
    setup_requires=[
        'pytest-runner',
    ],
    entry_points='''
        [console_scripts]
        safe=commands:cli
    ''',
)

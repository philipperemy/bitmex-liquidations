from setuptools import setup

setup(
    name='bitmex-liquidation',
    version='1.0.1',
    description='BitMEX Liquidation Python Wrapper',
    author='Philippe Remy',
    license='MIT',
    long_description_content_type='text/markdown',
    long_description=open('README.md').read(),
    packages=['bitmex_liquidation'],
    install_requires=['websocket-client==0.47.0']
)

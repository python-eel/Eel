from setuptools import setup

setup(
    name='Eel',
    version='0.2.0',
    author='Chris Knott',
    packages=['eel'],
    package_data={
        'eel': ['eel.js'],
    },
    install_requires=['bottle', 'bottle-websocket'],
    long_description=open('README.md', encoding='utf-8').read(),
    keywords=['gui', 'html', 'javascript', 'electron'],
)
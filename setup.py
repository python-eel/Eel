from setuptools import setup

setup(
    name='Eel',
    version='0.6.1',
    author='Chris Knott',
    author_email='chrisknott@hotmail.co.uk',
    packages=['eel'],
    package_data={
        'eel': ['eel.js'],
    },
    install_requires=['bottle', 'bottle-websocket'],
    description='For little HTML GUI applications, with easy Python/JS interop',
    long_description=open('README.md', encoding='utf-8').readlines()[1],
    keywords=['gui', 'html', 'javascript', 'electron'],
)
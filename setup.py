from io import open
from setuptools import setup

setup(
    name='Eel',
    version='1.0.0-a1',
    author='Chris Knott',
    author_email='chrisknott@hotmail.co.uk',
    packages=['eel'],
    package_data={
        'eel': ['eel.js'],
    },
    install_requires=['bottle', 'bottle-websocket', 'future', 'whichcraft'],
    python_requires='>=2.6',
    description='For little HTML GUI applications, with easy Python/JS interop',
    long_description=open('README.md', encoding='utf-8').readlines()[2],
    keywords=['gui', 'html', 'javascript', 'electron'],
    homepage='https://github.com/ChrisKnott/Eel',
)

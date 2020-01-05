from io import open
from setuptools import setup

with open('README.md') as read_me:
    long_description = read_me.read()

setup(
    name='Eel',
    version='0.12.2',
    author='Chris Knott',
    author_email='chrisknott@hotmail.co.uk',
    url='https://github.com/samuelhwilliams/Eel',
    packages=['eel'],
    package_data={
        'eel': ['eel.js'],
    },
    install_requires=['bottle', 'bottle-websocket', 'future', 'whichcraft'],
    python_requires='>=2.6',
    description='For little HTML GUI applications, with easy Python/JS interop',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=['gui', 'html', 'javascript', 'electron'],
)

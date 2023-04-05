from io import open
from setuptools import setup

with open('README.md') as read_me:
    long_description = read_me.read()

setup(
    name='Eel',
    version='0.16.0',
    author='Python Eel Organisation',
    author_email='python-eel@protonmail.com',
    url='https://github.com/python-eel/Eel',
    packages=['eel'],
    package_data={
        'eel': ['eel.js', 'py.typed'],
    },
    install_requires=['bottle', 'bottle-websocket', 'future', 'pyparsing'],
    extras_require={
        "jinja2": ['jinja2>=2.10']
    },
    python_requires='>=3.7',
    description='For little HTML GUI applications, with easy Python/JS interop',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=['gui', 'html', 'javascript', 'electron'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'License :: OSI Approved :: MIT License',
    ],
)

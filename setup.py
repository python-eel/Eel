from io import open
from setuptools import setup, find_packages

with open('README.md') as read_me:
    long_description = read_me.read()

dependencies = [
    'bottle',
    'bottle-websocket',
    'future',
    'pyparsing',
    'whichcraft',
]

setup(
    name='Paling',
    version='0.16.2',
    author='OpenSource Team - Roborian',
    author_email='info@roborian.com',
    url='https://github.com/python-paling/Paling',
    packages=find_packages(),
    package_data={
        'paling': ['paling.js', 'py.typed'],
    },
    install_requires=dependencies,
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
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'License :: OSI Approved :: MIT License',
    ],
    license='MIT',
)

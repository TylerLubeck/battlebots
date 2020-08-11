# -*- coding: utf-8 -*-
from setuptools import setup


install_requires = [
    'docker>=4.2.2,<5.0.0',
    'typer>=0.3.1,<0.4.0'
]

entry_points = {
    'console_scripts': [
        'battlebots = battlebots.__main__:entry'
    ]
}

setup_kwargs = {
    'name': 'battlebots',
    'version': '0.1.0',
    'description': 'BagelCon Battlebots Runner',
    'long_description': 'The Battlebots runner',
    'author': 'Tyler Lubeck',
    'author_email': 'tyler@tylerlubeck.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': '',
    'package_dir': {'': 'src'},
    'packages': ['battlebots'],
    'package_data': {'': ['*']},
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

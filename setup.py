# -*- coding: utf-8 -*-
from setuptools import setup


install_requires = [
    'colorama>=0.4.3,<=0.5.0',
    'docker>=4.2.2,<5.0.0',
    'typer>=0.3.1,<0.4.0',
    'pillow>=7.2.0<8.0.0',
]

entry_points = {
    'console_scripts': [
        'battlebots = battlebots.__main__:main'
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

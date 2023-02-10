#!/usr/bin/env python
"""Setup pygments-pgdl-lexer."""
from setuptools import setup, find_packages

entry_points = '''
[pygments.lexers]
pgdl=pygments_pgdl:PGDLLexer
'''

setup(
    name='pygments-pgdl-lexer',
    version='1.0.0',
    description='Pygments lexer package for PGDL',
    author='Mira Weller',
    author_email='mira@teamwiki.de',
    url='https://github.com/luelista/pygments-pgdl-lexer',
    packages=find_packages(),
    entry_points=entry_points,
    install_requires=[
        'Pygments>=2.0.1',
		'lark>=1.1.5',
    ],
    zip_safe=True,
    license='GPLv3 License',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Filters',
        'Topic :: Text Processing :: Markup :: HTML'
    ]
)
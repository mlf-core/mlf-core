#!/usr/bin/env python

"""The setup script."""

import os
import {{cookiecutter.project_slug|replace('-', '_')}} as module
from setuptools import setup, find_packages


def walker(base, *paths):
    file_list = set([])
    cur_dir = os.path.abspath(os.curdir)

    os.chdir(base)
    try:
        for path in paths:
            for dname, dirs, files in os.walk(path):
                for f in files:
                    file_list.add(os.path.join(dname, f))
    finally:
        os.chdir(cur_dir)

    return list(file_list)


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('CHANGELOG.rst') as history_file:
    history = history_file.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup_requirements = 'pytest-runner'

test_requirements = 'pytest'

{%- set license_classifiers = {
    'MIT': 'License :: OSI Approved :: MIT License',
    'BSD': 'License :: OSI Approved :: BSD License',
    'ISC': 'License :: OSI Approved :: ISC License (ISCL)',
    'Apache2.0': 'License :: OSI Approved :: Apache Software License',
    'GNUv3': 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
} %}

setup(
    author="{{ cookiecutter.full_name.replace('\"', '\\\"') }}",
    author_email='{{ cookiecutter.email }}',
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
{%- if cookiecutter.license in license_classifiers %}
        '{{ license_classifiers[cookiecutter.license] }}',
{%- endif %}
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    description="{{ cookiecutter.project_short_description }}",
    entry_points={
        'console_scripts': [
            '{{ cookiecutter.project_name }}={{ cookiecutter.project_slug|replace('-', '_') }}.cli_{% if cookiecutter.framework == 'pytorch' -%}pytorch{% elif cookiecutter.framework == 'tensorflow' -%}tensorflow{% elif cookiecutter.framework == 'xgboost' -%}xgboost{% endif %}:main',
        ],
    },
    install_requires=requirements,
{%- if cookiecutter.license in license_classifiers %}
    license="{{ cookiecutter.license }}",
{%- endif %}
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='{{ cookiecutter.project_slug }}',
    name='{{ cookiecutter.project_name }}',
    packages=find_packages(include=['{{ cookiecutter.project_slug_no_hyphen }}', '{{ cookiecutter.project_slug_no_hyphen }}.*']),
    package_data={
        module.__name__: walker(
            os.path.dirname(module.__file__),
            'models', 'data'
        ),
    },
    setup_requires=setup_requirements,
    tests_require=test_requirements,
    url='https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}',
    version='{{ cookiecutter.version }}',
    zip_safe=False,
)

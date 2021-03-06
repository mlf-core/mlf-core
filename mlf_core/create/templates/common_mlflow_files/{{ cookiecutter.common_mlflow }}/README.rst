{% set is_open_source = cookiecutter.license != 'Not open source' -%}
{% for _ in cookiecutter.project_name %}={% endfor %}
{{ cookiecutter.project_name }}
{% for _ in cookiecutter.project_name %}={% endfor %}

.. image:: https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/workflows/Train%20{{ cookiecutter.project_slug }}%20using%20CPU/badge.svg
        :target: https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/actions?query=workflow%3A%22Train+{{ cookiecutter.project_slug }}+using+CPU%22
        :alt: Github Workflow CPU Training {{ cookiecutter.project_name }} Status

.. image:: https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/workflows/Publish%20Container%20to%20Docker%20Packages/badge.svg
        :target: https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/actions?query=workflow%3A%22Publish+Container+to+Docker+Packages%22
        :alt: Publish Container to Docker Packages

.. image:: https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/workflows/mlf-core%20linting/badge.svg
        :target: https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/actions?query=workflow%3A%22mlf-core+lint%22
        :alt: mlf-core lint

{% if is_open_source %}
.. image:: https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/actions/workflows/publish_docs.yml/badge.svg
        :target: https://{{ cookiecutter.github_username }}.github.io/{{ cookiecutter.project_name }}
        :alt: Documentation Status
{%- endif %}

{{ cookiecutter.project_short_description }}

Features
--------

* Fully reproducible mlf-core {{ cookiecutter.framework }} model
* MLF-CORE TODO: Write features here


Credits
-------

This package was created with `mlf-core`_ using Cookiecutter_.

.. _mlf-core: https://mlf-core.readthedocs.io/en/latest/
.. _Cookiecutter: https://github.com/audreyr/cookiecutter

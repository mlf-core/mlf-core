{% set is_open_source = cookiecutter.license != 'Not open source' -%}
{% for _ in cookiecutter.project_name %}={% endfor %}
{{ cookiecutter.project_name }}
{% for _ in cookiecutter.project_name %}={% endfor %}

.. image:: https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/workflows/Train%20{{ cookiecutter.project_slug }}%20using%20CPU/badge.svg
        :target: https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/workflows/Train%20{{ cookiecutter.project_slug }}%20using%20CPU/badge.svg
        :alt: Github Workflow CPU Training {{ cookiecutter.project_name }} Status

{% if is_open_source %}
.. image:: https://readthedocs.org/projects/{{ cookiecutter.project_name }}/badge/?version=latest
        :target: https://{{ cookiecutter.project_name }}.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status
{%- endif %}

{{ cookiecutter.project_short_description }}

{% if is_open_source %}
* Free software: {{ cookiecutter.license }}
* Documentation: https://{{ cookiecutter.project_slug | replace("_", "-") }}.readthedocs.io.
{% endif %}

Features
--------

* Fully reproducible mlf-core Tensorflow model
* MLF-CORE TODO: Write features here


Credits
-------

This package was created with `mlf-core`_ using Cookiecutter_.

.. _mlf-core: https://mlf-core.readthedocs.io/en/latest/
.. _Cookiecutter: https://github.com/audreyr/cookiecutter

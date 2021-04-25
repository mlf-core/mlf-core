Welcome to {{ cookiecutter.project_name }}'s documentation!
======================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   readme
   {% if cookiecutter.domain == 'package' -%}installation.rst{% endif %}
   usage
   {% if cookiecutter.domain == 'mlflow' -%}model{% endif %}
   authors
   changelog
   code_of_conduct

Indices and tables
==================
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

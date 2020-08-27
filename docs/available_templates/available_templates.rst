.. _available_templates:

=========================
Available templates
=========================

cookietemple currently has the following templates available:

1. `mlflow-pytorch`_
2. `mlflow-tensorflow`_
3. `mlflow-xgboost`_
4. `mlflow-xgboost_dask`_

In the following every template is devoted its own section, which explains its purpose, design, included frameworks/libraries, usage and frequently asked questions.
A set of frequently questions, which all templates share see here: :ref:`all_templates_faq` FAQ.
It is recommended to use the sidebar to navigate this documentation, since it is very long and cumbersome to scroll through.

.. include:: mlflow_pytorch.rst
.. include:: mlflow_tensorflow.rst
.. include:: mlflow_xgboost.rst
.. include:: mlflow_xgboost_dask.rst

.. _all_templates_faq:

Shared FAQ
----------------------

How do I access my data when running inside a Docker container?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

mlf-core projects by default mount ``/data`` to ``/data`` inside the Docker container. Hence, add a ``/data`` folder and access the files by assuming that the files are in ``/data``.

How do I setup Read the Docs?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

cookietemple ships with a full, production ready `Read the Docs <https://readthedocs.org/>`_ setup.
You need to `import your documentation <https://docs.readthedocs.io/en/stable/intro/import-guide.html>`_ on Read the Docs website.
Do not forget to sync your account first to see your repository.

What is Dependabot and how do I set it up?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

`Dependabot <https://dependabot.com/>`_ is a service, which (for supported languages) automatically submits pull requests for dependency updates.
cookietemple templates ship with dependabot configurations, if the language is supported by Dependabot.
To enable Dependabot you need to login (with your Github account) and add your repository (or enable Dependabot for all repositories).
Note that you need to do this for every organization separately. Dependabot will then pick up the configuration and start submitting pull requests!

How do I add a new template?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Please follow :ref:`adding_templates`.

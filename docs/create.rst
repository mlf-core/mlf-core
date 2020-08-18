.. _create:

================
Create a project
================

| Creating projects from templates is the heart of mlf-core.
| To learn more about our templates please visit :ref:`available_templates` and check out your template of interest.

The creation of a new project can be invoked by

.. code-block:: console

    $ mlf-core create

which will guide you through the creation process of your (customized) project via prompts. If you do not have a mlf-core config yet, you will be asked to create one first.
The full name, email and possibly more information set during the configuration process is required when creating the project. For more details please visit :ref:`config`.
The prompts follow the pattern of domain (e.g. mlflow), subdomain (if applicable, e.g. machine_learning), language/framework (e.g. pytorch) followed by template specific prompts (e.g. Dask).
| The template will be created at the current working directory, where mlf-core has been called.

It is also possible to directly create a specific template using its handle

.. code-block:: console

    $ mlf-core create --handle <HANDLE>

| After the template has been created, linting (see :ref:`lint`) is automatically performed to verify that the template creation process was successful.
| You may already be made aware of any TODOs, which you should examine before coding your project.
| Finally, you will be asked whether or not you want to automatically push your new project to Github. For more details about the Github support please visit :ref:`github_support`.
| Note that in order to use the automatic Github repo creation feature, you need to set a personal access token via :code:`mlf-core config pat` (if not already done). This token is also used for mlf-core's sync feature.
| Take a look at `the Github docs <https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token>`_ to see, how to create a personal access token for your Github account.

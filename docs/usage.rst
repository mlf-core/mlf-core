=============
General Usage
=============

In the following an overview of mlf-core's main commands is given.
Please note that all commands are explained more in depth in their respective documentation point. You can use the menu on the left to navigate to them.

create
------

:code:`create` is the heart of mlf-core.
It starts the project creation process and guides the user through domain selection, language/framework selection and prompts for all required configuration parameters such as name, email and many more.
Additionally, the project is linted after creation to ensure that everything went well.
The user also has the option to push his just created project directly to Github.
Invoke :code:`create` by running

.. code-block:: console

    $ mlf-core create

For more details about project creation please visit :ref:`create` and for a detailed list of all available templates please visit :ref:`available_templates`.

list
----

:code:`list` allows you to list all available templates.
The list command prints the name, handle, short description, available libraries for the template and its version to the console.
Note that the long description is emitted and the :code:`info` command should be used to get a long description of the template.
Invoke :code:`list` by running

.. code-block:: console

    $ mlf-core list

For more details please visit :ref:`list_info`.

info
----

:code:`info` provides detailed information about a specific template or set of templates.
It prints the name, handle, long description, available libraries and version of the selected subset or specific template.
Invoke :code:`info` by running

.. code-block:: console

    $ mlf-core info <HANDLE>

For more details please visit :ref:`list_info`.

lint
----

:code:`lint` ensures that the template adheres to mlf-core's standards.
When linting an already existing project several general checks, which all templates share are performed and afterwards template specific linting functions are run.
All results are collected and printed to the user. If any of the checks fail linting terminates.
Invoke :code:`lint` by running

.. code-block:: console

    $ mlf-core lint

For more details please visit :ref:`lint`.

bump-version
------------

:code:`bump-version` conveniently bumps the version of a mlf-core based project across several files.
Default configurations for :code:`bump-version` are shipped with the template and can be extended if the user so desires.
All lines where the version was changed are printed to the console.
Invoke :code:`bump-version` by running

.. code-block:: console

    $ mlf-core bump-version <NEWVERSION> <PATH>

For more details please visit :ref:`bump-version`.

sync
----

:code:`sync` checks for a project whether a newer version of the used template is available.
If so, a pull request with only the changes of the newer template version is created against the development/last active branchh.
Invoke :code:`sync` by running

.. code-block:: console

    $ mlf-core sync

For more details please visit :ref:`sync`.

config
--------

:code:`config` sets commonly used defaults for the project creation.
Moreover, it is required for mlf-core's Github support, since it takes care of the personal access token (PAT).
Invoke :code:`config` by running

.. code-block:: console

    $ mlf-core config <all/general/pat>

For more details please visit :ref:`config` and :ref:`github_support`.

upgrade
---------

:code:`upgrade` checks whether a new version is available on PyPI and upgrades the version if not.
Invoke :code:`upgrade` by running

.. code-block:: console

   $ mlf-core upgrade

For more details please visit :ref:`upgrade`.

External Python based projects
------------------------------

To use mlf-core in an external Python based project

.. code-block:: python

    import mlf_core

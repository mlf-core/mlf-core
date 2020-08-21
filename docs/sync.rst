.. _sync:

=======================
Syncing your project
=======================

Syncing is supposed to integrate any changes to the mlf-core templates back into your already existing project.

Overview
----------

When ``mlf-core sync`` is invoked, mlf-core checks whether a new version of the corresponding template for the current project is available.
If so, mlf-core now creates a temporary project with the most recent template and pushes it to the ``TEMPLATE`` branch.
Next, a pull request is submitted to the ``development`` or most recently used branch.
The syncing process is configurable by setting the desired lower syncing boundary level and blacklisting files from syncing (see :ref:`sync_config`.

Requirements for sync
------------------------

For syncing to work properly, your project has to satisfy a few things:

 1.) A Github repository with your projects code (private or public, organization or non-organization repository).

 2.) An unmodified ``.mlf-core.yml`` file (if you modified this file, what you should never do, syncing may not be able to recreate the project with the most recent template.

 3.) A running, unmodified workflow called :code:`sync.yml`. Modifying this workflow should never be done and results in undefined sync behaviour.

 4.) An active repository secret called :code:`MLF_CORE_SYNC_TOKEN` for your project's repository containing the encrypted personal access token with at least :code:`repo` scope.

 5.) It is strongly advised not to touch the ``TEMPLATE`` branch.

How to use sync?
----------------

The ``sync`` command from mlf-core has a few options to run with. For a first overview see ``$ mlf-core sync --help``.
Note that you never need to run ``mlf-core sync`` manually with the workflow, but you can do any time if you want.

What command line options are available?
-----------------------------------------
The basic sync command syntax is: ``$ mlf-core sync [PROJECT_DIR] --set-token ([PAT] [GITHUB_USERNAME]) --check-update``

Running sync manually on an active mlf-core project with a Github repo, you should never ever have to set the ``PAT`` or ``GITHUB_USERNAME``. These
are options that are only required for the ``sync_project`` workflow for automatic syncing.
So: **You never need to care about these parameters when calling mlf-core sync manually**.

An important parameter is ``PROJECT_DIR``. This parameter contains the (relative) path to the mlf-core projects top level directory, you would like to sync.
Per default, this one is set to the current working directory. So, for example, if your current working directory is like ``/home/homersimpson/projects`` and you would like to sync
your project named ``ExplodingSpringfield`` located in ``/home/homersimpson/projects`` you need to call ``$ mlf-core sync ExplodingSpringfield/``.
This one should be always set (unless your current working directory is the top level directory of the project you'd like to sync).

Next, ``sync`` provides two flags: ``$ mlf-core sync [PROJECT_DIR] --set-token`` can be used to update your ``MLF_CORE_SYNC_TOKEN``, which mlf-core uses
to sync your project (especially when syncing with the workflow). This could be useful, for example, when the ownership of a repo had changed.

The ``--check_update`` flag, called via ``$ mlf-core sync [PROJECT_DIR] --check-update``, can be used for manually checking whether a new version for your template has been released by mlf-core.
Note that when you call ``$ mlf-core sync [PROJECT_DIR]`` mlf-core also runs this check, but then process with syncing rather than exiting.

What happens when my project gets synced?
-------------------------------------------
Syncing can happen via two ways: One way is when you call ``$ mlf-core sync [PROJECT_DIR]`` manually from your command line.
This way, mlf-core checks whether a new version has been released or not, and if so, creates a pull request with all changes (excluding blacklisted files) from the ``TEMPLATE`` branch to your
current working branch.

The other way would be via the ``sync_project.yml`` workflow. This workflow triggers on push everytime you push changes to your repository. You can safely modify this behaviour to only trigger
this workflow for example when a PR is created. The result is the same like above but you don't need to remember to run sync manually on a regulary basis.

Note that the PR is currently automatically created by the one who initially created/owns this repository.

Configuring sync
-----------------------

.. _sync_config:

Sync level
++++++++++++

Since mlf-core strongly adheres to semantic versioning our templates do so as well.
Hence, it is customizable whether only major, minor or all (=patch level) releases of the template should trigger mlf-core sync.
The sync level therefore specifies a lower boundary. It can be configured in the::

    [sync_level]
    ct_sync_level = minor

section.

Blacklisting files
++++++++++++++++++++++

Although, mlf-core only submits pull requests for files, which are part of the template sometimes even those files should be ignored.
Examples could be any html files, which at some point contain only custom content and should not be synced.
When syncing, mlf-core examines the ``mlf-core.cfg`` file and ignores any file patterns (e.g. ``*.html``) below the ``[sync_files_blacklisted]`` section.

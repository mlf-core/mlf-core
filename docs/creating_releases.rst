.. _creating_releases:

=====================
Creating Releases
=====================

This document serves as a guideline on how to create releases of your project.
Additionally, it may provide pointers about best practices and development workflows.

| Assuming that you start on the development branch with a ``x.x.x-SNAPSHOT`` version, you should ensure that your changelog is complete.
| The next step is then to bump your version to a release version:

.. code-block:: console

    $ mlf-core bump-version x.x.x .

| Then create a ``release/x.x.x branch`` and submit a pull request from it against the ``master`` branch.
| Any people that you have worked with including yourself should now review this pull request and fix and remaining issues.
| After pull request approval you merge the pull request into the ``master`` branch. Afterwards create a release on Github with the tag x.x.x and insert your changelog into the description and add any additional details that you deem important. A new Docker container should now be building with the latest version.
| Switch back to the ``development`` branch and merge the latest ``master`` branch into it. Next, according to semantic versioning and your planned features bump the version to a higher ``-SNAPSHOT`` version. The changelog will automatically add sections.

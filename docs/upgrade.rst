.. _upgrade:

=====================
Upgrade mlf-core
=====================

Every time mlf-core is run it will automatically contact PyPI to check whether the locally installed version of mlf-core is the latest version available.
If not

.. code:: console

    $ mlf-core upgrade

can be run. The command calls `pip <https://pypi.org/project/pip/>`_ in upgrade mode to upgrade mlf-core to the latest version.
For this to work however, it is required that pip is accessible from your PATH.

It is advised not to mix installations using setuptools directly and pip. If you are not a developer of mlf-core this should not concern you.

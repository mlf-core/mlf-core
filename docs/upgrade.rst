.. _upgrade:

=====================
Upgrade mlf-core
=====================

Every time mlf-core is run it will automatically contact PyPI to check whether the locally installed version of mlf-core is the latest version available.
If a new version is available mlf-core can be trivially upgraded. Note that ``pip`` must be available in your ``PATH``.
It is advised not to mix installations using setuptools directly and pip. If you are not a developer of mlf-core this should not concern you.

Usage
--------

.. code-block::

    $ mlf-core upgrade

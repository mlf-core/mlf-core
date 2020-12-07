.. _fix-artifact-paths:

==============================================
Fixing the paths of locally saved MLflow runs
==============================================

Often times the development and the training machines are not the same.
However, when trying to view the artifacts on the development machine, the paths to the artifacts defined in the ``meta.yaml`` files do not match anymore.
This is only of concern when saving artifacts locally and not remotely to for example AWS S3.
To automatically fix the paths locally mlf-core offers a ``fix-artifact-paths`` command.

Usage
-------

To fix the paths run

.. code-block:: console

    $ mlf-core fix-artifact-paths <PATH>

- ``PATH`` is the root folder of the ``mlruns`` directory

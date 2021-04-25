.. _config:

=======================
Configure mlf-core
=======================

To prevent frequent prompts for information, which rarely or never changes at all such as the full name, email or Github username of the user, mlf-core uses a configuration file.
Moreover, the personal access token associated with the Github username is stored, in encrypted form, to allow for various Github functionalities, such as automatic Github repository creation or :ref:`sync`.
The creation of projects with mlf-core requires a configuration file. A personal access token is not required, if Github support is not used.
The configuration file is saved operating system dependent in common config file locations (``~/.config/mlf-core`` on Unix, ``C:\Users\Username\AppData\Local\mlf-core\mlf-core`` on Windows).
Configuring mlf-core is only required once, although it is always possible to update the current configuration.

Usage
-------

Invoke mlf-core config *via*

.. code-block:: console

    $ mlf-core config <all/general/pat>

- ``all`` : Prompt for the full name, email, Github username and Github personal access token.

- ``general`` : Only prompt for the full name, email and the Github username.

  These details are required to create projects.

- ``pat`` : Solely prompts for the Github personal access token and updates it if already set.

  Ensure that your Github username still matches with the new personal access token.
  If not you should also update your Github username *via* ``mlf-core config general``. Additionally, any of your already created projects may still feature your old token and you may therefore run into issues when attempting to push.
  Hence, you must also `update your remote URL <https://help.github.com/en/github/using-git/changing-a-remotes-url>`_ for those projects!

Flags
------

- ``--view`` : To get your current mlf-core configuration.

  The explicit value of your Github personal access token will not be printed. You will only be informed about whether it is set or not.

On Github personal access tokens
------------------------------------

mlf-core's Github support requires access to your Github repositories to create repositories, add issues labels and set branch protection rules.
Github manages these access rights through Personal Access Tokens (PAT).
If you are using mlf-core's Github support for the first time ``mlf-core config pat`` will be run and you will be prompted for your Github PAT.
Please refer to the `official documentation <https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line>`_ on how to create one.
mlf-core only requires ``repo`` access, so you only need to tick this box. This ensures that your PAT would not even allow for the deletion of repositories.
mlf-core then encrypts the Personal Access Token, adds the encrypted token to the ``mlf_core_conf.cfg`` file and saves the key locally in a hidden place.
This is safer than Github's official way, which recommends the usage of environment variables or Github Credentials, which both save the token in plaintext.
It is still strongly advised to secure your personal computer and not allow any foe to get access.

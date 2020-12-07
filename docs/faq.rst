.. _general_faq:

=====
FAQ
=====

mlf-core is compound software and due to its complex nature many questions may arise.
This section serves as a collection of frequently asked questions.
If you do not find your answer here you may always `join our Discord channel <https://discord.gg/Mv8sAcq>`_ and ask for help.
We are happy to include your question here afterwards.


.. _mlf_core_faq:

I need help with mlf-core. How can I get in contact with the developers?
------------------------------------------------------------------------------------------

You can `open an issue <https://github.com/mlf-core/mlf-core/issues>`_ or `join our Discord channel <https://discord.gg/Mv8sAcq>`_.

I am looking for a template for domain x and language/framework y, but it does not exist yet!
--------------------------------------------------------------------------------------------------

We are always looking to add new templates to mlf-core. Please `open an issue <https://github.com/mlf-core/mlf-core/issues>`_ or `join our Discord channel <https://discord.gg/Mv8sAcq>`_.
Even better if you already have a draft for the template and/or could add it yourself!

How can you claim that your templates are GPU deterministic?
--------------------------------------------------------------------------------------------------

We performed extensive tests on various GPU architectures and can confidently say that given our settings GPU deterministic results can be expected on the same GPU architecture.
Hence, all mlf-core templates feature `system-intelligence <https://github.com/mlf-core/system-intelligence>`_, which queries your system for the used GPUs and their architecture.

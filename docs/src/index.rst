.. No Errors Test Project documentation master file, created by
   sphinx-quickstart on Sun Aug 09 17:07:56 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to OS Migrate's documentation!
======================================

OS Migrate is an open source toolbox for parallel cloud migration
between OpenStack clouds. Parallel cloud migration is a way to
modernize an OpenStack deployment. Instead of upgrading an OpenStack
cluster in place, a second OpenStack cluster is deployed alongside,
and tenant content is migrated from the original cluster to the new
one. As hardware resources free up in the original cluster, they can
be gradually added to the new cluster.

OS Migrate provides a framework for exporting and importing resources
between two clouds. It's a collection of Ansible playbooks that
provide the basic functionality, but may not fit each use case out of
the box. You can craft custom playbooks using the OS Migrate
collection pieces (roles and modules) as building blocks.

OS Migrate strictly uses the official OpenStack API and does not
utilize direct database access or other methods to export or import
data. The Ansible playbooks contained in OS Migrate are idempotent.
If a command fails, you can retry with the same command.

Community
~~~~~~~~~

The `source code of OS Migrate <https://github.com/os-migrate/os-migrate>`_
is hosted on GitHub.

For issue reports please use the GitHub
`OS Migrate issue tracker <https://github.com/os-migrate/os-migrate/issues>`_.

To get help, feel free to also create an
`issue <https://github.com/os-migrate/os-migrate/issues>`_
on GitHub with your question.

For a more interactive chat, join the Matrix room
`#os-migrate:matrix.org <https://app.element.io/#/room/#os-migrate:matrix.org>`_.

If you want to contribute to the project (code, docs, ...), please
refer to the `developer docs <devel/README.html>`_.

Contents
========

.. toctree::
   :maxdepth: 2

   user/README.rst
   roles
   modules
   changelog
   devel/README.rst

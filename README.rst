Food Reference Listing
======================

Reference Listing of Accepted Construction Materials, Packaging Materials and Non-Food Chemical Products Database

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
     :target: https://github.com/ambv/black
     :alt: Black code style


:License: MIT

Notes
-----

Implemented with GCWeb 6.0: https://wet-boew.github.io/wet-boew/docs/versions/dwnld-en.html



Settings
--------

Moved to settings_.

.. _settings: http://cookiecutter-django.readthedocs.io/en/latest/settings.html


Deployment
----------

Deploying this application on a new server should be fairly simple thanks to Docker.

1. First, here's how you would go about installing and configuring Docker (assuming Ubuntu 18.04)

.. code-block::

    $ # Docker (https://docs.docker.com/install/linux/docker-ce/ubuntu/)
    $ sudo apt-get remove docker docker-engine docker.io containerd runc
    $ sudo apt-get update
    $ sudo apt-get install apt-transport-https ca-certificates curl gnupg-agent software-properties-common
    $ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    $ sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
    $ sudo apt-get update
    $ sudo apt-get install docker-ce docker-ce-cli containerd.io

    $ # docker-machine
    $ base=https://github.com/docker/machine/releases/download/v0.16.0 &&
    $   curl -L $base/docker-machine-$(uname -s)-$(uname -m) >/tmp/docker-machine &&
    $   sudo mv /tmp/docker-machine /usr/local/bin/docker-machine &&
    $   chmod +x /usr/local/bin/docker-machine

    $ # docker-compose
    $ sudo curl -L "https://github.com/docker/compose/releases/download/1.25.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    $ sudo chmod +x /usr/local/bin/docker-compose

    $ # Add user to docker usergroup
    $ sudo usermod -aG docker $USER

    $ # Restart service
    $ sudo systemctl restart docker

2. Then, build the image with this command

.. code-block::

    $ docker-compose -f local.yml build

3. Make sure the database has been created

.. code-block::

    $ createdb food_reference_listing_db

4. Make database migrations then add superuser to Django app

.. code-block::

    $ docker-compose -f local.yml run --rm django python manage.py makemigrations
    $ docker-compose -f local.yml run --rm django python manage.py migrate
    $ docker-compose -f local.yml run --rm django python manage.py createsuperuser

5. Test to see if the server works. You should be able to log in with the superuser account you just made.

.. code-block::

    $ # Go to the IP address available here
    $ docker-compose -f local.yml up

6. Populate the databasew with the helper script.
    TODO


Docker
^^^^^^

See detailed `cookiecutter-django Docker documentation`_.

.. _`cookiecutter-django Docker documentation`: http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html



Type checks
^^^^^^^^^^^

Running type checks with mypy:

::

  $ mypy food_reference_listing

Test coverage
^^^^^^^^^^^^^

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

Running tests with py.test
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  $ pytest

Live reloading and Sass CSS compilation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Moved to `Live reloading and SASS compilation`_.

.. _`Live reloading and SASS compilation`: http://cookiecutter-django.readthedocs.io/en/latest/live-reloading-and-sass-compilation.html


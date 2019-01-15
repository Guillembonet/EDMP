*******
EDMP
*******

How to run
=======================================
To be able to have two nodes in the same computer you should run run_market.py with 3 arguments which have to be different for each node.

For example:

./run_market.py 8081 /home/bunetz/.Tribler /home/bunetz/.Tribler/ec_multichain.pem
./run_market.py 8082 /home/bunetz/.Tribler2 /home/bunetz/.Tribler2/ec_multichain2.pem

Now we can use call the api (with these calls https://tribler.readthedocs.io/en/devel/restapi/market.html) deployed in http://localhost:<port>


**We make use of submodules, so remember using the --recursive argument when cloning this repo.**

Setting up your development environment
=======================================

We support development on Linux, macOS and Windows. We have written documentation that guides you through installing the required packages when setting up a Tribler development environment. See `our Linux development guide <http://tribler.readthedocs.io/en/devel/development/development_on_linux.html>`_ for the guide on setting up a development environment on Linux distributions. See `our Windows development guide <http://tribler.readthedocs.io/en/devel/development/development_on_windows.html>`_ for setting everything up on Windows. See `our OS X development guide <http://tribler.readthedocs.io/en/devel/development/development_on_osx.html>`_ for the guide to setup the development environment on macOS.

Running EDMP from the repository
===================================

First clone the repository:

.. code-block:: none

    git clone --recursive git@github.com:Tribler/tribler.git

or, if you haven't added your ssh key to your github account:

.. code-block:: none

    git clone --recursive https://github.com/Tribler/tribler.git

Second, install the `dependencies <doc/development/development_on_linux.rst>`_.

Done!
Now you can run tribler by executing the ``tribler.sh`` script on the root of the repository:

.. code-block:: none

    ./tribler.sh
    
On Windows, you can use the following command to run Tribler:

.. code-block:: none

    python run_tribler.py

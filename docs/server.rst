The trackserver
===============

The trackserver command is used to start the trackserver ZeroRPC interface.
The trackserver can be launched with it's default configuration, which
uses the console and progress trackers, by launching the trackserver without
specifying any config file. I.e.::

    $ trackserver

Usually, however, you'll want to launch the trackserver with a custom
configuration file that specifies the track services that you would like to
use::

    $ trackserver --config config.yaml

The config file should be in YAML format. The following example config file
tells the trackserver to use the :ref:`console`, :ref:`progress`,
:ref:`tensorboard`, and :ref:`sqlite` trackers. Here the :ref:`sqlite` tracker
is configured to use a database name of ``db.sqlite``.

.. code-block :: yaml

    trackers:
    - type: progress
    - type: console
    - type: tensorboard

    - type: sqlite
      config:
      database: db.sqlite

More information on how to configure the trackers can be found in the
:ref:`trackers` documentation.

Usage
-----

The full usage information for the trackserver is shown below::

    Usage: trackserver [OPTIONS]

    Experiment tracking ZeroRPC server.

    Options:
    --config TEXT         YAML configuration file
    --port TEXT           TCP port number
    --host TEXT           Hostname to run on
    --debug / --no-debug  Only use the debug tracker
    --help                Show this message and exit.


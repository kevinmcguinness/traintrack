Tracker services
================


The following trackers come built-in.

console
-------

Print metrics to the console at the end of each epoch.

.. code-block:: yaml

    trackers:
    - type: console


progress
--------

Show a console based progress bar that can be use to track, for example, how
many batches have been processed in this epoch.

.. code-block:: yaml

    trackers:
    - type: progress


tensorboard
-----------

Monitor experiment progress, metrics, images, etc., using tensorboard
(uses `pytorch.utils.tensorboard`).


.. code-block:: yaml

    trackers:
    - type: tensorboard
        config:
        log_dir: ''  # if unspecified, defaults to runs
        comment: ''
        max_queue: 10
        flush_secs: 120
        filename_suffix: ''


logfile
-------

Write messages and metrics to a plain text log file.

.. code-block:: yaml

    trackers:
    - type: logfile
        config:
        logdir: logs
        suffix: .log  # filename suffix


slack
-----

Send log messages and metrics to a slack channel.

.. code-block:: yaml

    trackers:
    - type: slack
        config:
        token: YOUR-SLACK-API-TOKEN-HERE
        channel: '#your-channel-here'
        progressbar: false  # enable or disable a task progress bar
        loglevel: 'INFO'  # logging level of messages to send to slack


You can alternatively leave the token unspecified in the config file and set
the `SLACK_API_TOKEN` environmental variable to your slack API token.

sqlite
------

Save metrics and hyperparameters to a sqlite database.

.. code-block:: yaml

    trackers:
    - type: sqlite
        config:
        database: db.sqlite  # database file name


pandas
------

Collect metrics in a pandas dataframe and save the results to the disk after
each epoch.


.. code-block:: yaml

    trackers:
    - type: pandas
        config:
        path: logs  # where to save the dataframe
        format: excel  # format, one of: excel|csv|pickle|strata|hdf|json


custom
------

A custom user defined tracker available somewhere on the Python package/module
search path.

.. code-block:: yaml

    trackers:
    - type: custom
        config:
        classname: CustomClassName  # class name of the custom tracker
        modulename: your.package  # module name containing the above class


Any additional config key-value pairs will be passed as `kwargs` to the custom
tracker's constructor.

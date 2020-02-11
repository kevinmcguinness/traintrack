# TrainTrack

Monitor and track metrics and progress when training deep learning models.

## Installation

```bash
$ pip install git+https://github.com/kevinmcguinness/traintrack
```

This will install the `traintrack` package and the `trackserver` command line tool.

## Usage

Start the experiment tracker service:

```bash
$ trackserver --config <config.yaml>
```

You can configure the tracker service using the `config.yaml` file. See the `config.yaml` in the repository for an example of how this file should look. If you start the experiment tracker without specifying a config file, by default it will add the *console* and *progress* trackers.

Communicate with the tracker from your training code using something similar to the following::

```python
from traintrack.client import ExperimentTracker

tracker = ExperimentTracker()

for epoch in range(1, 11):
    tracker.begin_epoch(epoch)

    for i, batch in enumerate(batches):

        # train on a batch
        # ...

        tracker.progress(i+1, n_batches)

    # report metrics for the epoch
    tracker.metric('loss/train', loss_train)
    tracker.metric('loss/valid', loss_valid)
    tracker.metric('acc/valid', acc_valid)

    tracker.end_epoch()
```

## Available trackers

The following trackers come build in.

### console

Print metrics to the console at the end of each epoch.

```yaml
trackers:
  - type: console
```

### progress

Show a console based progress bar that can be use to track, for example, how many batches have been processed in this epoch.

```yaml
trackers:
  - type: progress
```

### tensorboard

Monitor experiment progress, metrics, images, etc., using tensorboard (uses `pytorch.utils.tensorboard`).


```yaml
trackers:
  - type: tensorboard
    config:
      log_dir: ''  # if unspecified, defaults to runs
      comment: ''
      max_queue: 10
      flush_secs: 120
      filename_suffix: ''
```

### logfile

Write messages and metrics to a plain text log file.

```yaml
trackers:
  - type: logfile
    config:
      logdir: logs
      suffix: .log  # filename suffix
```

### slack

Send log messages and metrics to a slack channel.

```yaml
trackers:
  - type: slack
    config:
      token: YOUR-SLACK-API-TOKEN-HERE
      channel: '#your-channel-here'
      progressbar: false  # enable or disable a task progress bar
      loglevel: 'INFO'  # logging level of messages to send to slack
```

You can alternatively leave the token unspecified in the config file and set the `SLACK_API_TOKEN` environmental variable to your slack API token.

### sqlite

Save metrics and hyperparameters to a sqlite database.

```yaml
trackers:
  - type: sqlite
    config:
      database: db.sqlite  # database file name
```

### pandas

Collect metrics in a pandas dataframe and save the results to the disk after
each epoch.


```yaml
trackers:
  - type: pandas
    config:
      path: logs  # where to save the dataframe
      format: excel  # format, one of: excel|csv|pickle|strata|hdf|json
```

### custom

A custom user defined tracker available somewhere on the Python package/module search path.

```yaml
trackers:
  - type: custom
    config:
      classname: CustomClassName  # class name of the custom tracker
      modulename: your.package  # module name containing the above class
```

Any additional config key-value pairs will be passed as `kwargs` to the custom tracker's constructor.

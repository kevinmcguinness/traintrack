# TrainTrack

Monitor and track metrics and progress when training deep learning models.

## Usage

Start the experiment tracker service:

```bash
$ python experiment_tracker.py --config <config.yaml>
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


### console

Print metrics to the console at the end of each epoch.

### progress

Show a console based progress bar that can be use to track, for example, how many batches have been processed in this epoch.

### tensorboard

Monitor experiment progress, metrics, images, etc., using tensorboard (uses `pytorch.utils.tensorboard`).

### logfile

Write messages and metrics to a plain text log file.

### slack

Send log messages and metrics to a slack channel.

### sqlite

Save metrics and hyperparameters to a sqlite database.


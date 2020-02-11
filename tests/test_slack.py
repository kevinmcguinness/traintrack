import os

from warnings import warn
from traintrack.services.slack import SlackTracker


def test_slack_tracker():

    if 'SLACK_API_TOKEN' not in os.environ:
        warn('SLACK_API_TOKEN environment variable not set, skipping test')
        return

    tracker = SlackTracker(channel='#nn_training',
                           progressbar=False,
                           loglevel='INFO')
    experiment = tracker.experiment('test_slack_tracker')
    experiment.log('INFO', 'info visible')
    experiment.log('DEBUG', 'debug invisible')
    epoch = experiment.epoch(0)
    epoch.begin()
    epoch.progress(50, 50, '')
    epoch.end()

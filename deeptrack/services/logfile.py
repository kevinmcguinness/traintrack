# -*- coding: utf-8 -*-
# (c) Copyright 2020 Kevin McGuinness. All Rights Reserved
from . import api
from ..util import timestamp
from pathlib import Path


class Epoch(api.Epoch):
    def __init__(self, experiment, epoch):
        super().__init__(experiment, epoch)

    @property
    def log(self):
        return self.experiment.log

    def begin(self):
        self.log('INFO', f'starting epoch [{self.epoch}]')  # pylint: disable=not-callable

    def metric(self, name, value):
        self.log('INFO', f'[{self.epoch}] metric {name}: {value}')  # pylint: disable=not-callable

    def end(self):
        self.log('INFO', f'ending epoch [{self.epoch}]')  # pylint: disable=not-callable


class Experiment(api.Experiment):
    epoch_type = Epoch

    def __init__(self, tracker, name):
        super().__init__(tracker, name)
        self.filename = tracker.logdir / (name + tracker.suffix)
        self.file = open(self.filename, 'w')

    def description(self, text):
        self.log('INFO', f'description: {text}')

    def parameter(self, name, value):
        self.log('INFO', f'param {name}: {value}')

    def log(self, level, text):
        ts = timestamp()
        print(f'[{ts}] {level} - {text}', file=self.file, flush=True)


class LogfileTracker(api.ExperimentTracker):
    experiment_type = Experiment

    def __init__(self, logdir=None, suffix='.log'):
        super().__init__()
        if logdir is not None:
            self.logdir = Path(logdir)
        else:
            self.logdir = Path()
        self.suffix = suffix


ExperimentTracker = LogfileTracker

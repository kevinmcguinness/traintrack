# -*- coding: utf-8 -*-
# (c) Copyright 2020 Kevin McGuinness. All Rights Reserved
from . import api
from ..util import timestamp, style_level
from ..util import make_epoch_summary

from click import echo


class Epoch(api.Epoch):
    def __init__(self, experiment, epoch):
        super().__init__(experiment, epoch)
        self.metrics = {}

    def metric(self, name, value):
        self.metrics[name] = value

    def end(self):
        print(make_epoch_summary(self.epoch, self.metrics))


class Experiment(api.Experiment):
    epoch_type = Epoch

    def __init__(self, tracker, name):
        super().__init__(tracker, name)
        self.log('INFO', f'Starting experiment {name}')

    def log(self, level, text):
        styled_level = style_level(level)
        echo(f'[{timestamp()}] {styled_level}: {text}')


class ConsoleTracker(api.ExperimentTracker):
    experiment_type = Experiment


ExperimentTracker = ConsoleTracker

# -*- coding: utf-8 -*-
# (c) Copyright 2020 Kevin McGuinness. All Rights Reserved
from . import api


class Epoch(api.Epoch):
    def __init__(self, experiment, epoch):
        super().__init__(experiment, epoch)

    def begin(self):
        print(f'[{self.experiment.name}] [{self.epoch}] started')

    def metric(self, name, value):
        print(f'[{self.experiment.name}] [{self.epoch}] '
              f'metric {name}: {value}')

    def begin_task(self, name):
        print(f'[{self.experiment.name}] begin task: {name}')

    def progress(self, completed, total, info):
        info = info or ''
        print(f'[{self.experiment.name}] progress {completed}/{total}  {info}')

    def end_task(self):
        print(f'[{self.experiment.name}] end task')

    def image(self, name, image):
        print(f'[{self.experiment.name}] [{self.epoch}] image {name}')

    def end(self):
        print(f'[{self.experiment.name}] [{self.epoch}] ended')


class Experiment(api.Experiment):
    epoch_type = Epoch

    def __init__(self, tracker, name):
        super().__init__(tracker, name)

    def description(self, text):
        print(f'[{self.name}] description: {text}')

    def parameter(self, name, value):
        print(f'[{self.name}] parameter {name} {value}')

    def log(self, level, text):
        print(f'[{self.name}] {level}: {text}')


class DebugTracker(api.ExperimentTracker):
    experiment_type = Experiment


ExperimentTracker = DebugTracker

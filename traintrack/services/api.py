# -*- coding: utf-8 -*-
# (c) Copyright 2020 Kevin McGuinness. All Rights Reserved
from collections import defaultdict


class Epoch(object):
    def __init__(self, experiment, epoch):
        self.experiment = experiment
        self.epoch = epoch

    def begin(self):
        pass

    def progress(self, completed, total, info):
        pass

    def metric(self, name, value):
        pass

    def image(self, name, image):
        pass

    def end(self):
        pass


class Experiment(object):
    epoch_type = Epoch

    def __init__(self, tracker, name):
        self.tracker = tracker
        self.name = name
        self._epochs = {}

    def description(self, text):
        pass

    def parameter(self, name, value):
        pass

    def log(self, level, text):
        pass

    def epoch(self, epoch):
        if epoch not in self._epochs:
            self._epochs[epoch] = self.epoch_type(self, epoch)
        return self._epochs[epoch]


class ExperimentTracker(object):
    experiment_type = Experiment

    def __init__(self):
        self._experiments = {}

    def experiment(self, id):
        if id not in self._experiments:
            self._experiments[id] = self.experiment_type(self, id)
        return self._experiments[id]

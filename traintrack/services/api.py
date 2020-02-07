# -*- coding: utf-8 -*-
# (c) Copyright 2020 Kevin McGuinness. All Rights Reserved
from collections import defaultdict


class Task(object):
    def __init__(self, epoch, name=None):
        self.epoch = epoch
        self.name = name

    def begin(self):
        pass

    def progress(self, completed, total, info):
        pass

    def end(self):
        pass


class Epoch(object):
    task_type = Task

    def __init__(self, experiment, epoch):
        self.experiment = experiment
        self.epoch = epoch
        self.task = None

    def begin(self):
        pass

    def begin_task(self, name=None):
        self.task = self.task_type(self, name)
        self.task.begin()
        return self.task

    def progress(self, completed, total, info):
        if self.task is None:
            self.begin_task()
        self.task.progress(completed, total, info)

    def end_task(self):
        self.task.end()
        self.task = None

    def metric(self, name, value):
        pass

    def image(self, name, image):
        pass

    def end(self):
        if self.task is not None:
            self.task.end()
            self.task = None


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

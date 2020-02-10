# -*- coding: utf-8 -*-
# (c) Copyright 2020 Kevin McGuinness. All Rights Reserved
from . import api
from ..util import timestamp
from pathlib import Path

import pandas as pd


available_formats = {
    'csv': ('.csv', pd.DataFrame.to_csv),
    'excel': ('.xls', pd.DataFrame.to_excel),
    'hdf': ('.h5', pd.DataFrame.to_hdf),
    'json': ('.json', pd.DataFrame.to_json),
    'pickle': ('.pkl', pd.DataFrame.to_pickle),
    'stata': ('.dta', pd.DataFrame.to_stata),
}


class Epoch(api.Epoch):
    def __init__(self, experiment, epoch):
        super().__init__(experiment, epoch)
        self.metrics = {}
        self.filename = experiment.filename

    def metric(self, name, value):
        self.metrics[name] = value

    def end(self):
        for k, v in self.metrics.items():
            self.experiment.metrics.setdefault(k, []).append(v)
        self.experiment.epochs.append(self.epoch)
        dataframe = pd.DataFrame(
            data=self.experiment.metrics,
            index=self.experiment.epochs)
        self.experiment.tracker.save_dataframe(
            dataframe, self.filename)


class Experiment(api.Experiment):
    epoch_type = Epoch

    def __init__(self, tracker, name):
        super().__init__(tracker, name)
        self.filename = tracker.path / (name + tracker.suffix)
        self.metrics = {}
        self.epochs = []


class DataFrameTracker(api.ExperimentTracker):
    experiment_type = Experiment

    def __init__(self, path=None, format='csv'):
        super().__init__()
        if path is not None:
            self.path = Path(path)
        else:
            self.path = Path()
        self.format = format
        self.suffix = available_formats[format][0]
        self.save_dataframe = available_formats[format][1]


ExperimentTracker = DataFrameTracker

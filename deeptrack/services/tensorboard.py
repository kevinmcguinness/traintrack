# -*- coding: utf-8 -*-
# (c) Copyright 2020 Kevin McGuinness. All Rights Reserved
import numpy as np

from . import api

from torch.utils.tensorboard import SummaryWriter


class Epoch(api.Epoch):
    def __init__(self, experiment, epoch):
        super().__init__(experiment, epoch)
        self.writer = experiment.writer

    def metric(self, name, value):
        self.writer.add_scalar(name, value, self.epoch)

    def image(self, name, image):
        image = np.array(image)
        self.writer.add_image(name, image, self.epoch, dataformats='HWC')


class Experiment(api.Experiment):
    epoch_type = Epoch

    def __init__(self, tracker, name):
        super().__init__(tracker, name)

        log_dir = tracker.log_dir
        if log_dir is None:
            log_dir = f'runs/{name}'

        self.writer = SummaryWriter(
            log_dir=tracker.log_dir,
            comment=tracker.comment,
            max_queue=tracker.max_queue,
            flush_secs=tracker.flush_secs,
            filename_suffix=tracker.filename_suffix)


class TensorboardTracker(api.ExperimentTracker):
    experiment_type = Experiment

    def __init__(self, log_dir=None, comment='', max_queue=10,
                 flush_secs=120, filename_suffix=''):
        super().__init__()
        self.log_dir = log_dir
        self.comment = comment
        self.max_queue = max_queue
        self.flush_secs = flush_secs
        self.filename_suffix = filename_suffix


ExperimentTracker = TensorboardTracker

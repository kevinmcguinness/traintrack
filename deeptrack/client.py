# -*- coding: utf-8 -*-
# (c) Copyright 2020 Kevin McGuinness. All Rights Reserved

import zerorpc
import time
import base64

from .util import make_experiment_id
from .util import encode_image


class ExperimentTracker(object):
    def __init__(self, experiment_id=None, host='0.0.0.0', port=4242,
                 first_epoch=1, default_log_level='INFO', async_=False):
        self.client = zerorpc.Client(f'tcp://{host}:{port}')
        self.experiment_id = experiment_id or make_experiment_id()
        self.epoch = first_epoch - 1
        self.default_log_level = default_log_level

        # need to work around the fact that async is a keyword in Python 3.7
        self.rpc_kwargs = {'async': async_}

    def begin_epoch(self, epoch=None):
        if epoch is not None:
            self.epoch = epoch
        else:
            self.epoch += 1
        self.client.begin_epoch(
            self.experiment_id, self.epoch, **self.rpc_kwargs)
        return self

    def end_epoch(self):
        self.client.end_epoch(
            self.experiment_id, self.epoch, **self.rpc_kwargs)
        return self

    def log(self, text, level=None):
        if level is None:
            level = self.default_log_level
        self.client.log(
            self.experiment_id, level, text, **self.rpc_kwargs)
        return self

    def debug(self, text):
        return self.log(text, level='DEBUG')

    def info(self, text):
        return self.log(text, level='INFO')

    def warn(self, text):
        return self.log(text, level='WARNING')

    def error(self, text):
        return self.log(text, level='ERROR')

    def critical(self, text):
        return self.log(text, level='CRITICAL')

    def parameter(self, name, value):
        self.client.parameter(
            self.experiment_id, name, value, **self.rpc_kwargs)
        return self

    def description(self, text):
        self.client.description(
            self.experiment_id, text, **self.rpc_kwargs)
        return self

    def metric(self, name, value):
        self.client.metric(
            self.experiment_id, self.epoch, name, value, **self.rpc_kwargs)
        return self

    def image(self, name, image, pixel_order=None):
        image = encode_image(image, pixel_order)
        self.client.image(
            self.experiment_id, self.epoch, name, image, **self.rpc_kwargs)
        return self

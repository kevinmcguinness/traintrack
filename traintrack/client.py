# -*- coding: utf-8 -*-
# (c) Copyright 2020 Kevin McGuinness. All Rights Reserved

import zerorpc
import time
import base64

from .util import make_experiment_id
from .util import encode_image


class ExperimentTracker(object):
    r"""
    Experiment tracker client.

    The experiment tracker client is used to communicate with a trackserver
    over ZeroRPC to report experiment configuration, metrics, and progress.
    The server then sends this information to configured backend services.

    Args:
        experiment_id (str, optional): identifier for the current experiment
            that will be tracked. This is used by the server to uniquely
            identify the experiment and often backend services to write to
            log files and databases, etc. If unspecified, it will be generated
            based on the current date and time.
        host (str, optional): the host name the server is running on. Default:
            ``'0.0.0.0'``
        port (int, optioal): TCP port number that the server is running on.
            Default: ``4242``
        first_epoch (int, optional): the number of the epoch that will be
            sent to the server when ``begin_epoch`` is first called. Useful
            for resuming stopped experiments. Default: ``1``
        default_log_level (str, optional): default logging level when none is
            specified in calls to ``log``. Default: ``'INFO'``
        async\_ (bool, optional): whether to send messages to the server
            asynchronously. If enabled, method calls will return immediately
            without waiting on a response from the server. This can be enabled
            if you are worried about communication with the server slowing down
            your experiments. Default: ``False``

    """

    def __init__(self, experiment_id=None, host='0.0.0.0', port=4242,
                 first_epoch=1, default_log_level='INFO', async_=False):
        self.client = zerorpc.Client(f'tcp://{host}:{port}')
        self.experiment_id = experiment_id or make_experiment_id()
        self.epoch = first_epoch - 1
        self.default_log_level = default_log_level

        # need to work around the fact that async is a keyword in Python 3.7
        self.rpc_kwargs = {'async': async_}

    def begin_epoch(self, epoch=None):
        """
        Start a new training epoch

        Args:
            epoch (int, optional): if specified the given epoch will be sent to
                the server. Otherwise the last epoch will be incremented and
                sent to the server.
        """
        if epoch is not None:
            self.epoch = epoch
        else:
            self.epoch += 1
        self.client.begin_epoch(
            self.experiment_id, self.epoch, **self.rpc_kwargs)
        return self

    def end_epoch(self):
        """
        End the current epoch.
        """
        self.client.end_epoch(
            self.experiment_id, self.epoch, **self.rpc_kwargs)
        return self

    def progress(self, completed, total, info=None):
        """
        Report progress on the current epoch.

        Args:
            completed (int): number of items (e.g. batches) completed.

            total (int): number of items (e.g. batches) in total.

            info (str, optional): extra information to be shown.
        """
        self.client.progress(
            self.experiment_id, self.epoch, completed, total, info,
            **self.rpc_kwargs)
        return self

    def log(self, text, level=None):
        """
        Send a logging message to the server.

        Args:
            test (str): the text to log.

            level (str, optional): the log level. If unspecified, defaults to
                ``self.default_log_level``.
        """
        if level is None:
            level = self.default_log_level
        self.client.log(
            self.experiment_id, level, text, **self.rpc_kwargs)
        return self

    def debug(self, text):
        """
        Convenience method to send a logging message with DEBUG log level
        to the server.

        Args:
            test (str): the text to log.
        """
        return self.log(text, level='DEBUG')

    def info(self, text):
        """
        Convenience method to send a logging message with INFO log level
        to the server.

        Args:
            test (str): the text to log.
        """
        return self.log(text, level='INFO')

    def warn(self, text):
        """
        Convenience method to send a logging message with WARNING log level
        to the server.

        Args:
            test (str): the text to log.
        """
        return self.log(text, level='WARNING')

    def error(self, text):
        """
        Convenience method to send a logging message with ERROR log level
        to the server.

        Args:
            test (str): the text to log.
        """
        return self.log(text, level='ERROR')

    def critical(self, text):
        """
        Convenience method to send a logging message with CRITICAL log level
        to the server.

        Args:
            test (str): the text to log.
        """
        return self.log(text, level='CRITICAL')

    def parameter(self, name, value):
        """
        Report an experiment parameter or hyperparameter (e.g. learning rate).

        Args:
            name (str): name of the parameter (e.g. ``'lr'``).

            value: value of the parameter being used in the experiment.
        """
        self.client.parameter(
            self.experiment_id, name, value, **self.rpc_kwargs)
        return self

    def description(self, text):
        """
        Report an description of the current experiment.
        """
        self.client.description(
            self.experiment_id, text, **self.rpc_kwargs)
        return self

    def metric(self, name, value):
        """
        Report a (scalar) metric like training loss or validation accuracy. The
        metric will automatically be associated with the current training
        epoch.

        Args:
            name (str): name of the metric (e.g. ``'loss/train'``).

            value (float): the value of the metric
        """
        self.client.metric(
            self.experiment_id, self.epoch, name, value, **self.rpc_kwargs)
        return self

    def image(self, name, image, pixel_order=None):
        """
        Report an image (e.g. a set of filters learned our outputs of a
        segmentation algorithm, etc.). The image will automatically be
        associated with the current training epoch.

        Args:
            name (str): name of the image (e.g. ``'filters'``).

            image (np.ndarray or PIL.Image): the image to report.

            pixel_order (str, optional): the order of the pixels in
                the ``ndarray``. Can be ``'CHW'`` for channels, height,
                width, or ``'HHC'`` for height, width, channels. By default,
                the image encoding algorithm will attempt to guess based on the
                dimensions of the ``ndarray``.
        """
        image = encode_image(image, pixel_order)
        self.client.image(
            self.experiment_id, self.epoch, name, image, **self.rpc_kwargs)
        return self

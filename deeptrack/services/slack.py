# -*- coding: utf-8 -*-
# (c) Copyright 2020 Kevin McGuinness. All Rights Reserved
from . import api
from ..util import encode_pil_image
from ..util import make_epoch_summary
from collections import defaultdict

import slack
import os
import io


class Epoch(api.Epoch):
    def __init__(self, experiment, epoch):
        super().__init__(experiment, epoch)
        self.metrics = {}
        self.tracker = experiment.tracker

    def begin(self):
        pass
        # self.tracker.post(f'Epoch {self.epoch} started')

    def metric(self, name, value):
        self.metrics[name] = value

    def end(self):
        self.tracker.post(make_epoch_summary(self.epoch, self.metrics))

    def image(self, name, image):
        buffer = encode_pil_image(image)
        fileobj = io.BytesIO(buffer)
        self.tracker.upload(
            title=name,
            file=fileobj,
            filename=f'{name}.jpg',
            filetype='jpg')


class Experiment(api.Experiment):
    epoch_type = Epoch

    def __init__(self, tracker, name):
        super().__init__(tracker, name)
        self.tracker.post(f'starting experiment "{name}"')

    def description(self, text):
        self.tracker.post(f'description: {text}')

    def parameter(self, name, value):
        self.tracker.post(f'parameter {name} {value}')

    def log(self, level, text):
        emoji = log_level_emojis[level]
        self.tracker.post(f'{emoji} {text}')


log_level_emojis = defaultdict(lambda: ':white_circle:', {
    'CRITICAL': ':radioactive_sign:',
    'ERROR': ':red_circle:',
    'WARNING': ':warning:',
    'INFO': ':information_source:',
    'DEBUG': ':white_circle:'
})


class SlackTracker(api.ExperimentTracker):
    experiment_type = Experiment

    def __init__(self, token=None, channel=None):
        super().__init__()
        token = os.environ['SLACK_API_TOKEN']
        if token is None:
            raise OSError('Set SLACK_API_TOKEN environment variable')
        self.client = slack.WebClient(token=token)
        self.channel = channel

    def post(self, text):
        self.client.chat_postMessage(
            channel=self.channel, text=text)

    def upload(self, file=None, content=None, **kwargs):
        self.client.files_upload(
            channels=self.channel,
            file=file,
            content=content,
            **kwargs)


ExperimentTracker = SlackTracker

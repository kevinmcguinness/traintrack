# -*- coding: utf-8 -*-
# (c) Copyright 2020 Kevin McGuinness. All Rights Reserved
from . import api
from ..util import encode_pil_image
from ..util import make_epoch_summary
from collections import defaultdict

import slack
import os
import io


class SlackProgressBar(object):
    def __init__(self, name, client, channel, width=10):
        self.name = name
        self.client = client
        self.channel = channel
        self.channel_id = None
        self.msg_ts = None
        self.width = width
        self.fill_block = chr(11035)
        self.empty_block = chr(11036)

    def update(self, completed, total, info):
        if completed > total:
            completed = total
        proportion = completed / total
        percent = proportion * 100
        n = round(proportion * self.width)
        bar = self.fill_block * n + self.empty_block * (self.width - n)
        status = f'{self.name}\n{bar} {percent:.0f}%'
        if info:
            status = status + '\n{info}'
        if self.msg_ts is not None:
            self.client.chat_update(
                channel=self.channel_id,
                ts=self.msg_ts,
                text=status)
        else:
            res = self.client.chat_postMessage(
                channel=self.channel,
                text=status)
            self.msg_ts = res['ts']
            self.channel_id = res['channel']


class Task(api.Task):

    def __init__(self, epoch, name):
        super().__init__(epoch, name)

    def begin(self):
        self.progress_bar = SlackProgressBar(
            self.name,
            self.epoch.tracker.client,
            self.epoch.tracker.channel)

    def progress(self, completed, total, info):
        self.progress_bar.update(completed, total, info)

    def end(self):
        self.progress_bar = None


class Epoch(api.Epoch):
    task_type = Task

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
        if not token:
            # try get token from environment
            token = os.environ.get('SLACK_API_TOKEN', None)
            if token is None:
                raise OSError('Set SLACK_API_TOKEN environment variable')
        print(token)
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

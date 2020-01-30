# -*- coding: utf-8 -*-
# (c) Copyright 2020 Kevin McGuinness. All Rights Reserved
import click
import zerorpc
import time


from PIL import Image
from .util import decode_image

arg = click.argument
opt = click.option


class TrackerService(object):

    def __init__(self):
        self.trackers = []

    def log(self, id, level, text):
        for tracker in self.trackers:
            tracker.experiment(id).log(level, text)

    def parameter(self, id, name, value):
        for tracker in self.trackers:
            tracker.experiment(id).parameter(name, value)

    def description(self, id, text):
        for tracker in self.trackers:
            tracker.experiment(id).description(text)

    def metric(self, id, epoch, name, value):
        for tracker in self.trackers:
            tracker.experiment(id).epoch(epoch).metric(name, value)

    def image(self, id, epoch, name, image):
        image = decode_image(image)
        for tracker in self.trackers:
            tracker.experiment(id).epoch(epoch).image(name, image)

    def begin_epoch(self, id, epoch):
        for tracker in self.trackers:
            tracker.experiment(id).epoch(epoch).begin()

    def end_epoch(self, id, epoch):
        for tracker in self.trackers:
            tracker.experiment(id).epoch(epoch).end()


class TrackerServer(object):
    def __init__(self):
        self.service = TrackerService()

    def register_tracker(self, tracker):
        self.service.trackers.append(tracker)

    def run(self, host, port):
        s = zerorpc.Server(self.service)
        s.bind(f"tcp://{host}:{port}")
        s.run()

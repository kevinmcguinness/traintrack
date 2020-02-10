# -*- coding: utf-8 -*-
# (c) Copyright 2020 Kevin McGuinness. All Rights Reserved
from traintrack.server import TrackerServer
from traintrack.services.debug import DebugTracker
from traintrack.services.progress import ProgressTracker
from traintrack.client import ExperimentTracker

import time


class DirectClient(ExperimentTracker):

    def __init__(self, trackers, **kwargs):
        self.trackers = trackers
        super().__init__(**kwargs)
        self.rpc_kwargs = {}

    def create_server_interface(self, host, port):
        server = TrackerServer()
        for tracker in self.trackers:
            server.register_tracker(tracker)
        return server.service


def test_server2():
    service = DirectClient(
        trackers=[DebugTracker()],
        experiment_id='DebugExperiment')

    service.begin_epoch()

    # exercise logging
    service.log('log message', level='INFO')

    # exercise experiment metadata
    service.description('Test client')
    service.parameter('lr', 0.01)
    service.parameter('gg', 0)

    # exercise progress
    service.begin_epoch()
    service.begin_task('train')
    for i in range(5):
        service.progress(i+1, 5)
    service.end_task()

    # exercise metrics
    service.metric('a/b', 1.0)
    service.metric('c/d', -1.0)
    service.end_epoch()


def test_server():
    server = TrackerServer()
    server.register_tracker(DebugTracker())
    service = server.service

    id = 'DebugExperiment'
    epoch = 1

    # exercise logging
    service.log('id', 'INFO', 'log message')

    # exercise experiment metadata
    service.description(id, 'Test client')
    service.parameter(id, 'lr', 0.01)
    service.parameter(id, 'gg', 0)

    # exercise progress
    service.begin_epoch(id, epoch)
    service.begin_task(id, epoch, 'train')
    for i in range(5):
        service.progress(id, epoch, i+1, 5, None)
    service.end_task(id, epoch)

    # exercise metrics
    service.metric(id, epoch, 'a/b', 1.0)
    service.metric(id, epoch, 'c/d', -1.0)
    service.end_epoch(id, epoch)


def test_progress():
    server = TrackerServer()
    server.register_tracker(ProgressTracker())
    service = server.service

    id = 'ProgressTest'

    # exercise progress
    for epoch in range(3):
        service.begin_epoch(id, epoch)

        for task in ('train', 'validate'):
            service.begin_task(id, epoch, task)
            for i in range(5):
                service.progress(id, epoch, i+1, 5, None)
                time.sleep(0.1)
            service.end_task(id, epoch)

        service.end_epoch(id, epoch)

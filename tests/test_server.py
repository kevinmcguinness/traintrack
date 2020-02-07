# -*- coding: utf-8 -*-
# (c) Copyright 2020 Kevin McGuinness. All Rights Reserved
from traintrack.server import TrackerServer
from traintrack.services.debug import DebugTracker


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
    for i in range(5):
        service.progress(id, epoch, i+1, 5, None)

    # exercise metrics
    service.metric(id, epoch, 'a/b', 1.0)
    service.metric(id, epoch, 'c/d', -1.0)
    service.end_epoch(id, epoch)

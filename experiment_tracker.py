#!/usr/bin/env python
# -*- coding: utf-8 -*-
# (c) Copyright 2020 Kevin McGuinness. All Rights Reserved
from __future__ import print_function
from __future__ import division

import click
import zerorpc
import time

from PIL import Image

from deeptrack.server import TrackerServer
from deeptrack.services.debug import DebugTracker
from deeptrack.services.tensorboard import TensorboardTracker
from deeptrack.services.sqlite import SqliteTracker
from deeptrack.services.console import ConsoleTracker
from deeptrack.services.slack import SlackTracker
from deeptrack.services.logfile import LogfileTracker
from deeptrack.services.progress import ProgressTracker


arg = click.argument
opt = click.option


available_services = {
    'debug': DebugTracker,
    'tensorboard': TensorboardTracker,
    'sqlite': SqliteTracker,
    'console': ConsoleTracker,
    'slack': SlackTracker,
    'logfile': LogfileTracker
}


@click.command()
@opt('--port', default=4242)
@opt('--host', default='0.0.0.0')
def main(host, port):
    server = TrackerServer()
    server.register_tracker(ProgressTracker())
    server.register_tracker(ConsoleTracker())
    server.register_tracker(SlackTracker(channel='#nn_training'))
    # server.register_tracker(LogfileTracker('logs'))
    # server.register_tracker(TensorboardTracker())
    # server.register_tracker(SqliteTracker('tmp.sqlite'))

    server.run(host, port)


if __name__ == '__main__':
    main()

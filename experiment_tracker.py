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
from deeptrack.services import create_tracker, default_trackers


arg = click.argument
opt = click.option


@click.command()
@opt('--port', default=4242)
@opt('--host', default='0.0.0.0')
def main(host, port):
    server = TrackerServer()
    for tracker_name in default_trackers:
        tracker = create_tracker(tracker_name)
        print(tracker_name, tracker)
        server.register_tracker(tracker)
    server.run(host, port)


if __name__ == '__main__':
    main()  # pylint: disable=no-value-for-parameter

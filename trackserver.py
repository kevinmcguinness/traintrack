#!/usr/bin/env python
# -*- coding: utf-8 -*-
# (c) Copyright 2020 Kevin McGuinness. All Rights Reserved
from __future__ import print_function
from __future__ import division

import click
import zerorpc
import time
import yaml

from loguru import logger as log
from PIL import Image
from traintrack.server import TrackerServer
from traintrack.services import add_trackers_from_config
from traintrack.services.debug import DebugTracker


arg = click.argument
opt = click.option


default_config = {
    'host': '0.0.0.0',
    'port': 4242,
    'trackers': [
        {'type': 'progress'},
        {'type': 'console'}
    ]
}


@click.command()
@opt('--config', 'configfile', default=None, help='YAML configuration file')
@opt('--port', default=None, help='TCP port number')
@opt('--host', default=None, help='Hostname to run on')
@opt('--debug/--no-debug', default=False, help='Only use the debug tracker')
def main(host, port, configfile, debug):
    """
    Experiment tracking ZeroRPC server.
    """
    server = TrackerServer()

    config = default_config
    if configfile:
        with open(configfile, 'r') as f:
            config = yaml.safe_load(f)

    # allow override host
    if host:
        config['host'] = host

    # allow override port
    if port:
        config['port'] = port

    # add trackers
    if debug:
        server.register_tracker(DebugTracker())
    else:
        add_trackers_from_config(server, config, log)

    # run
    log.info(f'Starting RPC service on {config["host"]}:{config["port"]}')
    server.run(config['host'], config['port'])


if __name__ == '__main__':
    main()  # pylint: disable=no-value-for-parameter

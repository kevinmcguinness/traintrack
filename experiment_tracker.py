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
from deeptrack.server import TrackerServer
from deeptrack.services import create_tracker


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
@opt('--config', 'configfile', default=None)
@opt('--port', default=None)
@opt('--host', default=None)
def main(host, port, configfile):
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
    for tracker_cfg in config['trackers']:
        tracker_name = tracker_cfg['type']
        tracker_kwargs = tracker_cfg.get('config', {})
        log.info(f'Adding tracker: {tracker_name} {tracker_kwargs}')
        tracker = create_tracker(tracker_name, **tracker_kwargs)
        server.register_tracker(tracker)

    # run
    log.info(f'Starting RPC service on {config["host"]}:{config["port"]}')
    server.run(config['host'], config['port'])


if __name__ == '__main__':
    main()  # pylint: disable=no-value-for-parameter

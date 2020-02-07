# -*- coding: utf-8 -*-
# (c) Copyright 2020 Kevin McGuinness. All Rights Reserved
from traintrack.client import ExperimentTracker
from traintrack.server import TrackerServer

import sh
import time
import numpy as np
import pytest

from PIL import Image


def start_server(host='0.0.0.0', port=4242, config=None):
    p = sh.python('trackserver.py', _bg=True)
    return p


def make_numpy_test_image(pixel_order='CHW'):
    im = np.zeros((3, 200, 200), dtype=np.uint8)
    im[0, :50, :50] = 255
    im[2, 100:, 100:] = 255
    if pixel_order == 'HWC':
        im = im.transpose(1, 2, 0)
    return im


def make_pil_test_image():
    im = Image.new('RGB', (200, 200))
    return im


@pytest.mark.parametrize('asynchronous', [False, True])
def test_client(asynchronous):
    client = ExperimentTracker(async_=asynchronous)

    # exercise logging
    client.log('log message')
    client.debug('debug message')
    client.info('information message')
    client.warn('warning message')
    client.error('error message')
    client.critical('critical message')

    # exercise experiment metadata
    client.description('Test client')
    client.parameter('lr', 0.01)
    client.parameter('gg', 0)

    # exercise epoch
    client.begin_epoch()

    # exercise progress
    for i in range(5):
        client.progress(i+1, 5)

    # exercise metrics
    client.metric('a/b', 1.0)
    client.metric('c/d', -1.0)

    # exercise image save
    client.image('test1', make_numpy_test_image('CHW'))
    client.image('test2', make_numpy_test_image('HWC'))
    client.image('test3', make_numpy_test_image('HWC'), pixel_order='HWC')
    client.image('test3', make_pil_test_image())
    client.end_epoch()

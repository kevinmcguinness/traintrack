# -*- coding: utf-8 -*-
# (c) Copyright 2020 Kevin McGuinness. All Rights Reserved
from . import api
from ..util import timestamp, style_level
from ..util import make_epoch_summary

from click import echo
from shutil import get_terminal_size


class Epoch(api.Epoch):
    def __init__(self, experiment, epoch):
        super().__init__(experiment, epoch)

    def begin(self):
        if self.progress_bar is not None:
            self.progress_bar.close()
            self.progress_bar = None
        self.progress_bar = ProgressBar()

    def progress(self, completed, total, info=None):
        if self.progress is None:
            self.progress_bar = ProgressBar()
        prefix = f'{self.epoch:03d}: '
        suffix = f'[{completed}/{total}]'
        if info:
            suffix = ' ' + info
        self.progress_bar.update(completed, total, prefix, suffix)

    def end(self):
        self.progress_bar.close()
        self.progress_bar = None


class Experiment(api.Experiment):
    epoch_type = Epoch

    def __init__(self, tracker, name):
        super().__init__(tracker, name)


class ProgressTracker(api.ExperimentTracker):
    experiment_type = Experiment


class ProgressBar(object):

    def __init__(self, block_char=chr(9608)):
        self.block_char = block_char

    def update(self, completed, total, prefix, suffix):
        if completed > total:
            completed = total
        proportion = completed / total
        w, h = get_terminal_size()
        remainder = w - len(prefix) - len(suffix)
        num_blocks = int(remainder * proportion)
        num_spaces = remainder - num_blocks
        spaces = ''.join([' '] * num_spaces)
        bar = ''.join([self.block_char]*num_blocks)

        # clear line
        print('\x1b[2K', end='', flush=False)

        # print bar
        print('\r', prefix, bar, spaces, suffix, end='', sep='', flush=True)

    def close(self):
        print(flush=True)


ExperimentTracker = ProgressTracker

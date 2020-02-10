#!/usr/bin/env python
# -*- coding: utf-8 -*-
# (c) Copyright 2020 Kevin McGuinness. All Rights Reserved
import time

from traintrack.client import ExperimentTracker


def main():
    tracker = ExperimentTracker()

    loss_train = 6.128
    loss_valid = 7.541
    acc_valid = 0.4

    for epoch in range(1, 3):
        tracker.begin_epoch(epoch)

        # train
        tracker.begin_task('train')
        for i in range(100):
            tracker.progress(i+1, 100)
            time.sleep(0.01)
        tracker.end_task()
        tracker.metric('loss/train', loss_train)

        # validate
        tracker.begin_task('validate')
        for i in range(5):
            tracker.progress(i+1, 5)
            time.sleep(0.01)
        tracker.end_task()
        tracker.metric('loss/valid', loss_valid)
        tracker.metric('acc/valid', acc_valid)

        tracker.end_epoch()

        loss_train = loss_train*0.9
        loss_valid = loss_valid*0.9
        acc_valid = acc_valid + 0.05


if __name__ == '__main__':
    main()

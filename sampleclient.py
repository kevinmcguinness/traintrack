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

    for epoch in range(1, 11):
        tracker.begin_epoch(epoch)

        for i in range(100):
            tracker.progress(i+1, 100)
            time.sleep(0.1)

        tracker.metric('loss/train', loss_train)
        tracker.metric('loss/valid', loss_valid)
        tracker.metric('acc/valid', acc_valid)

        tracker.end_epoch()

        loss_train = loss_train*0.9
        loss_valid = loss_valid*0.9
        acc_valid = acc_valid + 0.05


if __name__ == '__main__':
    main()

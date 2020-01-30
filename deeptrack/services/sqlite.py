# -*- coding: utf-8 -*-
# (c) Copyright 2020 Kevin McGuinness. All Rights Reserved
from . import api

import sqlite3


class Epoch(api.Epoch):
    def __init__(self, experiment, epoch):
        super().__init__(experiment, epoch)

    @property
    def connection(self):
        return self.experiment.connection

    def metric(self, name, value):
        set_metric(self.connection, self.experiment.name,
                   self.epoch, name, value)

    def image(self, name, image):
        print(f'[{self.experiment.name}] [{self.epoch}] image {name}')


class Experiment(api.Experiment):
    epoch_type = Epoch

    def __init__(self, tracker, name):
        super().__init__(tracker, name)
        insert_experiment(tracker.connection, name)

    @property
    def connection(self):
        return self.tracker.connection

    def description(self, text):
        set_description(self.connection, self.name, text)

    def parameter(self, name, value):
        set_parameter(self.connection, self.name, name, value)


class SqliteTracker(api.ExperimentTracker):
    experiment_type = Experiment

    def __init__(self, database, **kwargs):
        super().__init__()
        self.database = database
        self.connection = sqlite3.connect(database, **kwargs)
        create_schema(self.connection)


ExperimentTracker = SqliteTracker


def insert_experiment(con, experiment_name, description=None):
    con.execute(r"""
    INSERT INTO experiments VALUES (?, ?)
    """, (experiment_name, description))
    con.commit()


def set_description(con, experiment_name, description):
    con.execute(r"""
    UPDATE experiments SET description=? WHERE name=?
    """, (description, experiment_name))
    con.commit()


def set_parameter(con, experiment_name, key, value):
    con.execute(r"""
    INSERT OR REPLACE INTO parameters VALUES (?, ?, ?)
    """, (experiment_name, key, value))
    con.commit()


def set_metric(con, experiment_name, epoch, key, value):
    # import ipdb; ipdb.set_trace()
    con.execute(r"""
    INSERT OR REPLACE INTO metrics VALUES (?, ?, ?, ?)
    """, (experiment_name, epoch, key, value))
    con.commit()


def create_schema(con):
    con.execute(r"""
    CREATE TABLE IF NOT EXISTS experiments (
        name TEXT PRIMARY KEY,
        description TEXT)
    """)

    con.execute(r"""
    CREATE TABLE IF NOT EXISTS parameters (
        experiment TEXT,
        name TEXT UNIQUE,
        value TEXT,
        PRIMARY KEY (experiment, name)
        FOREIGN KEY (experiment) REFERENCES experiments (experiment))
    """)

    con.execute(r"""
    CREATE TABLE IF NOT EXISTS metrics (
        experiment TEXT,
        epoch INTEGER,
        name TEXT,
        value NUMERIC,
        PRIMARY KEY (experiment, epoch, name)
        FOREIGN KEY (experiment) REFERENCES experiments (experiment))
    """)
    con.commit()

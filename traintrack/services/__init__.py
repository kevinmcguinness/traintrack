from .debug import DebugTracker
from .tensorboard import TensorboardTracker
from .sqlite import SqliteTracker
from .console import ConsoleTracker
from .slack import SlackTracker
from .logfile import LogfileTracker
from .progress import ProgressTracker
from importlib import import_module


trackers = {
    'debug': DebugTracker,
    'tensorboard': TensorboardTracker,
    'sqlite': SqliteTracker,
    'console': ConsoleTracker,
    'slack': SlackTracker,
    'logfile': LogfileTracker,
    'progress': ProgressTracker
}


def available_trackers():
    return list(trackers.keys())


def install_tracker(name, constructor):
    trackers[name] = constructor


def create_tracker(name, **kwargs):
    if name == 'custom':
        modulename = kwargs.pop('modulename')
        classname = kwargs.pop('classname')
        tracker_module = import_module(modulename)
        tracker = getattr(tracker_module, classname)
    else:
        tracker = trackers[name]
    return tracker(**kwargs)


def add_trackers_from_config(server, config, log=None):
    for tracker_cfg in config['trackers']:
        tracker_name = tracker_cfg['type']
        tracker_kwargs = tracker_cfg.get('config', {})
        if log:
            log.info(f'Adding tracker: {tracker_name} {tracker_kwargs}')
        tracker = create_tracker(tracker_name, **tracker_kwargs)
        server.register_tracker(tracker)

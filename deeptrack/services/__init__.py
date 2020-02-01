from .debug import DebugTracker
from .tensorboard import TensorboardTracker
from .sqlite import SqliteTracker
from .console import ConsoleTracker
from .slack import SlackTracker
from .logfile import LogfileTracker
from .progress import ProgressTracker


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
    tracker = trackers[name]
    return tracker(**kwargs)

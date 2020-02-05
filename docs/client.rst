
.. automodule:: traintrack.client
.. currentmodule:: traintrack.client

ExperimentTracker
=================

Use the ``ExperimentTracker`` class to connect to the trackserver and
report progress and metrics of experiments.


Example:

.. code-block:: python

   from traintrack.client import ExperimentTracker

   tracker = ExperimentTracker()

   for epoch in range(1, 11):
       tracker.begin_epoch(epoch)

       for i, batch in enumerate(batches):
           # train on a batch
           # ...
           tracker.progress(i+1, n_batches)

       # report metrics for the epoch
       tracker.metric('loss/train', loss_train)
       tracker.metric('loss/valid', loss_valid)
       tracker.metric('acc/valid', acc_valid)
       tracker.end_epoch()




.. autoclass:: ExperimentTracker
    :members:

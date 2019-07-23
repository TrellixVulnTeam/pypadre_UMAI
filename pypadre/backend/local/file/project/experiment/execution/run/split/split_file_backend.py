import os
import shutil
import uuid

from pypadre.backend.interfaces.backend.generic.i_base_file_backend import File
from pypadre.backend.interfaces.backend.i_split_backend import ISplitBackend
from pypadre.backend.local.file.project.experiment.execution.run.split.result.result_file_backend import PadreResultFileBackend
from pypadre.backend.local.file.project.experiment.execution.run.split.metric.metric_file_backend import PadreMetricFileBackend
from pypadre.backend.serialiser import JSonSerializer, PickleSerializer


class PadreSplitFileBackend(ISplitBackend):

    def __init__(self, parent):
        super().__init__(parent)
        self.root_dir = os.path.join(self._parent.root_dir, "splits")
        self._result = PadreResultFileBackend(self)
        self._metric = PadreMetricFileBackend(self)

    RESULTS_FILE = File("results.json", JSonSerializer)
    METRICS_FILE = File("metrics.json", JSonSerializer)
    METADATA_FILE = File("metadata.json", JSonSerializer)

    @property
    def result(self):
        return self._result

    @property
    def metric(self):
        return self._metric

    def to_folder_name(self, split):
        return split.id

    def get_by_dir(self, directory):
        pass

    def log(self, msg):
        pass

    def put_progress(self, split, **kwargs):
        self.log(
            "Split " + split + " PROGRESS: {curr_value}/{limit}. phase={phase} \n".format(**kwargs))

    def list(self, search):
        pass

    def get(self, uid):
        pass

    def put(self, split, allow_overwrite=False):
        """
        Stores a split of an experiment to the file repository.
        :param allow_overwrite: allow overwrite of experiment
        :param split: split to put
        :return:
        """

        if split.id is None:  # this is a new experiment
            split.id = uuid.uuid4()

        directory = self.get_dir(self.to_folder_name(split))

        if os.path.exists(directory) and not allow_overwrite:
            raise ValueError("Split %s already exists." +
                             "Overwriting not explicitly allowed. Set allow_overwrite=True".format(split.id))
        else:
            shutil.rmtree(directory)
        os.mkdir(directory)

        self.write_file(directory, self.METADATA_FILE, split.metadata)

    def delete(self, uid):
        pass
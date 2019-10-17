from types import GeneratorType

from pypadre.core.metrics.metrics import Metric
from pypadre.pod.backend.i_padre_backend import IPadreBackend
from pypadre.pod.repository.i_repository import IMetricRepository
from pypadre.pod.repository.local.file.generic.i_file_repository import File, IChildFileRepository
from pypadre.pod.repository.local.file.generic.i_log_file_repository import ILogFileRepository
from pypadre.pod.repository.serializer.serialiser import JSonSerializer, PickleSerializer

NAME = "metrics"

META_FILE = File("metadata.json", JSonSerializer)
RESULT_FILE = File("results.bin", PickleSerializer)


class MetricFileRepository(IChildFileRepository, ILogFileRepository, IMetricRepository):

    @staticmethod
    def placeholder():
        return '{METRIC_ID}'

    def __init__(self, backend: IPadreBackend):
        super().__init__(parent=backend.run, name=NAME, backend=backend)

    def get_by_dir(self, directory):
        metadata = self.get_file(directory, META_FILE)
        result = self.get_file(directory, RESULT_FILE)

        # TODO Computation
        metric = Metric(metadata=metadata, result=result)
        return metric

    def put_progress(self, run, **kwargs):
        self.log(
            "RUN COMPUTATION: {curr_value}/{limit}. phase={phase} \n".format(**kwargs))

    def _put(self, obj, *args, directory: str, merge=False, **kwargs):
        metric = obj
        self.write_file(directory, META_FILE, metric.metadata)
        if not isinstance(metric.result, GeneratorType):
            self.write_file(directory, RESULT_FILE, metric.result, mode='wb')

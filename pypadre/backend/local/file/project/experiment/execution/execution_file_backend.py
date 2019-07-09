import os

from pypadre.backend.interfaces.backend.i_execution_backend import IExecutionBackend
from pypadre.backend.local.file.project.experiment.execution.run.run_file_backend import PadreRunFileBackend


class PadreExecutionFileBackend(IExecutionBackend):

    def __init__(self, parent):
        super().__init__(parent)
        self.root_dir = os.path.join(self._parent.root_dir, "executions")
        self._run = PadreRunFileBackend(self)

    @property
    def run(self):
        return self._run

    def list(self, search):
        pass

    def get(self, uid):
        pass

    def put(self, obj):
        pass

    def delete(self, uid):
        pass
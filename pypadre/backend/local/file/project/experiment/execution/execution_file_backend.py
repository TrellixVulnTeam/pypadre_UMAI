import os

from pypadre.backend.interfaces.backend.generic.i_base_file_backend import File
from pypadre.backend.interfaces.backend.i_execution_backend import IExecutionBackend
from pypadre.backend.local.file.project.experiment.execution.run.run_file_backend import PadreRunFileBackend
from pypadre.backend.serialiser import JSonSerializer


class PadreExecutionFileBackend(IExecutionBackend):

    def __init__(self, parent):
        super().__init__(parent)
        self.root_dir = os.path.join(self._parent.root_dir, "executions")
        self._run = PadreRunFileBackend(self)

    META_FILE = File("metadata.json", JSonSerializer)

    @property
    def run(self):
        return self._run

    def to_folder_name(self, obj):
        return obj.name

    def get(self, uid):
        """
        Shortcut because we know the uid is the folder name
        :param uid: Uid of the execution
        :return:
        """
        # TODO might be changed. Execution get folder name or id by git commit hash?
        return self.get_by_dir(self.get_dir(uid))

    def get_by_dir(self, directory):
        metadata = self.get_file(directory, self.META_FILE)
        #TODO parse to execution object
        pass

    def put(self, execution, allow_overwrite=True):
        directory = self.get_dir(self.to_folder_name(execution))

        if os.path.exists(directory) and not allow_overwrite:
            raise ValueError("Experiment %s already exists." +
                             "Overwriting not explicitly allowed. Set allow_overwrite=True".format(experiment.name))

        self.write_file(directory, self.META_FILE, execution.metadata)

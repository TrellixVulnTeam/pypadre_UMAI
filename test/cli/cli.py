
import unittest

from pypadre.app import PadreApp
from pypadre.app.dataset.dataset_app import DatasetApp
from pypadre.app.project.experiment.execution.execution_app import ExecutionApp
from pypadre.app.project.experiment.execution.run.run_app import RunApp
from pypadre.app.project.experiment.execution.run.split.split_app import SplitApp
from pypadre.app.project.experiment.experiment_app import ExperimentApp
from pypadre.app.project.project_app import ProjectApp
from pypadre.cli.padre import pypadre_cli


class PadreCli(unittest.TestCase):

    def test_cli(self):
        pypadre_cli
        # TODO test cli

if __name__ == '__main__':
    unittest.main()

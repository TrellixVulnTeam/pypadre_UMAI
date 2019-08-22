
import unittest

from pypadre.app import PadreApp
from pypadre.app.dataset.dataset_app import DatasetApp
from pypadre.app.project.experiment.execution.execution_app import ExecutionApp
from pypadre.app.project.experiment.execution.run.run_app import RunApp
from pypadre.app.project.experiment.execution.run.split.split_app import SplitApp
from pypadre.app.project.experiment.experiment_app import ExperimentApp
from pypadre.app.project.project_app import ProjectApp


class LocalBackends(unittest.TestCase):

    def test_app(self):
        PadreApp
        # TODO test app

    def test_datasets(self):
        dataset_app: DatasetApp = PadreApp.datasets
        # TODO test app

    def test_projects(self):
        project_app: ProjectApp = PadreApp.projects
        # TODO test app

    def test_executions(self):
        execution_app: ExecutionApp = PadreApp.executions
        # TODO test app

    def test_experiments(self):
        experiment_app: ExperimentApp = PadreApp.experiments
        # TODO test app

    def test_runs(self):
        run_app: RunApp = PadreApp.runs
        # TODO test app

    def test_splits(self):
        split_app: SplitApp = PadreApp.splits
        # TODO test app

if __name__ == '__main__':
    unittest.main()
